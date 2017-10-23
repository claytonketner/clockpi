from datetime import datetime

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.external import get_traffic
from clockpi.external import get_weather_temps


def generate_empty_matrix(fill_with=0):
    # TODO save this somewhere for faster re-use?
    """Generates a matrix of zeros that can be referenced like:
        my_matrix[x_coordinate][y_coordinate]
    """
    empty_matrix = []
    for _ in xrange(ARRAY_WIDTH):
        empty_matrix.append([fill_with]*ARRAY_HEIGHT)
    return empty_matrix


def add_to_matrix(partial_matrix, matrix, x, y, transpose=True,
                  bit_or=True, bit_and=False, bit_xor=False):
    if transpose:
        partial_matrix_x_len = len(partial_matrix[0])
        partial_matrix_y_len = len(partial_matrix)
    else:
        partial_matrix_x_len = len(partial_matrix)
        partial_matrix_y_len = len(partial_matrix[0])
    for xx in range(partial_matrix_x_len):
        for yy in range(partial_matrix_y_len):
            is_inside = (len(matrix) > (x+xx) and (x+xx) >= 0 and
                         len(matrix[0]) > (y+yy) and (y+yy) >= 0)
            if is_inside:
                matrix_bit = matrix[x+xx][y+yy]
                if transpose:
                    partial_matrix_bit = partial_matrix[yy][xx]
                else:
                    partial_matrix_bit = partial_matrix[xx][yy]
                if bit_and:
                    result_bit = matrix_bit and partial_matrix_bit
                elif bit_xor:
                    result_bit = matrix_bit ^ partial_matrix_bit
                else:
                    result_bit = (bit_or and matrix_bit) or partial_matrix_bit
                matrix[x+xx][y+yy] = result_bit


def add_items_to_matrix(items, matrix, origin_x, origin_y, spacing, **kwargs):
    """Adds a left-aligned 'sentence', which consists of `items`, which are
    separated by `spacing`, which can be an integer, or a list containing
    spacing distances between each item in `items`
    """
    x = origin_x
    for ii in range(len(items)):
        item = items[ii]
        if ii > 0:
            space = spacing
            if hasattr(spacing, '__iter__'):
                space = spacing[ii-1]
            x += space + len(items[ii-1][0])
        add_to_matrix(item, matrix, x, origin_y, **kwargs)


def update_clock_info(clock_info):
    now = datetime.now()
    second = now.second
    if clock_info.get('last_second') == second:
        # Don't update if it won't change the clockface
        return False
    clock_info['last_second'] = second
    # Time
    minute = now.minute
    hour_24 = now.hour
    hour_12 = hour_24 % 12
    if hour_24 == 0:
        hour_12 = 12
    clock_info['hour_digits'] = map(int, [hour_12 / 10, hour_12 % 10])
    clock_info['minute_digits'] = map(int, [minute / 10, minute % 10])
    clock_info['second_digits'] = map(int, [second / 10, second % 10])
    # Weather
    clock_info['weather_update_time'], clock_info['weather'] = (
        get_weather_temps(clock_info.setdefault('weather_update_time', now),
                          clock_info.get('weather', {})))
    if clock_info.get('weather'):
        clock_info['temp_digits'] = map(
            int, [clock_info['weather']['current_temp'] / 10,
                  clock_info['weather']['current_temp'] % 10])
        clock_info['sun_is_up'] = (clock_info['weather']['sunrise'] < now and
                                   clock_info['weather']['sunset'] > now)
    else:
        # Default to False because the bright clockface is annoying at night
        clock_info['sun_is_up'] = False
    # Traffic
    clock_info['traffic_update_time'], clock_info['traffic'] = get_traffic(
        clock_info.setdefault('traffic_update_time', now),
        clock_info.get('traffic', {}))
    return True


def digit_to_graphic(digit_list, alphanum_source):
    # Converts a list of numbers to a list of alphanum arrays
    alphanum_list = []
    for digit in digit_list:
        alphanum_list.append(alphanum_source[digit])
    return alphanum_list
