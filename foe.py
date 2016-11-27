#!/usr/bin/env python
# ============================================
# IMPORTS
# ============================================
from time import sleep
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
        self.OffSpring = (956, 852)
        self.XMax = (1683, 494)
        self.YMax = (484, 617)
        self.XPix = 23
        self.YPix = 15
        self.FarmPoints = self.read_points('FarmPoints.txt')
        self.StockPoints = self.read_points('StockPoints.txt')

    def read_points(self, name):
        f = open(name)
        lines = f.readlines()
        f.close()
        return [[int(cood) for cood in line.strip('\n').split('  ')] for line in lines]


    def get_pos(self, x, y):
        x_pos = self.OffSpring[0] + (self.XMax[0] - self.OffSpring[0]) / float(self.XPix) * x
        y_pos = self.OffSpring[1] + (self.XMax[1] - self.OffSpring[1]) / float(self.XPix) * x
        x_pos += (self.YMax[0] - self.OffSpring[0]) / float(self.YPix) * y
        y_pos += (self.YMax[1] - self.OffSpring[1]) / float(self.YPix) * y
        print x_pos, y_pos
        return int(x_pos), int(y_pos)

    def move_to(self, x, y):
        self.m.move(*self.get_pos(x, y))

    def press(self, x, y, button=1):
        x, y = self.get_pos(x, y)
        self.m.press(x, y, button)

    def release(self, x, y, button=1):
        x, y = self.get_pos(x, y)
        self.m.release(x, y, button)

    def farm(self):
        for i, p in enumerate(self.FarmPoints):
            sleep(.5)
            self.press(*p) if not i else self.move_to(*p)
        self.release(*self.FarmPoints[-1])



if __name__ == '__main__':
    z = FOE()