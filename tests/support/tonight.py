"""Ce que « Ce soir » annonce, lu comme le visiteur le lit."""

# Un Starlink seul garde son nom de catalogue ; une file devient « Train Starlink (N satellites) ».
STARLINK_NAMES = ("STARLINK-", "Train Starlink")


def is_a_starlink_announcement(name: str) -> bool:
    return name.startswith(STARLINK_NAMES)
