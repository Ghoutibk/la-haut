"""Racine de composition : seul endroit qui connaît cas d'usage et adaptateurs à la fois."""

import logging
import os
from pathlib import Path

from fastapi import FastAPI

from la_haut.application.combined_satellite_catalog import CombinedSatelliteCatalog
from la_haut.application.famous_satellite_catalog import FamousSatelliteCatalog
from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.identify_sighting_with_planets import IdentifySightingWithPlanets
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.list_visible_passes_by_slot import ListVisiblePassesBySlot
from la_haut.application.ports import SatelliteCatalog
from la_haut.application.send_feedback import SendFeedback
from la_haut.application.starlink_catalog import StarlinkCatalog
from la_haut.infrastructure.celestrak_satellite_catalog import (
    CELESTRAK_URL_TEMPLATE,
    CelestrakSatelliteCatalog,
)
from la_haut.infrastructure.github_feedback_inbox import (
    GITHUB_API_URL,
    GitHubIssuesFeedbackInbox,
    UnconfiguredFeedbackInbox,
)
from la_haut.infrastructure.skyfield_planet_locator import SkyfieldPlanetLocator
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog
from la_haut.interface.http.app import create_app

DEFAULT_CACHE_PATH = Path.home() / ".cache" / "la-haut" / "visual.csv"
# Les lancements des 30 derniers jours : les Starlink qui défilent encore en train.
RECENT_LAUNCHES_GROUP = "last-30-days"
FEEDBACK_REPOSITORY_SETTING = "LA_HAUT_FEEDBACK_REPO"
FEEDBACK_TOKEN_SETTING = "LA_HAUT_FEEDBACK_TOKEN"

logger = logging.getLogger(__name__)


def _list_visible_passes(catalog: SatelliteCatalog) -> ListVisiblePasses:
    return ListVisiblePasses(catalog=catalog, tracker=SkyfieldSkyTracker())


def build_list_visible_passes(catalog_path: Path) -> ListVisiblePasses:
    """Les satellites d'un fichier TLE local."""
    return _list_visible_passes(TleFileSatelliteCatalog(catalog_path))


def build_list_visible_passes_from_celestrak(
    cache_path: Path, url_template: str = CELESTRAK_URL_TEMPLATE
) -> ListVisiblePasses:
    """Les satellites célèbres et les Starlink récents, tenus à jour depuis CelesTrak.

    Chaque groupe a son propre cache, dans le dossier de `cache_path`.
    """
    brightest = CelestrakSatelliteCatalog(cache_path, url_template=url_template)
    recent_launches = CelestrakSatelliteCatalog(
        cache_path.with_name(f"{RECENT_LAUNCHES_GROUP}.csv"),
        group=RECENT_LAUNCHES_GROUP,
        url_template=url_template,
    )
    catalog = CombinedSatelliteCatalog(
        FamousSatelliteCatalog(brightest), StarlinkCatalog(recent_launches)
    )
    return _list_visible_passes(catalog)


def _identify_sighting(list_visible_passes: ListVisiblePasses) -> IdentifySightingWithPlanets:
    return IdentifySightingWithPlanets(
        IdentifySighting(list_visible_passes), SkyfieldPlanetLocator()
    )


def build_identify_sighting(catalog_path: Path) -> IdentifySightingWithPlanets:
    """« C'était quoi, ça ? » parmi les satellites d'un fichier TLE local et les planètes."""
    return _identify_sighting(build_list_visible_passes(catalog_path))


def build_identify_sighting_from_celestrak(
    cache_path: Path, url_template: str = CELESTRAK_URL_TEMPLATE
) -> IdentifySightingWithPlanets:
    """« C'était quoi, ça ? » parmi les satellites suivis depuis CelesTrak et les planètes."""
    return _identify_sighting(build_list_visible_passes_from_celestrak(cache_path, url_template))


def build_send_feedback(
    repository: str | None, token: str | None, api_url: str = GITHUB_API_URL
) -> SendFeedback:
    """Les avis des visiteurs, en tickets d'un dépôt GitHub privé ; sans jeton, rien ne part."""
    if repository and token:
        return SendFeedback(GitHubIssuesFeedbackInbox(repository, token, api_url=api_url))
    return SendFeedback(UnconfiguredFeedbackInbox())


def _send_feedback_from_environment(api_url: str) -> SendFeedback:
    """Les réglages d'avis, sans les espaces collés autour ; un réglage absent est nommé dans les
    logs dès le démarrage, sans jamais écrire une valeur."""
    settings = {
        name: os.environ.get(name, "").strip()
        for name in (FEEDBACK_REPOSITORY_SETTING, FEEDBACK_TOKEN_SETTING)
    }
    missing = [name for name, value in settings.items() if not value]
    if missing:
        logger.warning("Avis désactivés, réglage absent : %s", ", ".join(missing))
    return build_send_feedback(
        settings[FEEDBACK_REPOSITORY_SETTING], settings[FEEDBACK_TOKEN_SETTING], api_url=api_url
    )


def build_web_app(
    cache_path: Path | None = None,
    url_template: str | None = None,
    feedback_api_url: str = GITHUB_API_URL,
) -> FastAPI:
    """Le site Là-haut : uvicorn --factory la_haut.composition:build_web_app

    Le cache CelesTrak se règle avec la variable d'environnement LA_HAUT_CACHE. La source des
    catalogues se règle avec LA_HAUT_CATALOG_URL, une adresse où {group} est remplacé par le nom
    du groupe : CelesTrak par défaut, ou un relais qui le recopie. Les avis partent en tickets du
    dépôt LA_HAUT_FEEDBACK_REPO, avec le jeton LA_HAUT_FEEDBACK_TOKEN.
    """
    cache_path = cache_path or Path(os.environ.get("LA_HAUT_CACHE", DEFAULT_CACHE_PATH))
    url_template = url_template or os.environ.get("LA_HAUT_CATALOG_URL", CELESTRAK_URL_TEMPLATE)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    list_visible_passes = build_list_visible_passes_from_celestrak(cache_path, url_template)
    # « Ce soir » se resert par quarts d'heure ; l'identification calcule au moment signalé.
    send_feedback = _send_feedback_from_environment(feedback_api_url)
    return create_app(
        ListVisiblePassesBySlot(list_visible_passes),
        _identify_sighting(list_visible_passes),
        send_feedback=send_feedback,
    )
