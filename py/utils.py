import datetime
import serial
from time import sleep

from constants import STARTUP_WAIT
from constants import OFF
from constants import ON
from constants import NUM_LEDS


CHUNK_SIZE = 40  # Optimal is 60 TODO


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
    print "Ping stats:\n\tmin: {}\n\tmax: {}\n\tavg: {}".format(min(pings), max(pings), total/iterations)


def send_data(arduino, data, chunk_size=CHUNK_SIZE):
    """Sends data to the arduino.
    `data` should be a 640 char string consisting of ON's and OFF's
    `chunk_size` should evenly divide the length of `data`
    The data is sent to the arduino in chunks of size `chunk_size`
    """
    assert len(data) == NUM_LEDS
    arduino.write('sp')
    wait_for_ping(arduino)
    for ii in xrange(len(data)/CHUNK_SIZE):
        arduino.write(data[CHUNK_SIZE*ii:CHUNK_SIZE*(ii+1)] + 'p')
        wait_for_ping(arduino)


def test_speed(arduino):
    start = datetime.datetime.now()
    arduino.write('s')
    for _ in xrange(10):
        arduino.write(ON*60 + 'p')
        wait_for_ping(arduino)
    arduino.write('\x01'*40)
    print (datetime.datetime.now() - start)
    arduino.write('rp')
    wait_for_ping(arduino)
