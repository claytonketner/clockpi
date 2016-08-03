#!/usr/bin/env python
import benchmark
import utils


arduino = utils.connect_to_arduino()
benchmark.benchmark(arduino)
