"""Un faux CelesTrak sur localhost : de vraies requêtes HTTP, sans dépendre du réseau.

Il joue aussi le relais des catalogues, qui sert chaque groupe dans un fichier <groupe>.csv.
"""

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import PurePosixPath
from urllib.parse import parse_qs, urlparse

from tests.support.omm import cut_short, omm_csv_from_tle


class FakeCelestrak:
    def __init__(self) -> None:
        self.body = ""
        self.bodies_by_group: dict[str, str] = {}
        self.status = 200
        self.statuses_by_group: dict[str, int] = {}
        self.cuts_off = False
        self.requests: list[dict[str, list[str]]] = []
        self.paths: list[str] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 (nom imposé par http.server)
                url = urlparse(self.path)
                query = parse_qs(url.query)
                fake.requests.append(query)
                fake.paths.append(url.path)
                [group] = query.get("GROUP", [PurePosixPath(url.path).stem])
                payload = fake.bodies_by_group.get(group, fake.body).encode("utf-8")
                self.send_response(fake.statuses_by_group.get(group, fake.status))
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                # Interrompue, la réponse s'arrête à la moitié de la longueur annoncée.
                self.wfile.write(payload[: len(payload) // 2] if fake.cuts_off else payload)

            def log_message(self, *args) -> None:
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        base = f"http://127.0.0.1:{self._server.server_port}"
        self.url_template = base + "/NORAD/elements/gp.php?GROUP={group}&FORMAT=csv"
        self.relay_url_template = base + "/releases/download/catalogues/{group}.csv"

    def __enter__(self) -> "FakeCelestrak":
        # Scrutation courte : l'arrêt du serveur n'attend pas une demi-seconde à chaque test.
        threading.Thread(
            target=self._server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        ).start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()

    def publishes(self, *lines: str, group: str | None = None) -> None:
        """Publie ces lignes pour un groupe donné, ou pour tous les groupes sans réponse propre."""
        body = "\r\n".join(lines) + "\r\n"
        if group is None:
            self.body = body
        else:
            self.bodies_by_group[group] = body
        self.status = 200
        self.cuts_off = False

    def publishes_as_omm(self, *entries: tuple[str, str, str], group: str | None = None) -> None:
        """Publie ces TLE (nom, ligne 1, ligne 2), convertis en catalogue OMM au format CSV."""
        self.publishes(*omm_csv_from_tle(*entries).splitlines(), group=group)

    def publishes_a_web_page(self) -> None:
        """Répond une page web, comme une page de maintenance, au lieu d'un catalogue."""
        self.publishes(
            "<!DOCTYPE html>",
            "<html><head><title>Maintenance</title></head>",
            "<body>Back soon.</body></html>",
        )

    def publishes_an_endless_line(self) -> None:
        """Répond une page web d'un seul tenant, plus longue qu'un champ CSV ne peut l'être."""
        self.publishes("<!DOCTYPE html><html><body>" + "x" * 200_000 + "</body></html>")

    def publishes_cut_short(self, catalog: str) -> None:
        """Publie ce catalogue coupé entre deux colonnes de son premier satellite."""
        self.publishes(*cut_short(catalog).splitlines())

    def cuts_off_its_answers(self) -> None:
        """Annonce chaque catalogue en entier, n'en envoie que la moitié et raccroche."""
        self.cuts_off = True

    def fails_with(self, status: int, group: str | None = None) -> None:
        """Répond cette erreur pour un groupe donné, ou pour tous les groupes sans erreur propre."""
        if group is None:
            self.status = status
        else:
            self.statuses_by_group[group] = status
