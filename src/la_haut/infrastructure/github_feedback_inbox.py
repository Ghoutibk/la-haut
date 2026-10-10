import json
import logging
import re
import ssl
import urllib.request
from datetime import datetime

import certifi

from la_haut.application.ports import FeedbackNotConfiguredError, FeedbackUnavailableError
from la_haut.domain.feedback import Feedback, FeedbackKind

GITHUB_API_URL = "https://api.github.com"
REQUEST_TIMEOUT_S = 10
TITLE_LENGTH = 70
# Les étiquettes et les titres du dépôt d'avis, en français.
LABELS = {FeedbackKind.PROBLEM: "problème", FeedbackKind.IDEA: "idée", FeedbackKind.OTHER: "autre"}
TITLE_PREFIXES = {
    FeedbackKind.PROBLEM: "Problème",
    FeedbackKind.IDEA: "Idée",
    FeedbackKind.OTHER: "Autre",
}

logger = logging.getLogger(__name__)


def _title(feedback: Feedback) -> str:
    first_line = feedback.message.splitlines()[0]
    if len(first_line) > TITLE_LENGTH:
        first_line = first_line[: TITLE_LENGTH - 1] + "…"
    return f"{TITLE_PREFIXES[feedback.kind]} : {first_line}"


def _quoted(message: str) -> str:
    """Le message dans un bloc de code : une mention @quelqu'un n'y notifie personne.

    La clôture est plus longue que toute suite d'accents graves du message, qui ne peut en sortir.
    """
    longest = max((len(run) for run in re.findall(r"`+", message)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{message}\n{fence}"


def _body(feedback: Feedback, sent_at: datetime) -> str:
    contact = f"`{feedback.contact}`" if feedback.contact else "aucun e-mail laissé"
    return (
        f"{_quoted(feedback.message)}\n\n"
        f"Contact : {contact}\n"
        f"Envoyé depuis Là-haut le {sent_at:%d/%m/%Y à %H:%M} UTC\n"
    )


class GitHubIssuesFeedbackInbox:
    """Adaptateur FeedbackInbox : chaque avis devient un ticket d'un dépôt GitHub privé.

    Le jeton n'a besoin que du droit d'écrire les tickets de ce dépôt.
    """

    def __init__(self, repository: str, token: str, api_url: str = GITHUB_API_URL) -> None:
        self._repository = repository
        self._token = token
        self._api_url = api_url

    def deliver(self, feedback: Feedback, sent_at: datetime) -> None:
        issue = {
            "title": _title(feedback),
            "body": _body(feedback, sent_at),
            "labels": [LABELS[feedback.kind]],
        }
        request = urllib.request.Request(
            f"{self._api_url}/repos/{self._repository}/issues",
            data=json.dumps(issue).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
                "User-Agent": "la-haut",
            },
        )
        context = ssl.create_default_context(cafile=certifi.where())
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S, context=context):
                pass
        except OSError as error:
            logger.warning("Avis non remis au dépôt %s : %s", self._repository, error)
            raise FeedbackUnavailableError("GitHub n'a pas pris l'avis") from error


class UnconfiguredFeedbackInbox:
    """Adaptateur FeedbackInbox quand aucun dépôt ni jeton n'est réglé : rien ne part."""

    def deliver(self, feedback: Feedback, sent_at: datetime) -> None:
        raise FeedbackNotConfiguredError("La boîte à avis n'est pas configurée")
