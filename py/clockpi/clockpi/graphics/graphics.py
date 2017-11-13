from clockpi.clockface_config import LARGE_WITH_TEMPERATURE_CONFIG
from clockpi.clockface_config import TRAFFIC_CONFIG
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import config_to_matrix
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.graphics.utils import update_clock_info


def display_clock(clock_info={}):
    """
    N.B.: Uses the fact that the default arg for clock_info can be mutated
    permanently because it's a dictionary. Kinda sketchy...?

    Returns the matrix to be displayed, or None, if the display shouldn't be
    updated.
    """
    if not update_clock_info(clock_info):
        return None
    if clock_info['sun_is_up']:
        matrix = generate_empty_matrix(1)
    else:
        matrix = generate_empty_matrix()
    if clock_info['show_traffic']:
        clockface = config_to_matrix(TRAFFIC_CONFIG, clock_info)
    else:
        clockface = config_to_matrix(LARGE_WITH_TEMPERATURE_CONFIG, clock_info)
    add_to_matrix(clockface, matrix, 0, 0, transpose=False, bit_xor=True)
    return matrix
