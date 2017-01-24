from clockpi.external import get_weather_temps


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


def update_clock_info(now, clock_info):
    second = now.second
    if clock_info.get('last_second') == second:
        # Don't update if it won't change the clockface
        return False
    clock_info['last_second'] = second
    clock_info['weather_update_time'], clock_info['temps'] = get_weather_temps(
        clock_info.setdefault('weather_update_time', now),
        clock_info.get('temps', {}))
    return True
