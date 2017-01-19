#!/usr/bin/env python
# ============================================
# IMPORTS
# ============================================
from time import sleep, time
from keys import Keys
from mouse import Mouse


__author__ = 'micha'


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class FOE(Keys, Mouse):
    def __init__(self):
        Keys.__init__(self)
        Mouse.__init__(self)
        self.OffSpring = (982, 996)
        self.XMax = (1761, 604)
        self.YMax = (257, 631)
        self.XPix = 25
        self.YPix = 23
        self.FarmPoints = self.read_points('FarmPoints.txt')
        self.StockPoints = self.read_points('StockPoints.txt')
        self.StockTimes = {5: (730, 472), 15: (951, 485), 1: (1178, 487), 4: (737, 651), 8: (961, 660), 24: (1181, 669)}

    @staticmethod
    def read_points(name):
        f = open(name)
        lines = f.readlines()
        f.close()
        return [[int(cood) for cood in line.strip('\n').split('  ')] for line in lines]

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

    def farm_houses(self):
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

    def plant_stock(self, t=15, farm=True):
        if farm:
            self.farm_stock()
            sleep(3)
        for i, p in enumerate(self.StockPoints):
            sleep(.5)
            self.click(*p)
            sleep(1)
            self.click(*self.StockTimes[t])

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
                self.plant_stock(5, farm=False)
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


def idle():
    pass

if __name__ == '__main__':
    z = FOE()
