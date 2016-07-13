#!/usr/bin/env python
import graphics
import utils


arduino = utils.connect_to_arduino()
graphics.benchmark(arduino)
# graphics.display_clock(arduino)
