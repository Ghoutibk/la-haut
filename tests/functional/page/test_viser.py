from pytest_bdd import parsers, scenarios, then, when

scenarios("page/viser.feature")


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
