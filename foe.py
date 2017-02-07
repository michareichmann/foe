#!/usr/bin/env python
# ============================================
# IMPORTS
# ============================================
from time import sleep, time
from keys import Keys
from mouse import Mouse
from argparse import ArgumentParser
from os import system
from sys import platform
from numpy import sign
if platform.startswith('win'):
    import winsound


__author__ = 'micha'


windows = platform.startswith('win')


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class FOE(Keys, Mouse):
    def __init__(self, location):
        Keys.__init__(self)
        Mouse.__init__(self)
        self.Location = location
        self.OffSprings = {'ETH': (1000, 836), 'home': (977, 905)}
        self.XMaxs = {'ETH': (1514, 578), 'home': (1596, 593)}
        self.Ymaxs = {'ETH': (457, 569), 'home': (331, 582)}
        self.OffSpring = self.OffSprings[location]
        self.XMax = self.XMaxs[location]
        self.YMax = self.Ymaxs[location]
        self.XPix = 22
        self.YPix = 23
        self.FarmPoints = self.read_points('FarmPoints.txt')
        self.StockPoints = self.read_points('StockPoints.txt')
        self.StockTimes = {5: (750, 520), 15: (951, 520), 1: (1178, 520), 4: (750, 680), 8: (961, 680), 24: (1181, 680)}

    @staticmethod
    def read_points(name):
        f = open(name)
        lines = f.readlines()
        f.close()
        coods = []
        for line in lines:
            data = [int(word) for word in line.strip('\n').split('  ')]
            if len(data) == 3:
                coods += [[data[0] + sign(data[2]) * 2 * i, data[1]] for i in xrange(abs(data[2]))]
            else:
                coods += [data]
        return coods

    @staticmethod
    def finish_sound():
        for i in xrange(3):
            beep(300 + 100 * i)
            sleep(.1)

    def get_pos(self, x, y):
        if x > self.XPix * 2:
            return x, y
        x_pos = self.OffSpring[0] + (self.XMax[0] - self.OffSpring[0]) / float(self.XPix) * x
        y_pos = self.OffSpring[1] + (self.XMax[1] - self.OffSpring[1]) / float(self.XPix) * x
        x_pos += (self.YMax[0] - self.OffSpring[0]) / float(self.YPix) * y
        y_pos += (self.YMax[1] - self.OffSpring[1]) / float(self.YPix) * y
        # print x_pos, y_pos
        return int(x_pos), int(y_pos)

    def move_to(self, x, y):
        self.m.move(*self.get_pos(x, y))

    def drag(self, x, y, button=1):
        x, y = self.get_pos(x, y)
        self.m.drag(x, y, button)

    def press(self, x, y, button=1):
        x, y = self.get_pos(x, y)
        self.m.press(x, y, button)

    def release(self, x, y, button=1):
        x, y = self.get_pos(x, y)
        self.m.release(x, y, button)

    def click(self, x, y, button=1, n=1):
        x, y = self.get_pos(x, y)
        self.m.click(x, y, button, n)

    def move_map(self, p1, p2):
        t = .1
        self.press(p1[0] + 10, p1[1] + 10)
        sleep(t)
        self.move_to(*p1)
        sleep(t)
        self.move_to(*p2)
        sleep(t)
        self.release(*p2)

    def goto_start_position(self,):
        self.move_map((160, 234), (1890, 1056))
        sleep(.1)
        p2 = (500, 275) if self.Location == 'home' else (755, 327)
        self.move_map((1188, 589), p2)

    def switch_player_menu(self, on=True):
        self.click(277, 898) if not on else self.click(277, 1022)

    def farm_houses(self):
        self.goto_start_position()
        sleep(.2)
        for i, p in enumerate(self.FarmPoints):
            sleep(.1)
            self.press(*p) if not i else self.move_to(*p)
        self.release(*self.FarmPoints[-1])

    def farm_stock(self):
        for i, p in enumerate(self.StockPoints):
            sleep(.2)
            self.press(*p) if not i else self.move_to(*p)
        sleep(.2)
        self.release(*self.StockPoints[-1])

    @staticmethod
    def get_time(t):
        return 60 * (t if t in [5, 15] else t * 60) + 2

    def plant_stock(self, t=15, farm=True, sound=True):
        # self.switch_player_menu(on=False)
        self.goto_start_position()
        sleep(.2)
        if farm:
            self.farm_stock()
            sleep(3)
        for i, p in enumerate(self.StockPoints):
            sleep(.5)
            self.click(*p)
            sleep(1)
            self.click(*self.StockTimes[t])
        # self.switch_player_menu(on=True)
        if sound:
            sleep(self.get_time(t))
            self.finish_sound()

    def plant_loop(self, first_time=60, iterations=8):
        first_loop = True
        for _ in xrange(iterations):
            start = time()
            t = start - time()
            n_loops = 1
            while t < (60 if not first_loop else first_time) * 60 + 5:
                print 'starting loop {n}'.format(n=n_loops),
                if not first_loop:
                    self.farm_stock()
                    sleep(3)
                first_loop = False
                self.plant_stock(5, farm=False, sound=False)
                start2 = time()
                t = 0
                while t < 5 * 60 + 2:
                    t = int(time() - start2)
                    print '\rloop {n}, time: {m:02d}:{s:02d}'.format(m=t / 60, s=t - t / 60 * 60, n=n_loops),
                    sleep(1)
                print
                n_loops += 1
                t = time() - start
            self.farm_houses()

    def motivate(self, n=10):
        x0, y = 667, 1028
        for _ in xrange(n):
            for i in xrange(5):
                x = x0 - 100 * i
                self.click(x, y)
                sleep(1)
            self.click(220, 984)
            sleep(1)


def idle():
    pass


def beep(freq=500, dur=.5):
    if not windows:
        system('play --no-show-progress --null --channels 1 synth {d} sine {f}'.format(d=dur, f=freq))
    else:
        winsound.Beep(freq, int(dur * 1000))


if __name__ == '__main__':
    locations = ['ETH', 'home']
    parser = ArgumentParser()
    parser.add_argument('location', nargs='?', type=int, default=1)
    args = parser.parse_args()
    z = FOE(locations[args.location])
