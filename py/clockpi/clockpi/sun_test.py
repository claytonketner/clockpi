from datetime import datetime
from datetime import timedelta
import math

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.graphics.graphics import display_clock
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.utils import send_matrix


def get_sun_matrix(center_x, center_y, radius):
    radius = int(radius)
    matrix = generate_empty_matrix(0)
    for ii in xrange(radius + 1):
        x_t = math.acos(float(ii) / radius)
        edge_y = round(math.sin(x_t) * radius)
        for jj in xrange(int(edge_y) + 1):
            # We only need the top hemisphere (quadrants 1 and 2)
            add_to_matrix([[1]], matrix,
                          int(center_x + ii + 0.5),
                          int(center_y - jj + 0.5))
            add_to_matrix([[1]], matrix,
                          int(center_x - ii + 0.5),
                          int(center_y - jj + 0.5))
    return matrix


def sun_test(arduino):
    sun_start_diameter = 10
    sun_growth = 200
    total_duration = 60
    start = datetime.now()
    end = start + timedelta(seconds=total_duration)
    while datetime.now() < end:
        elapsed_seconds = (datetime.now() - start).total_seconds()
        total_travel = ARRAY_HEIGHT + 8
        percent_done = elapsed_seconds / total_duration
        sun_current_diameter = int(sun_start_diameter / 2 +
                                   percent_done * sun_growth)
        sun_y = (sun_current_diameter / 2 + ARRAY_HEIGHT -
                 (total_travel * percent_done))
        sun_matrix = get_sun_matrix(ARRAY_WIDTH / 2, sun_y,
                                    sun_current_diameter / 2)
        matrix = display_clock()
        if matrix:
            add_to_matrix(sun_matrix, matrix, 0, 0, bit_xor=True,
                          transpose=False)
            send_matrix(arduino, matrix)
