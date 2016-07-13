import datetime

import utils
import alphanum
from constants import OFF
from constants import ON


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


def matrix_to_command(matrix):
    command_str = ""
    for array in range(10):
        array_x = array % 5
        array_y = 0
        if array >= 5:
            array_y = 1
        for led_row in range(8):
            for led_col in range(8):
                matrix_row = 8*2 - array_y*8 - led_row - 1
                matrix_col = array_x*8 + 8 - led_col - 1
                if matrix[matrix_col][matrix_row]:
                    command_str += ON
                else:
                    command_str += OFF
    return command_str


def display_clock(arduino):
    while(True):
        now = datetime.datetime.now()
        hour = now.hour
        if hour > 12:
            hour = hour % 12
        minute = now.minute
        matrix = generate_empty_matrix()
        add_to_matrix(alphanum.NUMBERS[hour / 10], matrix, 0, 0)
        add_to_matrix(alphanum.NUMBERS[hour % 10], matrix, 8, 0)
        add_to_matrix(alphanum.SEPARATOR, matrix, 16, 0)
        add_to_matrix(alphanum.NUMBERS[minute / 10], matrix, 24, 0)
        add_to_matrix(alphanum.NUMBERS[minute % 10], matrix, 32, 0)
        utils.send_data(arduino, matrix_to_command(matrix))


def benchmark(arduino):
    start = datetime.datetime.now()
    matrix = generate_empty_matrix(1)
    utils.send_data(arduino, matrix_to_command(matrix))

    matrix = generate_empty_matrix()
    add_to_matrix(alphanum.ZERO, matrix, 0, 0)
    add_to_matrix(alphanum.ONE, matrix, 8, 0)
    add_to_matrix(alphanum.TWO, matrix, 16, 0)
    add_to_matrix(alphanum.THREE, matrix, 24, 0)
    add_to_matrix(alphanum.FOUR, matrix, 32, 0)
    utils.send_data(arduino, matrix_to_command(matrix))

    matrix = generate_empty_matrix()
    add_to_matrix(alphanum.FIVE, matrix, 0, 0)
    add_to_matrix(alphanum.SIX, matrix, 8, 0)
    add_to_matrix(alphanum.SEVEN, matrix, 16, 0)
    add_to_matrix(alphanum.EIGHT, matrix, 24, 0)
    add_to_matrix(alphanum.NINE, matrix, 32, 0)
    utils.send_data(arduino, matrix_to_command(matrix))
    finish = datetime.datetime.now()
    elapsed_time = finish - start
    print "Benchmark time: {}".format(elapsed_time)
    print "Approx time/LED: {}".format(elapsed_time/(640*3))
