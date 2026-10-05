from la_haut.domain.satellite import Satellite

ISS_NORAD_ID = 25544
TIANGONG_NORAD_ID = 48274  # module central Tianhe, auquel le reste de la station est amarré
HUBBLE_NORAD_ID = 20580

FAMOUS_NORAD_IDS = frozenset({ISS_NORAD_ID, TIANGONG_NORAD_ID, HUBBLE_NORAD_ID})


def is_famous(satellite: Satellite) -> bool:
    """Visible et reconnaissable par tous ; reconnu à son numéro NORAD, pas à son nom."""
    return satellite.norad_id in FAMOUS_NORAD_IDS
