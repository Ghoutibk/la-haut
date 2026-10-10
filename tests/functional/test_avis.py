import json

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.composition import (
    FEEDBACK_REPOSITORY_SETTING,
    FEEDBACK_TOKEN_SETTING,
    build_web_app,
)
from tests.support.fake_github import FakeGitHub

scenarios("avis.feature")

FEEDBACK_REPOSITORY = "Ghoutibk/la-haut-avis"


@pytest.fixture
def github():
    with FakeGitHub() as fake:
        yield fake


@pytest.fixture
def site(celestrak, cache_path, github):
    """Le site assemblé comme en ligne, avec les réglages d'avis donnés par le scénario."""
    return TestClient(
        build_web_app(cache_path, url_template=celestrak.url_template, feedback_api_url=github.url)
    )


@given("une boîte à avis privée sur GitHub")
def a_private_feedback_inbox(monkeypatch):
    monkeypatch.setenv(FEEDBACK_REPOSITORY_SETTING, FEEDBACK_REPOSITORY)
    monkeypatch.setenv(FEEDBACK_TOKEN_SETTING, "jeton-de-test")


def send(site, kind, message, contact=None):
    """L'avis tel que la page l'envoie : sa nature, le message et l'e-mail facultatif."""
    return site.post("/api/feedback", json={"kind": kind, "message": message, "contact": contact})


@when(
    parsers.parse("j'envoie le problème « {message} » avec mon e-mail {contact}"),
    target_fixture="answer",
)
def send_a_problem(site, message, contact):
    return send(site, "problem", message, contact)


@when("j'envoie un problème sans message", target_fixture="answer")
def send_a_problem_without_message(site):
    return send(site, "problem", "")


@when(parsers.parse("j'envoie un problème de {length:d} caractères"), target_fixture="answer")
def send_a_long_problem(site, length):
    return send(site, "problem", "a" * length)


@when(parsers.parse("j'envoie l'idée « {message} »"), target_fixture="answer")
def send_an_idea(site, message):
    return send(site, "idea", message)


@then(
    parsers.parse(
        "un ticket « {label} » arrive dans la boîte à avis, avec mon message et mon e-mail"
    )
)
def an_issue_with_the_message_and_the_contact(github, answer, label):
    sent = json.loads(answer.request.content)
    [issue] = github.issues
    assert issue["labels"] == [label]
    assert sent["message"] in issue["body"]
    assert sent["contact"] in issue["body"]


@then(
    parsers.parse(
        "un ticket « {label} » arrive dans la boîte à avis, avec mon message et sans e-mail"
    )
)
def an_issue_with_the_message_only(github, answer, label):
    sent = json.loads(answer.request.content)
    [issue] = github.issues
    assert issue["labels"] == [label]
    assert sent["message"] in issue["body"]
    assert "@" not in issue["body"]


@then(parsers.parse("mon avis est refusé : « {reason} »"))
def my_feedback_is_refused(answer, reason):
    assert answer.is_client_error
    assert answer.json()["detail"] == reason


@then("aucun ticket n'arrive dans la boîte à avis")
def no_issue_arrives(github):
    assert github.issues == []
