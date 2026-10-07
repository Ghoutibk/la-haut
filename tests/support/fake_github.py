"""Un faux GitHub sur localhost : il reçoit les tickets créés par l'API, sans toucher le réseau."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class FakeGitHub:
    def __init__(self) -> None:
        self.status = 201
        self.requests: list[dict] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802 (nom imposé par http.server)
                length = int(self.headers.get("Content-Length", 0))
                fake.requests.append(
                    {
                        "path": self.path,
                        "headers": dict(self.headers),
                        "json": json.loads(self.rfile.read(length) or b"null"),
                    }
                )
                payload = json.dumps({"number": len(fake.requests)}).encode("utf-8")
                self.send_response(fake.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args) -> None:
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_port}"

    def __enter__(self) -> "FakeGitHub":
        # Scrutation courte : l'arrêt du serveur n'attend pas une demi-seconde à chaque test.
        threading.Thread(
            target=self._server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        ).start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()

    @property
    def issues(self) -> list[dict]:
        """Les tickets reçus, tels que l'API les a envoyés."""
        return [request["json"] for request in self.requests]

    def fails_with(self, status: int) -> None:
        self.status = status
