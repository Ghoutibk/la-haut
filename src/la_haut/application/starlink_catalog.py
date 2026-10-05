from la_haut.application.ports import SatelliteCatalog
from la_haut.domain.satellite import Satellite
from la_haut.domain.starlink import is_starlink


class StarlinkCatalog:
    """SatelliteCatalog qui ne garde, d'un autre catalogue, que les satellites Starlink."""

    def __init__(self, catalog: SatelliteCatalog) -> None:
        self._catalog = catalog

    def tracked_satellites(self) -> list[Satellite]:
        return [
            satellite
            for satellite in self._catalog.tracked_satellites()
            if is_starlink(satellite.name)
        ]
