from datetime import datetime
from types import ModuleType

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.external import get_traffic
from clockpi.external import get_weather_temps
from clockpi.secret import DIRECTIONS_END_HOUR
from clockpi.secret import DIRECTIONS_START_HOUR


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
    if hour_12 < 10:
        clock_info['hour_digits'][0] = 'BLANK'
    # Weather
    clock_info['weather_update_time'], clock_info['weather'] = (
        get_weather_temps(clock_info.setdefault('weather_update_time', now),
                          clock_info.get('weather', {})))
    if clock_info.get('weather'):
        # Temp out of range
        if (clock_info['weather']['current_temp'] > 99 or
                clock_info['weather']['current_temp'] < 0):
            clock_info['temp_digits'] = ['SKULL']
        else:
            clock_info['temp_digits'] = map(
                int, [clock_info['weather']['current_temp'] / 10 % 10,
                      clock_info['weather']['current_temp'] % 10])
        clock_info['sun_is_up'] = (clock_info['weather']['sunrise'] < now and
                                   clock_info['weather']['sunset'] > now)
    else:
        clock_info['temp_digits'] = ['E', 'R']
        # Default to sundown because the bright clockface is annoying at night
        clock_info['sun_is_up'] = False
    # Traffic
    clock_info['traffic_update_time'], clock_info['traffic'] = get_traffic(
        clock_info.setdefault('traffic_update_time', now),
        clock_info.get('traffic', {}))
    if clock_info.get('traffic'):
        clock_info['traffic_delta_digits'] = map(
            int, [clock_info['traffic']['traffic_delta'] / 10 % 10,
                  clock_info['traffic']['traffic_delta'] % 10])
        clock_info['travel_time_digits'] = map(
            int, [clock_info['traffic']['travel_time'] / 10 % 10,
                  clock_info['traffic']['travel_time'] % 10])
    clock_info['show_traffic'] = (clock_info.get('traffic') and hour_24 >=
                                  DIRECTIONS_START_HOUR and hour_24 <
                                  DIRECTIONS_END_HOUR)
    # Special cases
    clock_info['separator'] = ['SEPARATOR']
    return True


def data_to_alphanums(data_list, alphanum_source):
    """
    Converts a list of numbers or variable names to a list of alphanum arrays
    You can do different combinations of parameters (this is probably bad
    practice). The items in data_list are evaluated on a per-item basis, so
    data_list can contain both ints and strings. Not all combinations work.
    Examples:
        - One of the items in data_list is an int
        - alphanum_source is a list of alphanums
        The alphanum will be looked up by using the int from data_list as the
        index for alphanum_source

        - One of the items in data_list is an int
        - alphanum_source is a module
        The alphanum will be looked up by accessing the ALL_NUMBERS list in
        the alphanum_source module

        - One of the items in data_list is a str
        - alphanum_source is a module
        The alphanum will be looked up by using the str from data_list as the
        name of a variable in the module
    """
    alphanum_list = []
    for item in data_list:
        if isinstance(item, int) and isinstance(alphanum_source, list):
            alphanum_list.append(alphanum_source[item])
        elif isinstance(item, int) and isinstance(alphanum_source, ModuleType):
            alphanum_list.append(alphanum_source.ALL_NUMBERS[item])
        elif isinstance(item, str) and isinstance(alphanum_source, ModuleType):
            alphanum_list.append(getattr(alphanum_source, item))
        else:
            raise NotImplementedError("No way to relate {item} to the source "
                                      "data type given {source_type}".format(
                                          item=item,
                                          source_type=type(alphanum_source)))
    return alphanum_list


def config_to_matrix(config, data):
    """
    Takes a configuration and data and generates a matrix using the two. There
    is a special case where you can provide a list of fonts instead of a single
    font. In this case, each item in the list will be tried and the first one
    that works will be used.
    """
    matrix = generate_empty_matrix()
    for group_name, group_config in config.iteritems():
        data_name = group_config['data_name']
        if data_name not in data:
            print "{} not in the data given".format(data_name)
            continue
        group_data = data[data_name]
        font = group_config['font']
        if isinstance(font, list):
            for font_choice in font:
                try:
                    group_display = data_to_alphanums(group_data, font_choice)
                    break
                except:
                    pass
            else:
                raise ValueError("None of the font choices for {} "
                                 "worked.".format(group_name))
        else:
            group_display = data_to_alphanums(group_data, font)
        add_items_to_matrix(group_display, matrix, **group_config['spatial'])
    return matrix
