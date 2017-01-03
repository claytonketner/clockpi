#!/usr/bin/env python
import graphics
import utils


if __name__ == '__main__':
    arduino = utils.connect_to_arduino()
    graphics.display_clock(arduino)
