"""Données réelles partagées par toutes les familles de tests (DRY)."""

from datetime import UTC, datetime

# TLE réel de l'ISS (époque 2018-07-03), repris de la suite de tests de Skyfield.
ISS_NAME = "ISS (ZARYA)"
ISS_TLE_LINE_1 = "1 25544U 98067A   18184.80969102  .00001614  00000-0  31745-4 0  9993"
ISS_TLE_LINE_2 = "2 25544  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106"
ISS_TLE_EPOCH = datetime(2018, 7, 3, 19, 25, 57, tzinfo=UTC)

PARIS_LATITUDE_DEG = 48.8566
PARIS_LONGITUDE_DEG = 2.3522
