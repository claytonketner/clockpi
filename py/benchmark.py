import datetime

import alphanum
from constants import NUM_LEDS
from constants import ON
from graphics import add_to_matrix
from graphics import generate_empty_matrix
from graphics import matrix_to_command
from utils import send_data
from utils import wait_for_ping


def test_ping(arduino, iterations):
    total = datetime.timedelta(seconds=0)
    pings = []
    for ii in range(iterations):
        start = datetime.datetime.now()
        arduino.write('p')
        wait_for_ping(arduino)
        end = datetime.datetime.now()
        diff = end - start
        pings.append(diff)
        total += diff
    print "Ping stats:\n\tmin: {}\n\tmax: {}\n\tavg: {}".format(
        min(pings), max(pings), total/iterations)


def test_speed(arduino):
    start = datetime.datetime.now()
    arduino.write('s')
    data = ON*NUM_LEDS
    send_data(arduino, data)
    elapsed_time = datetime.datetime.now() - start
    arduino.write('rp')
    wait_for_ping(arduino)
    return elapsed_time


def benchmark(arduino):
    start = datetime.datetime.now()
    matrix = generate_empty_matrix(1)
    send_data(arduino, matrix_to_command(matrix))

    matrix = generate_empty_matrix()
    add_to_matrix(alphanum.ZERO, matrix, 0, 0)
    add_to_matrix(alphanum.ONE, matrix, 8, 0)
    add_to_matrix(alphanum.TWO, matrix, 16, 0)
    add_to_matrix(alphanum.THREE, matrix, 24, 0)
    add_to_matrix(alphanum.FOUR, matrix, 32, 0)
    send_data(arduino, matrix_to_command(matrix))

    matrix = generate_empty_matrix()
    add_to_matrix(alphanum.FIVE, matrix, 0, 0)
    add_to_matrix(alphanum.SIX, matrix, 8, 0)
    add_to_matrix(alphanum.SEVEN, matrix, 16, 0)
    add_to_matrix(alphanum.EIGHT, matrix, 24, 0)
    add_to_matrix(alphanum.NINE, matrix, 32, 0)
    send_data(arduino, matrix_to_command(matrix))
    finish = datetime.datetime.now()
    elapsed_time = finish - start
    print "Benchmark time: {}".format(elapsed_time)
    print "Approx time/LED: {}".format(elapsed_time/(640*3))


def cycle_time_benchmark(arduino, num_cycles=100):
    start = datetime.datetime.now()
    for _ in range(num_cycles/len(alphanum.NUMBERS)):
        for number in alphanum.NUMBERS:
            matrix = generate_empty_matrix(0)
            add_to_matrix(number, matrix, 0, 0)
            add_to_matrix(number, matrix, 8, 0)
            add_to_matrix(number, matrix, 16, 0)
            add_to_matrix(number, matrix, 24, 0)
            add_to_matrix(number, matrix, 32, 0)
            send_data(arduino, matrix_to_command(matrix))

    finish = datetime.datetime.now()
    elapsed_time = finish - start
    print "Time/cycle: {}".format(elapsed_time/num_cycles)
