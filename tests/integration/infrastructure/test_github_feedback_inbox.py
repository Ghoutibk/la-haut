import logging

import pytest

from la_haut.application.ports import FeedbackNotConfiguredError, FeedbackUnavailableError
from la_haut.domain.feedback import Feedback, FeedbackKind
from la_haut.infrastructure.github_feedback_inbox import (
    GitHubIssuesFeedbackInbox,
    UnconfiguredFeedbackInbox,
)
from tests.support.builders import DEFAULT_INSTANT
from tests.support.fake_github import FakeGitHub

REPOSITORY = "Ghoutibk/la-haut-avis"
TOKEN = "jeton-de-test"
A_PROBLEM = Feedback(
    FeedbackKind.PROBLEM, "La boussole ne bouge pas sur mon Android", "claire@example.org"
)


@pytest.fixture
def github():
    with FakeGitHub() as fake:
        yield fake


def deliver(github, feedback=A_PROBLEM):
    GitHubIssuesFeedbackInbox(REPOSITORY, TOKEN, api_url=github.url).deliver(
        feedback, DEFAULT_INSTANT
    )
    [issue] = github.issues
    return issue


def test_the_feedback_becomes_an_issue_of_the_private_repository_with_the_token(github):
    deliver(github)

    [request] = github.requests
    assert request["path"] == "/repos/Ghoutibk/la-haut-avis/issues"
    assert request["headers"]["Authorization"] == "Bearer jeton-de-test"
    assert request["headers"]["Accept"] == "application/vnd.github+json"


@pytest.mark.parametrize(
    "kind, label, title",
    [
        (FeedbackKind.PROBLEM, "problème", "Problème : Rien ne s'affiche"),
        (FeedbackKind.IDEA, "idée", "Idée : Rien ne s'affiche"),
        (FeedbackKind.OTHER, "autre", "Autre : Rien ne s'affiche"),
    ],
)
def test_the_issue_is_labelled_and_titled_by_the_kind_of_feedback(github, kind, label, title):
    issue = deliver(github, Feedback(kind, "Rien ne s'affiche\nsur mon téléphone"))

    assert (issue["labels"], issue["title"]) == ([label], title)


def test_a_long_first_line_is_cut_in_the_title(github):
    issue = deliver(github, Feedback(FeedbackKind.IDEA, "a" * 200))

    assert issue["title"] == "Idée : " + "a" * 69 + "…"


def test_the_message_stays_in_a_code_block_so_that_mentions_notify_nobody(github):
    issue = deliver(github, Feedback(FeedbackKind.OTHER, "Bonjour @quelquun ```"))

    assert "````text\nBonjour @quelquun ```\n````" in issue["body"]


def test_the_issue_tells_the_contact_and_when_it_was_sent(github):
    body = deliver(github)["body"]

    assert "Contact : `claire@example.org`" in body
    assert "Envoyé depuis Là-haut le 05/10/2026 à 19:42 UTC" in body


def test_the_issue_says_so_when_no_contact_was_left(github):
    body = deliver(github, Feedback(FeedbackKind.IDEA, "Merci"))["body"]

    assert "Contact : aucun e-mail laissé" in body


def test_a_refusal_from_github_makes_the_inbox_unavailable_and_is_logged(github, caplog):
    github.fails_with(401)

    with caplog.at_level(logging.WARNING), pytest.raises(FeedbackUnavailableError):
        deliver(github)

    [record] = caplog.records
    assert "401" in record.getMessage()
    assert TOKEN not in record.getMessage()


def test_an_unreachable_github_makes_the_inbox_unavailable():
    inbox = GitHubIssuesFeedbackInbox(REPOSITORY, TOKEN, api_url="http://127.0.0.1:9")

    with pytest.raises(FeedbackUnavailableError):
        inbox.deliver(A_PROBLEM, DEFAULT_INSTANT)


def test_an_inbox_without_repository_or_token_says_it_is_not_configured():
    with pytest.raises(FeedbackNotConfiguredError):
        UnconfiguredFeedbackInbox().deliver(A_PROBLEM, DEFAULT_INSTANT)
