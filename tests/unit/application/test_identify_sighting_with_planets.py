from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.identify_sighting_with_planets import IdentifySightingWithPlanets
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.identification import Identification
from la_haut.domain.planet import Planet
from la_haut.domain.sighting import Sighting
from tests.support.builders import (
    DEFAULT_INSTANT,
    ONE_MINUTE,
    a_planet_position,
    a_satellite,
    a_track,
    an_observer_in_paris,
)
from tests.support.fakes import (
    FakePlanetLocator,
    FakeSatelliteCatalog,
    FakeSkyTracker,
    UnavailableSatelliteCatalog,
)

SEEN_IN_THE_WEST = Sighting(at=DEFAULT_INSTANT + ONE_MINUTE, direction=CompassPoint.WEST)
WEST = {"azimuth_deg": 270.0}


def identify(planets, tracks_by_name=None, locator=None, catalog=None):
    tracks_by_name = tracks_by_name or {}
    satellites = [a_satellite(name) for name in tracks_by_name]
    list_visible_passes = ListVisiblePasses(
        catalog=catalog or FakeSatelliteCatalog(satellites), tracker=FakeSkyTracker(tracks_by_name)
    )
    use_case = IdentifySightingWithPlanets(
        IdentifySighting(list_visible_passes), locator or FakePlanetLocator(planets)
    )
    return use_case.execute(an_observer_in_paris(), SEEN_IN_THE_WEST)


def test_a_planet_in_that_direction_is_identified_when_no_satellite_was_there():
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=275.0)

    assert identify([venus]).candidates == (venus,)


def test_a_planet_elsewhere_is_not_identified():
    assert identify([a_planet_position(planet=Planet.MARS, azimuth_deg=90.0)]).candidates == ()


def test_satellites_come_before_planets():
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=270.0)

    candidates = identify([venus], {"ISS (ZARYA)": a_track(WEST, WEST, WEST)}).candidates

    assert [getattr(c, "satellite_name", None) for c in candidates] == ["ISS (ZARYA)", None]
    assert candidates[1] == venus


def test_planets_come_from_the_closest_to_the_furthest_from_the_given_direction():
    saturn = a_planet_position(planet=Planet.SATURN, azimuth_deg=268.0)
    jupiter = a_planet_position(planet=Planet.JUPITER, azimuth_deg=300.0)
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=245.0)

    assert identify([venus, jupiter, saturn]).candidates == (saturn, venus, jupiter)


def test_every_planet_is_located_for_the_observer_at_the_moment_of_the_sighting():
    locator = FakePlanetLocator([])

    identify([], locator=locator)

    assert locator.requests == [
        (planet, an_observer_in_paris(), SEEN_IN_THE_WEST.at) for planet in Planet
    ]


def test_the_satellites_are_checked_when_their_catalog_is_available():
    assert identify([]).satellites_checked


def test_without_a_satellite_catalog_the_planets_still_answer_and_say_so():
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=275.0)

    identification = identify([venus], catalog=UnavailableSatelliteCatalog())

    assert identification == Identification(candidates=(venus,), satellites_checked=False)
