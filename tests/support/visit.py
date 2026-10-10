"""Une visite de la page dans Google Chrome : l'appareil, la position et l'heure du visiteur.

Le navigateur ne sort jamais de localhost : toute autre requête est bloquée et retenue.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime

from playwright.sync_api import Browser, BrowserContext, Page, Response, Route

PHONE_SCREEN = {"width": 390, "height": 844}


@dataclass(frozen=True)
class Position:
    """Ce que le navigateur répond quand la page demande où est le visiteur."""

    context_options: dict = field(default_factory=dict)
    script: str = ""


def a_shared_position(latitude: float, longitude: float) -> Position:
    return Position(
        {
            "geolocation": {"latitude": latitude, "longitude": longitude},
            "permissions": ["geolocation"],
        }
    )


# Sans autorisation accordée, Chrome refuse la demande de position.
REFUSED_POSITION = Position()
NO_GEOLOCATION = Position(script="delete Navigator.prototype.geolocation;")
# La demande reste sans réponse, comme une autorisation que le visiteur ignore.
UNANSWERED_POSITION = Position(script="Geolocation.prototype.getCurrentPosition = () => {};")


@dataclass(frozen=True)
class Device:
    """L'appareil du visiteur : son écran, son pointeur et sa boussole.

    `orientation` est une fonction JavaScript qui reçoit un cap et envoie à la page l'événement
    d'orientation que ce téléphone enverrait en pointant vers ce cap.
    """

    is_phone: bool
    script: str = ""
    orientation: str = ""

    def context_options(self) -> dict:
        if not self.is_phone:
            return {}
        return {"has_touch": True, "is_mobile": True, "viewport": PHONE_SCREEN}


COMPUTER = Device(is_phone=False)
PHONE_WITHOUT_COMPASS = Device(is_phone=True, script="delete window.DeviceOrientationEvent;")

# Chrome sur Android : une orientation absolue, sans autorisation à demander.
ANDROID = Device(
    is_phone=True,
    script="delete DeviceOrientationEvent.requestPermission;",
    orientation="""heading => window.dispatchEvent(new DeviceOrientationEvent(
        "deviceorientationabsolute",
        { alpha: heading === null ? null : (360 - heading) % 360, absolute: heading !== null }))""",
)

# Un navigateur Android sans l'événement d'orientation absolue : l'orientation ordinaire dit
# si elle connaît le nord.
ANDROID_WITHOUT_ABSOLUTE_EVENT = Device(
    is_phone=True,
    script="""delete DeviceOrientationEvent.requestPermission;
        delete window.ondeviceorientationabsolute;""",
    orientation="""heading => window.dispatchEvent(new DeviceOrientationEvent(
        "deviceorientation",
        { alpha: heading === null ? 10 : (360 - heading) % 360, absolute: heading !== null }))""",
)


def an_iphone(permission: str) -> Device:
    """Safari sur iPhone : la boussole donne le cap, -1 tant qu'elle n'est pas étalonnée.

    `permission` est la réponse du visiteur, « granted » ou « denied », ou « fails » si la
    demande échoue. Le nombre de demandes est retenu dans la page.
    """
    answer = (
        'Promise.reject(new DOMException("refusé", "NotAllowedError"))'
        if permission == "fails"
        else f'Promise.resolve("{permission}")'
    )
    return Device(
        is_phone=True,
        script=f"""delete window.ondeviceorientationabsolute;
            window.compassPermissionRequests = 0;
            DeviceOrientationEvent.requestPermission = () => {{
              window.compassPermissionRequests += 1;
              return {answer};
            }};""",
        orientation="""heading => {
            const event = new DeviceOrientationEvent("deviceorientation",
              { alpha: 120, beta: 0, gamma: 0, absolute: false });
            Object.defineProperty(event, "webkitCompassHeading",
              { value: heading === null ? -1 : heading });
            window.dispatchEvent(event);
        }""",
    )


class Visit:
    """Une visite dans un contexte Chrome neuf, fermé à la fin du scénario.

    Avant d'ouvrir la page, chaque étape peut régler l'heure, l'appareil, la position et la
    préférence pour des animations réduites.
    """

    def __init__(self, browser: Browser, site_url: str, now: datetime) -> None:
        self._browser = browser
        self._site_url = site_url
        self._context: BrowserContext | None = None
        self.now = now
        self.device = COMPUTER
        self.position = REFUSED_POSITION
        self.reduces_motion = False
        self.responses: list[Response] = []
        self.blocked_urls: list[str] = []
        self.page: Page | None = None

    def opens(self, path: str) -> Page:
        self._context = self._browser.new_context(
            locale="fr-FR",
            timezone_id="Europe/Paris",
            reduced_motion="reduce" if self.reduces_motion else "no-preference",
            **self.device.context_options(),
            **self.position.context_options,
        )
        # Seules les requêtes qui sortent du site passent par ici : celles du site restent dans
        # le navigateur, même quand le test attend sans piloter Playwright.
        self._context.route(re.compile(f"^(?!{re.escape(self._site_url)}/)"), self._blocks)
        for script in (self.device.script, self.position.script):
            if script:
                self._context.add_init_script(script)
        self.page = self._context.new_page()
        self.page.on("response", self._remembers)
        # L'heure du visiteur ne bouge que quand un scénario la fait avancer.
        self.page.clock.install(time=self.now)
        self.page.clock.pause_at(self.now)
        self.page.goto(self._site_url + path)
        return self.page

    def points_phone_to(self, heading: float | None) -> None:
        """Le téléphone tenu à plat pointe vers ce cap, ou None s'il ne sait pas où est le nord."""
        self.page.evaluate(self.device.orientation, heading)

    def ends(self) -> None:
        if self._context is not None:
            self._context.close()

    def _remembers(self, response: Response) -> None:
        self.responses.append(response)

    def _blocks(self, route: Route) -> None:
        self.blocked_urls.append(route.request.url)
        route.abort()
