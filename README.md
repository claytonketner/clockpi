Performance Metric
=======================
```
cd py
make stop
make cycle_time
```
A full cycle, which consists of:

- RPi generating an array of what it wants to display
- Transmitting the data from the RPi to the Arduino
- The Arduino displaying the data on the LED's

Runs in 0.38 seconds!


Benchmark Log
================
This table shows how optimizations have affected the execution speed

| Date | Issue Fixed | Benchmark execution time [s] |
| --- | --- | --- |
| 2016-07-13 | No optimizations | 30.7 |
| 2016-07-25 | [#4](https://github.com/claytonketner/clockpi/issues/4) | 23.2 |
| 2016-08-02 | [#2](https://github.com/claytonketner/clockpi/issues/2) | 18.0 |
| 2016-08-05 | [#1](https://github.com/claytonketner/clockpi/issues/1) | 4.4  |
| 2016-08-05 | [#6](https://github.com/claytonketner/clockpi/issues/6) | 1.0  |


Notes
==========
General
--------------
Go through the `Makefile`s and edit the variables to match your setup

Arduino
--------------
In order to build this, you need to add the `LedControl` library to `ar/lib/`
