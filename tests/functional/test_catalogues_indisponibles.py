import re

from pytest_bdd import given, parsers, scenarios, then

from la_haut.composition import RECENT_LAUNCHES_GROUP
from tests.support.cache import THREE_HOURS_S, a_cache_written
from tests.support.fixtures import LAST_30_DAYS_CSV_2026, VISUAL_CSV_2026

scenarios("catalogues_indisponibles.feature")


def _cuts_off_the_catalogs(celestrak):
    celestrak.publishes(*VISUAL_CSV_2026.splitlines())
    celestrak.cuts_off_its_answers()


# Ce que la source des catalogues peut répondre de travers.
FAILURES = {
    "répond une erreur 503": lambda celestrak: celestrak.fails_with(503),
    "répond une page web au lieu du catalogue": lambda celestrak: celestrak.publishes_a_web_page(),
    "envoie un catalogue coupé au milieu d'une ligne": lambda celestrak: (
        celestrak.publishes_cut_short(VISUAL_CSV_2026)
    ),
    "interrompt sa réponse en cours de route": _cuts_off_the_catalogs,
}


@given("Là-haut a gardé les catalogues du 6 octobre 2026, téléchargés il y a trois heures")
def catalogs_kept_from_three_hours_ago(cache_path):
    a_cache_written(cache_path, VISUAL_CSV_2026, seconds_ago=THREE_HOURS_S)
    a_cache_written(
        cache_path.with_name(f"{RECENT_LAUNCHES_GROUP}.csv"),
        LAST_30_DAYS_CSV_2026,
        seconds_ago=THREE_HOURS_S,
    )


@given(parsers.re("CelesTrak (?P<failure>" + "|".join(map(re.escape, FAILURES)) + ")"))
def celestrak_answers_badly(celestrak, failure):
    FAILURES[failure](celestrak)


@given(parsers.parse("le groupe « {group} » est injoignable"))
def an_unreachable_group(celestrak, group):
    celestrak.fails_with(503, group=group)


@then(parsers.parse("« Ce soir » répond « {message} »"))
def tonight_answers(tonight, message):
    assert tonight.is_server_error
    assert tonight.json()["detail"] == message


@then("« Ce soir » n'annonce aucun Starlink")
def no_starlink_is_announced(tonight):
    names = [announced["name"] for announced in tonight.json()["passes"]]

    assert [name for name in names if "starlink" in name.lower()] == []
