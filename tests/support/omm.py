"""Des TLE de test convertis en catalogue OMM au format CSV de CelesTrak, par sgp4."""

import csv
import io

from sgp4 import exporter
from sgp4.api import Satrec

# Les colonnes des CSV de CelesTrak, dans leur ordre.
CELESTRAK_CSV_COLUMNS = (
    "OBJECT_NAME",
    "OBJECT_ID",
    "EPOCH",
    "MEAN_MOTION",
    "ECCENTRICITY",
    "INCLINATION",
    "RA_OF_ASC_NODE",
    "ARG_OF_PERICENTER",
    "MEAN_ANOMALY",
    "EPHEMERIS_TYPE",
    "CLASSIFICATION_TYPE",
    "NORAD_CAT_ID",
    "ELEMENT_SET_NO",
    "REV_AT_EPOCH",
    "BSTAR",
    "MEAN_MOTION_DOT",
    "MEAN_MOTION_DDOT",
)


def omm_csv_from_tle(*entries: tuple[str, str, str]) -> str:
    """Le catalogue CSV que CelesTrak publierait pour ces TLE (nom, ligne 1, ligne 2)."""
    text = io.StringIO()
    writer = csv.DictWriter(
        text, fieldnames=CELESTRAK_CSV_COLUMNS, extrasaction="ignore", lineterminator="\r\n"
    )
    writer.writeheader()
    for name, line_1, line_2 in entries:
        writer.writerow(exporter.export_omm(Satrec.twoline2rv(line_1, line_2), name))
    return text.getvalue()
