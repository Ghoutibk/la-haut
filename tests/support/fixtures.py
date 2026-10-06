"""Données réelles partagées par toutes les familles de tests (DRY)."""

from datetime import UTC, datetime
from pathlib import Path

# TLE réel de l'ISS (époque 2018-07-03), repris de la suite de tests de Skyfield.
ISS_NAME = "ISS (ZARYA)"
ISS_TLE_LINE_1 = "1 25544U 98067A   18184.80969102  .00001614  00000-0  31745-4 0  9993"
ISS_TLE_LINE_2 = "2 25544  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106"
ISS_TLE_EPOCH = datetime(2018, 7, 3, 19, 25, 57, tzinfo=UTC)

# Un vaisseau amarré partage l'orbite de la station : mêmes éléments, autre numéro de catalogue.
DOCKED_VEHICLE_NAME = "VAISSEAU AMARRÉ"
DOCKED_VEHICLE_TLE_LINE_1 = "1 43508U 98067A   18184.80969102  .00001614  00000-0  31745-4 0  9993"
DOCKED_VEHICLE_TLE_LINE_2 = "2 43508  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106"

PARIS_LATITUDE_DEG = 48.8566
PARIS_LONGITUDE_DEG = 2.3522

# Éléments réels publiés par CelesTrak (groupe « visual ») le 5 octobre 2026.
TIANGONG_NAME = "CSS (TIANHE)"
TIANGONG_TLE_LINE_1 = "1 48274U 21035A   26278.26053918  .00022931  00000+0  27545-3 0  9997"
TIANGONG_TLE_LINE_2 = "2 48274  41.4701  13.5304 0001708 334.1337  25.9416 15.60329241310352"
HUBBLE_NAME = "HST"
HUBBLE_TLE_LINE_1 = "1 20580U 90037B   26276.71991929  .00004347  00000+0  13013-3 0  9992"
HUBBLE_TLE_LINE_2 = "2 20580  28.4729  58.1679 0001270 285.6016  74.4440 15.31815463805220"
ROCKET_BODY_NAME = "SL-16 R/B"
ROCKET_BODY_TLE_LINE_1 = "1 16182U 85097B   26277.86702633 -.00000011  00000+0  18308-4 0  9992"
ROCKET_BODY_TLE_LINE_2 = "2 16182  71.0030  60.1639 0009676 291.7986 179.8193 14.16623856116857"

# Trois Starlink FABRIQUÉS pour les tests : un même lancement (désignation 18999, pièces A, B, C)
# sur l'orbite de l'ISS du 3 juillet 2018, chacun 1° d'anomalie moyenne derrière le précédent,
# soit une quinzaine de secondes. Sommes de contrôle recalculées. Avec Skyfield
# (find_events, seuil 10°), ils passent sur Paris le 4 juillet 2018 de 02:54:10 à 02:58:28 UTC.
STARLINK_TRAIN_LAUNCH = "18999"
STARLINK_TRAIN = (
    (
        "STARLINK-90001",
        "1 90001U 18999A   18184.80969102  .00001614  00000-0  31745-4 0  9999",
        "2 90001  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106",
    ),
    (
        "STARLINK-90002",
        "1 90002U 18999B   18184.80969102  .00001614  00000-0  31745-4 0  9990",
        "2 90002  51.6414 295.8524 0003435 262.6267 203.2868 15.54005638121106",
    ),
    (
        "STARLINK-90003",
        "1 90003U 18999C   18184.80969102  .00001614  00000-0  31745-4 0  9991",
        "2 90003  51.6414 295.8524 0003435 262.6267 202.2868 15.54005638121106",
    ),
)

# Éléments réels de l'ISS publiés par CelesTrak le 6 octobre 2026 (groupe « visual »), téléchargés
# coup sur coup dans les deux formats : le même jeu d'éléments, en TLE et en OMM (CSV). L'OMM
# garde un chiffre de plus sur l'excentricité et le BSTAR.
ISS_2026_TLE_LINE_1 = "1 25544U 98067A   26279.53064673  .00004741  00000+0  94937-4 0  9991"
ISS_2026_TLE_LINE_2 = "2 25544  51.6312 109.0734 0006869 229.7980 130.2407 15.48752789589016"
ISS_2026_EPOCH = datetime(2026, 10, 6, 12, 44, 7, 877472, tzinfo=UTC)
ISS_2026_OMM = {
    "OBJECT_NAME": "ISS (ZARYA)",
    "OBJECT_ID": "1998-067A",
    "EPOCH": "2026-10-06T12:44:07.877472",
    "MEAN_MOTION": "15.48752789",
    "ECCENTRICITY": ".00068694",
    "INCLINATION": "51.6312",
    "RA_OF_ASC_NODE": "109.0734",
    "ARG_OF_PERICENTER": "229.7980",
    "MEAN_ANOMALY": "130.2407",
    "EPHEMERIS_TYPE": "0",
    "CLASSIFICATION_TYPE": "U",
    "NORAD_CAT_ID": "25544",
    "ELEMENT_SET_NO": "999",
    "REV_AT_EPOCH": "58901",
    "BSTAR": ".94937468E-4",
    "MEAN_MOTION_DOT": ".4741E-4",
    "MEAN_MOTION_DDOT": "0",
}

# Les vrais catalogues CelesTrak du 6 octobre 2026 vers 20 h UTC, au format OMM (CSV) : groupes
# « visual » et « last-30-days ». Les objets lancés depuis mi-2026 ont des numéros NORAD au-delà
# de 99999 ; CelesTrak ne les publie plus en TLE.
CELESTRAK_DIR = Path(__file__).parent / "celestrak"
VISUAL_CSV_2026 = (CELESTRAK_DIR / "visual-2026-10-06.csv").read_text("utf-8")
LAST_30_DAYS_CSV_2026 = (CELESTRAK_DIR / "last-30-days-2026-10-06.csv").read_text("utf-8")
