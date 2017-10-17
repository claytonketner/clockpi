from datetime import datetime

from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_tiny
from clockpi.graphics.utils import add_items_to_matrix
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.graphics.utils import update_clock_info


def display_clock(arduino, clock_info={}):
    """
    N.B.: Uses the fact that the default arg for clock_info can be mutated
    permanently because it's a dictionary. Kinda sketchy...?

    Returns the matrix to be displayed, or None, if the display shouldn't be
    updated.
    """
    now = datetime.now()
    if not update_clock_info(now, clock_info):
        return None
    second = now.second
    minute = now.minute
    hour = now.hour
    if hour >= 22 or hour < 8:
        matrix = generate_empty_matrix()
    else:
        matrix = generate_empty_matrix(1)
    if hour == 0:
        hour = 12
    if hour > 12:
        hour = hour % 12
    second_digits = map(int, [second / 10, second % 10])
    minute_digits = map(int, [minute / 10, minute % 10])
    hour_digits = map(int, [hour / 10, hour % 10])
    # Hours/minutes
    hour_minute_display = [
        numbers_large.ALL[hour_digits[0]],
        numbers_large.ALL[hour_digits[1]],
        numbers_large.SEPARATOR,
        numbers_large.ALL[minute_digits[0]],
        numbers_large.ALL[minute_digits[1]],
    ]
    # Drop the leading zero on the hour
    if hour_digits[0] == 0:
        hour_minute_display[0] = numbers_large.BLANK
    add_items_to_matrix(hour_minute_display, matrix, 1, 0, 1, bit_xor=True)
    # Seconds
    seconds_display = [
        numbers_tiny.ALL[second_digits[0]],
        numbers_tiny.ALL[second_digits[1]],
    ]
    add_items_to_matrix(seconds_display, matrix, 32, 10, 1, bit_xor=True)
    # Weather
    temp_display = []
    if clock_info['temps'].get('current_temp'):
        current_temp = clock_info['temps']['current_temp']
        temp_digits = map(int, [current_temp / 10, current_temp % 10])
        if temp_digits[0] > 9:
            temp_display = [glyphs.SKULL]
        else:
            temp_display = [
                numbers_tiny.ALL[temp_digits[0]],
                numbers_tiny.ALL[temp_digits[1]],
            ]
    else:
        # Communicate error
        temp_display = [letters_tiny.E, letters_tiny.R]
    add_items_to_matrix(temp_display, matrix, 32, 1, 1, bit_xor=True)
    return matrix
