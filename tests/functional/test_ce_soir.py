"""Heures de référence calculées avec Skyfield seul, seconde par seconde, sans nos adaptateurs :
au-dessus de 10°, éclairé par le Soleil, Soleil à −6° ou moins. Le 7 octobre 2026 à Paris,
CSS (TIANHE) passe de 06:41:17 à 06:45:11, STARLINK-38375 de 06:16:32 à 06:19:03 et le corps de
fusée H-2A R/B (43682) de 06:41:09 à 06:47:46."""

from pytest_bdd import given, parsers, scenarios, then

from tests.support.fixtures import TIANGONG_NAME, VISUAL_CSV_2026

scenarios("ce_soir.feature")

# Un Starlink seul garde son nom de catalogue ; une file devient « Train Starlink (N satellites) ».
STARLINK_NAMES = ("STARLINK-", "Train Starlink")


@given(parsers.parse("CelesTrak renomme la station chinoise « {new_name} »"))
def celestrak_renames_the_chinese_station(celestrak, new_name):
    renamed = VISUAL_CSV_2026.replace(f"{TIANGONG_NAME},", f"{new_name},")
    celestrak.publishes(*renamed.splitlines(), group="visual")


@then("« Ce soir » n'annonce que la station chinoise et des Starlink")
def only_the_chinese_station_and_starlinks(tonight):
    names = {announced["name"] for announced in tonight.json()["passes"]}

    assert {name for name in names if not name.startswith(STARLINK_NAMES)} == {
        "Station spatiale chinoise Tiangong"
    }
