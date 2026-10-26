from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then

scenarios("page/ouvrir_la_page.feature")

GOOGLE_FONTS = ("https://fonts.googleapis.com/", "https://fonts.gstatic.com/")


@then(parsers.parse("l'onglet du navigateur s'intitule « {title} »"))
def the_browser_tab_is_titled(page, title):
    expect(page).to_have_title(title)


@then("la page est écrite en français")
def the_page_is_in_french(page):
    expect(page.locator("html")).to_have_attribute("lang", "fr")


@then(parsers.parse("la page se décrit ainsi : « {description} »"))
def the_page_describes_itself(page, description):
    expect(page.locator('meta[name="description"]')).to_have_attribute("content", description)


@then(parsers.parse("la barre du navigateur prend la couleur de la nuit, {color}"))
def the_browser_bar_takes_the_night_color(page, color):
    expect(page.locator('meta[name="theme-color"]')).to_have_attribute("content", color)


@then("la page s'étend jusqu'aux bords de l'écran")
def the_page_reaches_the_screen_edges(page):
    viewport = page.locator('meta[name="viewport"]').get_attribute("content")
    assert "viewport-fit=cover" in viewport


def _scripts_and_styles(visit):
    return [
        response
        for response in visit.responses
        if response.request.resource_type in ("script", "stylesheet")
    ]


@then("chaque script et chaque feuille de style vient de Là-haut, sous /static")
def scripts_and_styles_come_from_la_haut(visit, site):
    resources = _scripts_and_styles(visit)
    kinds = {response.request.resource_type for response in resources}

    assert kinds == {"script", "stylesheet"}
    assert [r.url for r in resources if not r.url.startswith(site.url + "/static/")] == []
    assert [r.url for r in resources if r.status != 200] == []


@then("chaque script est servi comme du JavaScript")
def scripts_are_served_as_javascript(visit):
    scripts = [r for r in _scripts_and_styles(visit) if r.request.resource_type == "script"]

    assert scripts
    assert all(r.headers["content-type"].startswith("text/javascript") for r in scripts)


@then("la page demande ses polices à Google Fonts, et rien d'autre hors de Là-haut")
def only_the_fonts_come_from_google(visit):
    assert any(url.startswith(GOOGLE_FONTS[0]) for url in visit.blocked_urls)
    assert [url for url in visit.blocked_urls if not url.startswith(GOOGLE_FONTS)] == []
