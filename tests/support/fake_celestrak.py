"""Un faux CelesTrak sur localhost : de vraies requêtes HTTP, sans dépendre du réseau."""

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class FakeCelestrak:
    def __init__(self) -> None:
        self.body = ""
        self.bodies_by_group: dict[str, str] = {}
        self.status = 200
        self.requests: list[dict[str, list[str]]] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 (nom imposé par http.server)
                query = parse_qs(urlparse(self.path).query)
                fake.requests.append(query)
                [group] = query.get("GROUP", [""])
                payload = fake.bodies_by_group.get(group, fake.body).encode("utf-8")
                self.send_response(fake.status)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args) -> None:
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_port}/NORAD/elements/gp.php"

    def __enter__(self) -> "FakeCelestrak":
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
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

    def fails_with(self, status: int) -> None:
        self.status = status
