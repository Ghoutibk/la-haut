from datetime import timedelta

import pytest

from la_haut.application.ports import FeedbackUnavailableError
from la_haut.application.send_feedback import FeedbackLimitReachedError, SendFeedback
from la_haut.domain.feedback import Feedback, FeedbackKind
from tests.support.builders import DEFAULT_INSTANT
from tests.support.fakes import FakeFeedbackInbox, UnavailableFeedbackInbox

AN_IDEA = Feedback(FeedbackKind.IDEA, "Ajouter les passages de la Lune")


class Clock:
    def __init__(self) -> None:
        self.now = DEFAULT_INSTANT

    def __call__(self):
        return self.now


def test_the_feedback_is_delivered_with_the_moment_it_was_sent():
    inbox = FakeFeedbackInbox()

    SendFeedback(inbox, clock=lambda: DEFAULT_INSTANT).execute(AN_IDEA)

    assert inbox.delivered == [(AN_IDEA, DEFAULT_INSTANT)]


def test_beyond_the_hourly_limit_the_feedback_is_refused_and_not_delivered():
    inbox = FakeFeedbackInbox()
    send_feedback = SendFeedback(inbox, clock=Clock(), max_per_hour=2)
    send_feedback.execute(AN_IDEA)
    send_feedback.execute(AN_IDEA)

    with pytest.raises(FeedbackLimitReachedError):
        send_feedback.execute(AN_IDEA)

    assert len(inbox.delivered) == 2


def test_an_hour_later_feedback_is_accepted_again():
    inbox = FakeFeedbackInbox()
    clock = Clock()
    send_feedback = SendFeedback(inbox, clock=clock, max_per_hour=1)
    send_feedback.execute(AN_IDEA)

    clock.now += timedelta(hours=1)
    send_feedback.execute(AN_IDEA)

    assert len(inbox.delivered) == 2


def test_a_feedback_that_could_not_be_delivered_does_not_count_in_the_limit():
    send_feedback = SendFeedback(UnavailableFeedbackInbox(), clock=Clock(), max_per_hour=1)
    with pytest.raises(FeedbackUnavailableError):
        send_feedback.execute(AN_IDEA)

    with pytest.raises(FeedbackUnavailableError):
        send_feedback.execute(AN_IDEA)
