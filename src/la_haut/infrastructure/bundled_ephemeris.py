from functools import cache

from skyfield.api import Loader
from skyfield.jpllib import SpiceKernel
from skyfield.timelib import Timescale
from skyfield_data import get_skyfield_data_path

EPHEMERIS_FILE = "de421.bsp"


@cache
def load_bundled_ephemeris() -> tuple[Timescale, SpiceKernel]:
    """L'échelle de temps et les éphémérides DE421 embarquées, chargées une seule fois."""
    load = Loader(get_skyfield_data_path(), verbose=False)
    return load.timescale(builtin=True), load(EPHEMERIS_FILE)
