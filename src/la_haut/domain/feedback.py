import re
from dataclasses import dataclass
from enum import StrEnum

MAX_MESSAGE_LENGTH = 2000
# La longueur maximale d'une adresse e-mail utilisable (RFC 5321).
MAX_CONTACT_LENGTH = 254
# Volontairement simple : une adresse plausible, pas une vérification complète.
EMAIL_ADDRESS = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


class InvalidFeedbackError(ValueError):
    """Un avis vide, trop long ou avec une adresse illisible ne part pas."""


class FeedbackKind(StrEnum):
    """Ce que le visiteur veut dire à l'auteur du site."""

    PROBLEM = "problem"
    IDEA = "idea"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Feedback:
    """Un message d'un visiteur à l'auteur du site, avec son e-mail s'il veut une réponse."""

    kind: FeedbackKind
    message: str
    contact: str | None = None

    def __post_init__(self) -> None:
        message = self.message.strip()
        if not message:
            raise InvalidFeedbackError("Écris ton message avant de l'envoyer.")
        if len(message) > MAX_MESSAGE_LENGTH:
            raise InvalidFeedbackError(
                f"Ton message dépasse {MAX_MESSAGE_LENGTH} caractères : raccourcis-le un peu."
            )
        contact = (self.contact or "").strip() or None
        if contact is not None and (
            len(contact) > MAX_CONTACT_LENGTH or not EMAIL_ADDRESS.fullmatch(contact)
        ):
            raise InvalidFeedbackError("Cette adresse e-mail ne semble pas valide.")
        object.__setattr__(self, "message", message)
        object.__setattr__(self, "contact", contact)
