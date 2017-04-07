#!/usr/bin/env python
# ============================================
# IMPORTS
# ============================================
from time import sleep, time
from keys import Keys
from mouse import Mouse
from argparse import ArgumentParser
from Utils import finish_sound, get_time
from Production import Production


__author__ = 'micha'


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
        self.OffSpring = self.OffSprings[location]
        self.XVector = self.XMaxs[location][0] - self.OffSpring[0], self.XMaxs[location][1] - self.OffSpring[1]
        self.XPix = 22.
        self.Houses = Production(houses=True)
        self.Provisions = Production(houses=False)
        self.StockTimes = {5: (750, 520), 15: (951, 520), 1: (1178, 520), 4: (750, 680), 8: (961, 680), 24: (1181, 680)}
        self.Vars = {'Short': True}

    # ======================================
    # region map manipulation
    def get_pos_from_mouse_pos(self):
        x, y = self.get_mouse_position()
        # length from offspring
        x, y = x - self.OffSpring[0], y - self.OffSpring[1]
        x1 = x * self.XPix / (2. * self.XVector[0]) + y * self.XPix / (2. * self.XVector[1])
        y1 = -x * self.XPix / (2. * self.XVector[0]) + y * self.XPix / (2. * self.XVector[1])
        return x1, y1

    def get_pix_pos(self, x, y):
        # return pixel values if pixel values are provided
        if any(value > 100 for value in [x, y]):
            return x, y
        xpix = (x - y) / self.XPix * self.XVector[0] + self.OffSpring[0]
        ypix = (x + y) / self.XPix * self.XVector[1] + self.OffSpring[1]
        return int(xpix), int(ypix)

    def move_to(self, x, y):
        self.m.move(*self.get_pix_pos(x, y))

    def drag(self, x, y, button=1):
        x, y = self.get_pix_pos(x, y)
        self.m.drag(x, y, button)

    def press(self, x, y, button=1):
        x, y = self.get_pix_pos(x, y)
        self.m.press(x, y, button)

    def release(self, x, y, button=1):
        x, y = self.get_pix_pos(x, y)
        self.m.release(x, y, button)

    def click(self, x, y, button=1, n=1):
        x, y = self.get_pix_pos(x, y)
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
        self.move_map((160, 274), (1890, 1056))
        sleep(.1)
        p2 = (500, 275) if self.Location == 'home' else (755, 327)
        self.move_map((1188, 589), p2)

    def switch_player_menu(self, on=True):
        self.click(277, 898) if not on else self.click(277, 1022)

    # endregion

    def farm_houses(self, short=None):
        short = self.Vars['Short'] if short is None else short
        self.goto_start_position()
        sleep(.2)
        points = self.Houses.ShortPoints if short else self.Houses.Points
        for i, (point, typ) in enumerate(points.iteritems()):
            sleep(.1)
            self.press(*point) if not i else self.move_to(*point)
            self.Houses.add_production(typ)
        self.release(*points.keys()[-1])
        self.Houses.print_production()

    def farm_provisions(self):
        for i, point in enumerate(self.Provisions.Points.iterkeys()):
            sleep(.2)
            self.press(*point) if not i else self.move_to(*point)
        sleep(.2)
        self.release(*self.Provisions.Points.keys()[-1])

    def plant_provisions(self, t=15, farm=True, sound=True, prnt=True):
        self.goto_start_position()
        sleep(.2)
        if farm:
            self.farm_provisions()
            sleep(3)
        for i, (point, typ) in enumerate(self.Provisions.Points.iteritems()):
            sleep(.5)
            self.click(*point)
            sleep(1)
            self.click(*self.StockTimes[t])
            self.Provisions.add_production(typ, t)
        if prnt:
            self.Provisions.print_production()
        if sound:
            sleep(get_time(t))
            finish_sound()

    def plant_stock_loop(self, t=15, farm=True):
        while not raw_input('Wanna continue? '):
            self.plant_provisions(t, farm)

    def plant_loop(self, first_time=60, iterations=8):
        first_loop = True
        for _ in xrange(iterations):
            start = time()
            t = start - time()
            n_loops = 1
            while t < (60 if not first_loop else first_time) * 60 + 5:
                self.plant_provisions(5, farm=not first_loop, sound=False, prnt=True)
                first_loop = False
                start2 = time()
                t = 0
                while t < 5 * 60 + 2:
                    t = int(time() - start2)
                    sleep(1)
                n_loops += 1
                t = time() - start
            self.farm_houses()
        print

    def motivate(self):
        x, y = 667, 1028
        for _ in xrange(5):
            self.click(x, y)
            x -= 99
            sleep(1)

    def tavernate(self):
        x, y = 702, 1010
        for _ in xrange(5):
            self.click(x, y)
            x -= 99
            sleep(1)
            self.click(1732, 887)
            sleep(.2)

    def mopo_tavern(self, n=10, mopo=True, tavern=True):
        for _ in xrange(n):
            if mopo:
                self.motivate()
            if tavern:
                self.tavernate()
            self.click(220, 984)
            sleep(1)

    def mopo(self, n=10):
        self.mopo_tavern(n, True, False)

    def calc_productions(self, t_tot=1, boost=False):
        for t in self.StockTimes:
            i_boosts = 0
            t1 = t / 60. if t in [5, 15] else t
            p1 = 0
            p2 = 0
            t2 = t1
            fac = 1.65 if boost else 1
            while t2 < t_tot + .001:
                for prod in self.ProductPoints.itervalues():
                    if i_boosts >= 40:
                        fac = 1
                    p1 += int(self.Production[prod][t] * fac)
                    p2 += int(int(self.Production[prod][t] * 1.2) * fac)
                    i_boosts += 1
                t2 += t1
            if p1:
                print t, p1, p2


if __name__ == '__main__':
    locations = ['ETH', 'home']
    parser = ArgumentParser()
    parser.add_argument('location', nargs='?', type=int, default=1)
    parser.add_argument('opt', nargs='?', type=int, default=0)
    parser.add_argument('arg1', nargs='?', type=int, default=15)
    parser.add_argument('arg2', nargs='?', type=int, default=1)
    args = parser.parse_args()
    z = FOE(locations[args.location])
