import datetime

from alphanum import numbers_large
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


def add_to_matrix(partial_matrix, matrix, x, y, bit_or=True):
    for xx in range(len(partial_matrix[0])):
        for yy in range(len(partial_matrix)):
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
            if type(space) is list:
                space = space[ii]
            x += space + len(items[ii-1][0])
        add_to_matrix(item, matrix, x, origin_y)


def display_clock(arduino):
    number_style = numbers_large
    last_minute = -1
    while(True):
        now = datetime.datetime.now()
        hour = now.hour
        if hour == 0:
            hour = 12
        if hour > 12:
            hour = hour % 12
        minute = now.minute
        if last_minute != minute:
            last_minute = minute
            matrix = generate_empty_matrix()
            clock_time = [
                number_style.ALL[hour / 10],
                number_style.ALL[hour % 10],
                number_style.SEPARATOR,
                number_style.ALL[minute / 10],
                number_style.ALL[minute % 10],
            ]
            add_items_to_matrix(clock_time, matrix, 1, 0, 2)
            send_data(arduino, matrix_to_command(matrix))
