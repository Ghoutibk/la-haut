from pytest_bdd import given, parsers, scenarios, then, when

scenarios("page/animations.feature")

# Le temps que l'effet du doigt, s'il y en a un, aille à son terme.
PRESS_SETTLING_MS = 300


def _button(page, name):
    return page.get_by_role("button", name=name, exact=True)


@given("je n'ai pas de préférence pour les animations")
def no_motion_preference(visit):
    visit.reduces_motion = False


@given("je préfère réduire les animations")
def i_prefer_reduced_motion(visit):
    visit.reduces_motion = True


@when(parsers.parse("j'appuie sans relâcher sur « {name} »"), target_fixture="width_at_rest")
def i_press_and_hold(page, name):
    button = _button(page, name)
    width_at_rest = button.bounding_box()["width"]
    button.hover()
    page.mouse.down()
    page.wait_for_timeout(PRESS_SETTLING_MS)
    return width_at_rest


@then(parsers.parse("le bouton « {name} » rapetisse"))
def the_button_shrinks(page, name, width_at_rest):
    assert _button(page, name).bounding_box()["width"] < width_at_rest


@then(parsers.parse("le bouton « {name} » garde sa taille"))
def the_button_keeps_its_size(page, name, width_at_rest):
    assert _button(page, name).bounding_box()["width"] == width_at_rest
