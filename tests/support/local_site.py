"""Le site Là-haut servi sur un port libre de localhost, pour le piloter depuis un vrai navigateur.

Un seul serveur uvicorn pour toute la session : chaque scénario lui confie sa propre application,
construite sur les doublures de `tests/support`.
"""

import asyncio
import socket
import threading
import time

import uvicorn

STARTUP_PATIENCE_S = 5.0
# Le site répond dans un autre fil : ce qu'il a reçu se vérifie avec un peu de patience.
CHECK_PATIENCE_S = 5.0
# Au-delà, une réponse retenue part quand même : un scénario oublié ne bloque pas le serveur.
HOLD_PATIENCE_S = 10.0


class LocalSite:
    def __init__(self) -> None:
        self._app = None
        self._held: dict[str, threading.Event] = {}
        self._down: set[str] = set()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(("127.0.0.1", 0))
        self.url = f"http://127.0.0.1:{self._socket.getsockname()[1]}"
        config = uvicorn.Config(
            self._serve, interface="asgi3", lifespan="off", log_config=None, access_log=False
        )
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(
            target=self._server.run, kwargs={"sockets": [self._socket]}, daemon=True
        )

    def __enter__(self) -> "LocalSite":
        self._thread.start()
        deadline = time.monotonic() + STARTUP_PATIENCE_S
        while not self._server.started:
            if time.monotonic() > deadline:
                raise RuntimeError("Le site local n'a pas démarré")
            time.sleep(0.01)
        return self

    def __exit__(self, *exc) -> None:
        self.reset()
        self._server.should_exit = True
        self._thread.join()

    def serves(self, app) -> None:
        """Confie le site à l'application du scénario en cours."""
        self._app = app

    def holds(self, path: str) -> None:
        """Retient les réponses à ce chemin jusqu'à `answers`."""
        self._held[path] = threading.Event()

    def answers(self) -> None:
        """Laisse partir les réponses retenues."""
        for gate in self._held.values():
            gate.set()
        self._held.clear()

    def goes_down_on(self, prefix: str) -> None:
        """Les chemins qui commencent ainsi répondent comme un hébergeur en panne : 502 et une
        page HTML, sans explication."""
        self._down.add(prefix)

    def reset(self) -> None:
        """Ni application, ni réponse retenue, ni panne : prêt pour le scénario suivant."""
        self.answers()
        self._down.clear()
        self._app = None

    async def _serve(self, scope, receive, send) -> None:
        path = scope.get("path", "")
        if any(path.startswith(prefix) for prefix in self._down):
            await _bad_gateway(send)
            return
        gate = self._held.get(path)
        if gate is not None:
            await asyncio.to_thread(gate.wait, HOLD_PATIENCE_S)
        await self._app(scope, receive, send)


async def _bad_gateway(send) -> None:
    body = b"<html><body><h1>502 Bad Gateway</h1></body></html>"
    await send(
        {
            "type": "http.response.start",
            "status": 502,
            "headers": [
                (b"content-type", b"text/html"),
                (b"content-length", str(len(body)).encode()),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


def eventually(check) -> None:
    """Refait la vérification jusqu'à ce qu'elle passe, ou échoue au bout de la patience."""
    deadline = time.monotonic() + CHECK_PATIENCE_S
    while True:
        try:
            check()
            return
        except AssertionError:
            if time.monotonic() > deadline:
                raise
            time.sleep(0.02)
