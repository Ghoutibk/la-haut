import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.composition import build_send_feedback
from la_haut.domain.feedback import Feedback, FeedbackKind
from tests.support.fake_github import FakeGitHub

scenarios("avis.feature")

FEEDBACK_REPOSITORY = "Ghoutibk/la-haut-avis"


@pytest.fixture
def github():
    with FakeGitHub() as fake:
        yield fake


@given("une boîte à avis privée sur GitHub", target_fixture="send_feedback")
def a_private_feedback_inbox(github):
    return build_send_feedback(FEEDBACK_REPOSITORY, "jeton-de-test", api_url=github.url)


@when(
    parsers.parse("j'envoie le problème « {message} » avec mon e-mail {contact}"),
    target_fixture="sent",
)
def send_a_problem(send_feedback, message, contact):
    feedback = Feedback(FeedbackKind.PROBLEM, message, contact)
    send_feedback.execute(feedback)
    return feedback


@when(parsers.parse("j'envoie l'idée « {message} »"), target_fixture="sent")
def send_an_idea(send_feedback, message):
    feedback = Feedback(FeedbackKind.IDEA, message)
    send_feedback.execute(feedback)
    return feedback


@then(
    parsers.parse(
        "un ticket « {label} » arrive dans la boîte à avis, avec mon message et mon e-mail"
    )
)
def an_issue_with_the_message_and_the_contact(github, sent, label):
    [issue] = github.issues
    assert issue["labels"] == [label]
    assert sent.message in issue["body"]
    assert sent.contact in issue["body"]


@then(
    parsers.parse(
        "un ticket « {label} » arrive dans la boîte à avis, avec mon message et sans e-mail"
    )
)
def an_issue_with_the_message_only(github, sent, label):
    [issue] = github.issues
    assert issue["labels"] == [label]
    assert sent.message in issue["body"]
    assert "@" not in issue["body"]
