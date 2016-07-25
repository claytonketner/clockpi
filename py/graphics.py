import datetime

import alphanum
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


def display_clock(arduino):
    while(True):
        now = datetime.datetime.now()
        hour = now.hour
        if hour == 0:
            hour = 12
        if hour > 12:
            hour = hour % 12
        minute = now.minute
        matrix = generate_empty_matrix()
        add_to_matrix(alphanum.NUMBERS[hour / 10], matrix, 0, 0)
        add_to_matrix(alphanum.NUMBERS[hour % 10], matrix, 8, 0)
        add_to_matrix(alphanum.SEPARATOR, matrix, 16, 0)
        add_to_matrix(alphanum.NUMBERS[minute / 10], matrix, 24, 0)
        add_to_matrix(alphanum.NUMBERS[minute % 10], matrix, 32, 0)
        send_data(arduino, matrix_to_command(matrix))
