from la_haut.application.ports import SatelliteCatalog
from la_haut.domain.satellite import Satellite


class CombinedSatelliteCatalog:
    """SatelliteCatalog qui réunit plusieurs catalogues, chaque numéro NORAD une seule fois."""

    def __init__(self, *catalogs: SatelliteCatalog) -> None:
        self._catalogs = catalogs

    def tracked_satellites(self) -> list[Satellite]:
        by_norad_id: dict[int, Satellite] = {}
        for catalog in self._catalogs:
            for satellite in catalog.tracked_satellites():
                by_norad_id.setdefault(satellite.norad_id, satellite)
        return list(by_norad_id.values())
