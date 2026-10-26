from pytest_bdd import given, parsers, scenarios, then, when

from tests.support.visit import (
    ANDROID,
    ANDROID_WITHOUT_ABSOLUTE_EVENT,
    COMPUTER,
    PHONE_WITHOUT_COMPASS,
    an_iphone,
)

scenarios("page/viser.feature")

DEVICES = {
    "sur un ordinateur": COMPUTER,
    "sur un téléphone sans boussole": PHONE_WITHOUT_COMPASS,
    "sur un téléphone Android": ANDROID,
    "sur un téléphone Android sans orientation absolue": ANDROID_WITHOUT_ABSOLUTE_EVENT,
    "sur un iPhone, et que j'autorise l'accès à la boussole": an_iphone("granted"),
    "sur un iPhone, et que je refuse l'accès à la boussole": an_iphone("denied"),
    "sur un iPhone, et que la demande d'accès à la boussole échoue": an_iphone("fails"),
}


@given(parsers.parse("je visite Là-haut {device}"))
def i_visit_la_haut_on(visit, device):
    visit.device = DEVICES[device]


@when(parsers.parse("mon téléphone pointe vers {heading:g}°"))
def my_phone_points_to(visit, heading):
    visit.points_phone_to(heading)


@when("ma boussole ne sait pas où est le nord")
def my_compass_does_not_know_the_north(visit):
    visit.points_phone_to(None)


def _permission_requests(page):
    return page.evaluate("window.compassPermissionRequests")


@then("mon iPhone ne m'a pas encore demandé l'accès à la boussole")
def no_compass_access_was_asked_yet(page):
    assert _permission_requests(page) == 0


@then("mon iPhone m'a demandé l'accès à la boussole")
def compass_access_was_asked(page):
    assert _permission_requests(page) == 1
