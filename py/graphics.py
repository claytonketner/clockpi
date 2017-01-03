from datetime import datetime

from alphanum import letters_tiny
from alphanum import numbers_large
from alphanum import numbers_tiny
from external import get_weather_temps
from utils import matrix_to_command
from utils import send_data


def generate_empty_matrix(fill_with=0):
    # TODO save this somewhere for faster re-use?
    """Generates a matrix of zeros that can be referenced like:
        my_matrix[x_coordinate][y_coordinate]
    """
    empty_matrix = []
    for _ in xrange(8*5):
        empty_matrix.append([fill_with]*8*2)
    return empty_matrix


def add_to_matrix(partial_matrix, matrix, x, y,
                  bit_or=True, bit_and=False, bit_xor=False):
    for xx in range(len(partial_matrix[0])):
        for yy in range(len(partial_matrix)):
            if len(matrix) > (x+xx) and len(matrix[0]) > (y+yy):
                if bit_and:
                    matrix[x+xx][y+yy] = matrix[x+xx][y+yy] \
                        and partial_matrix[yy][xx]
                elif bit_xor:
                    matrix[x+xx][y+yy] = matrix[x+xx][y+yy] \
                        ^ partial_matrix[yy][xx]
                else:
                    matrix[x+xx][y+yy] = (bit_or and matrix[x+xx][y+yy]) \
                        or partial_matrix[yy][xx]


def add_items_to_matrix(items, matrix, origin_x, origin_y, spacing):
    """Adds a left-aligned 'sentence', which consists of `items`, which are
    separated by `spacing`, which can be an integer, or a list containing
    spacing distances between each item in `items`
    """
    x = origin_x
    for ii in range(len(items)):
        item = items[ii]
        if ii > 0:
            space = spacing
            if hasattr(space, '__iter__'):
                space = space[ii-1]
            x += space + len(items[ii-1][0])
        add_to_matrix(item, matrix, x, origin_y)


def display_clock(arduino):
    last_second = None
    last_update_time = datetime.now()
    temps = {}
    while(True):
        now = datetime.now()
        hour = now.hour
        if hour == 0:
            hour = 12
        if hour > 12:
            hour = hour % 12
        minute = now.minute
        second = now.second
        if last_second != second:
            last_second = second
            matrix = generate_empty_matrix()
            # Hours/minutes
            hour_minute_display = [
                numbers_large.ALL[hour / 10],
                numbers_large.ALL[hour % 10],
                numbers_large.SEPARATOR,
                numbers_large.ALL[minute / 10],
                numbers_large.ALL[minute % 10],
            ]
            add_items_to_matrix(hour_minute_display, matrix, 1, 0, 1)
            # Seconds
            seconds_display = [
                numbers_tiny.ALL[second / 10],
                numbers_tiny.ALL[second % 10],
            ]
            add_items_to_matrix(seconds_display, matrix, 32, 10, 1)
            # Weather
            last_update_time, temps = get_weather_temps(last_update_time,
                                                        temps)
            temp_display = []
            if temps.get('current_temp'):
                temp_display = [
                    numbers_tiny.ALL[temps['current_temp'] / 10],
                    numbers_tiny.ALL[temps['current_temp'] % 10],
                ]
            else:
                # Communicate error
                temp_display = [letters_tiny.E, letters_tiny.R]
            add_items_to_matrix(temp_display, matrix, 32, 1, 1)
            send_data(arduino, matrix_to_command(matrix))
