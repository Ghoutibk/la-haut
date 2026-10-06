from la_haut.application.ports import CatalogUnavailableError, SatelliteCatalog
from la_haut.domain.satellite import Satellite


class CombinedSatelliteCatalog:
    """SatelliteCatalog qui réunit plusieurs catalogues, chaque numéro NORAD une seule fois.

    Un catalogue indisponible n'empêche pas d'annoncer les satellites des autres.
    """

    def __init__(self, *catalogs: SatelliteCatalog) -> None:
        self._catalogs = catalogs

    def tracked_satellites(self) -> list[Satellite]:
        by_norad_id: dict[int, Satellite] = {}
        answered = False
        for catalog in self._catalogs:
            try:
                satellites = catalog.tracked_satellites()
            except CatalogUnavailableError:
                continue
            answered = True
            for satellite in satellites:
                by_norad_id.setdefault(satellite.norad_id, satellite)
        if not answered:
            raise CatalogUnavailableError("Aucun catalogue de satellites disponible")
        return list(by_norad_id.values())
