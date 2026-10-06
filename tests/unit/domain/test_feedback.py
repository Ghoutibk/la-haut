import pytest

from la_haut.domain.feedback import (
    MAX_CONTACT_LENGTH,
    MAX_MESSAGE_LENGTH,
    Feedback,
    FeedbackKind,
    InvalidFeedbackError,
)


def test_the_message_is_kept_without_the_spaces_around_it():
    assert Feedback(FeedbackKind.IDEA, "  Ajouter la Lune \n").message == "Ajouter la Lune"


@pytest.mark.parametrize("message", ["", "   \n "])
def test_an_empty_message_is_refused(message):
    with pytest.raises(InvalidFeedbackError):
        Feedback(FeedbackKind.PROBLEM, message)


def test_a_message_longer_than_the_limit_is_refused():
    with pytest.raises(InvalidFeedbackError):
        Feedback(FeedbackKind.OTHER, "a" * (MAX_MESSAGE_LENGTH + 1))


@pytest.mark.parametrize("contact", [None, "", "   "])
def test_the_contact_is_optional(contact):
    assert Feedback(FeedbackKind.IDEA, "Merci !", contact).contact is None


def test_the_contact_is_kept_without_the_spaces_around_it():
    feedback = Feedback(FeedbackKind.PROBLEM, "La page reste vide", " claire@example.org ")

    assert feedback.contact == "claire@example.org"


@pytest.mark.parametrize("contact", ["claire", "claire@", "@example.org", "cl aire@example.org"])
def test_a_contact_that_is_not_an_email_address_is_refused(contact):
    with pytest.raises(InvalidFeedbackError):
        Feedback(FeedbackKind.PROBLEM, "La page reste vide", contact)


def test_a_contact_longer_than_an_email_address_can_be_is_refused():
    too_long = "a" * MAX_CONTACT_LENGTH + "@example.org"

    with pytest.raises(InvalidFeedbackError):
        Feedback(FeedbackKind.PROBLEM, "La page reste vide", too_long)
