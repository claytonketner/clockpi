#!/usr/bin/env python
from clockpi.graphics.graphics import display_clock
from clockpi.utils import connect_to_arduino


if __name__ == '__main__':
    arduino = connect_to_arduino()
    display_clock(arduino)
