"""Un faux CelesTrak sur localhost : de vraies requêtes HTTP, sans dépendre du réseau."""

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class FakeCelestrak:
    def __init__(self) -> None:
        self.body = ""
        self.status = 200
        self.requests: list[dict[str, list[str]]] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 (nom imposé par http.server)
                fake.requests.append(parse_qs(urlparse(self.path).query))
                payload = fake.body.encode("utf-8")
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

    def publishes(self, *lines: str) -> None:
        self.body = "\r\n".join(lines) + "\r\n"
        self.status = 200

    def fails_with(self, status: int) -> None:
        self.status = status
