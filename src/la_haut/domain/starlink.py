STARLINK_NAME_PREFIX = "STARLINK"


def is_starlink(satellite_name: str) -> bool:
    """Un satellite de la constellation Starlink, que CelesTrak nomme STARLINK-<numéro>."""
    return satellite_name.startswith(STARLINK_NAME_PREFIX)
