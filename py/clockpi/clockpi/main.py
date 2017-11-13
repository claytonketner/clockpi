#!/usr/bin/env python
from clockpi.graphics.graphics import display_clock
from clockpi.utils import connect_to_arduino
from clockpi.utils import matrix_to_command
from clockpi.utils import send_data


if __name__ == '__main__':
    arduino = connect_to_arduino()
    while True:
        matrix = display_clock()
        if matrix:
            send_data(arduino, matrix_to_command(matrix))
