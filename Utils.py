#!/usr/bin/env python
# --------------------------------------------------------
#       Utility methods for the Forge of Empires project
# created on March 4th 2017 by M. Reichmann (micha.reichmann@gmail.com)
# --------------------------------------------------------

from os import system
from time import sleep
from sys import platform
windows = platform.startswith('win')
if windows:
    import winsound


def idle():
    pass


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def beep(freq=500, dur=.5):
    if not windows:
        system('play --no-show-progress --null --channels 1 synth {d} sine {f}'.format(d=dur, f=freq))
    else:
        winsound.Beep(freq, int(dur * 1000))


def finish_sound():
    for i in xrange(3):
        beep(300 + 100 * i)
        sleep(.1)


def get_time(t):
    # return time in seconds
    return 60 * (t if t in [5, 15] else t * 60) + 2


def calc_stocktimes(p1, p2):
    d = p2[0] - p1[0]
    return {5: (p1[0], p1[1]), 15: (p1[0] + d, p1[1]), 1: (p1[0] + 2 * d, p1[1]), 4: (p1[0], p1[1] + d), 8: (p1[0] + d, p1[1] + d), 24: (p1[0] + 2 * d, p1[1] + d)}
