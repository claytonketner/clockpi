import math
import serial
from time import sleep

from constants import NUM_LEDS
from constants import OFF
from constants import ON
from constants import STARTUP_WAIT


CHUNK_SIZE = 60


def wait_for_ping(arduino, startup=False):
    if startup:
        sleep(STARTUP_WAIT)
    arduino.read_until(terminator='p', size=None)


def connect_to_arduino():
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    arduino.flush()
    arduino.reset_output_buffer()
    wait_for_ping(arduino, True)
    return arduino


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


def send_data(arduino, data, chunk_size=CHUNK_SIZE):
    """Sends data to the arduino.
    `data` should be a 640 char string consisting of ON's and OFF's
    The data is sent to the arduino in chunks of size `chunk_size`
    """
    assert len(data) == NUM_LEDS
    arduino.write('sp')
    wait_for_ping(arduino)
    for ii in xrange(int(math.ceil(len(data)/float(CHUNK_SIZE)))):
        chunk_end_index = CHUNK_SIZE*(ii+1)
        if chunk_end_index > len(data):
            chunk_end_index = len(data)
        arduino.write(data[CHUNK_SIZE*ii:chunk_end_index])
        arduino.write('p')
        wait_for_ping(arduino)
