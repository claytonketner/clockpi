from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_tiny
from clockpi.graphics.utils import add_items_to_matrix
from clockpi.graphics.utils import digit_to_graphic
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.graphics.utils import update_clock_info


def display_clock(arduino, clock_info={}):
    """
    N.B.: Uses the fact that the default arg for clock_info can be mutated
    permanently because it's a dictionary. Kinda sketchy...?

    Returns the matrix to be displayed, or None, if the display shouldn't be
    updated.
    """
    if not update_clock_info(clock_info):
        return None
    if clock_info['sun_is_up']:
        matrix = generate_empty_matrix(1)
    else:
        matrix = generate_empty_matrix()
    # Hours/minutes
    hour_minute_display = digit_to_graphic(clock_info['hour_digits'],
                                           numbers_large.ALL_NUMBERS)
    hour_minute_display.append(numbers_large.SEPARATOR)
    hour_minute_display.extend(digit_to_graphic(clock_info['minute_digits'],
                                                numbers_large.ALL_NUMBERS))
    # Drop the leading zero on the hour
    if clock_info['hour_digits'][0] == 0:
        hour_minute_display[0] = numbers_large.BLANK
    add_items_to_matrix(hour_minute_display, matrix, 1, 1, 1, bit_xor=True)
    # Seconds
    seconds_display = digit_to_graphic(clock_info['second_digits'],
                                       numbers_tiny.ALL_NUMBERS)
    add_items_to_matrix(seconds_display, matrix, 32, 10, 1, bit_xor=True)
    # Weather
    temp_display = []
    if clock_info.get('weather'):
        current_temp = clock_info['weather']['current_temp']
        if current_temp > 99 or current_temp < 0:
            temp_display = [glyphs.SKULL]
        else:
            temp_display = digit_to_graphic(clock_info['temp_digits'],
                                            numbers_tiny.ALL_NUMBERS)
    else:
        # Something's wrong!
        temp_display = [letters_tiny.E, letters_tiny.R]
    add_items_to_matrix(temp_display, matrix, 32, 1, 1, bit_xor=True)
    return matrix
