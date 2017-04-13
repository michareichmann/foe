#!/usr/bin/env python
# ============================================
# IMPORTS
# ============================================
from time import sleep, time
from keys import Keys
from mouse import Mouse
from argparse import ArgumentParser
from Utils import finish_sound, get_time, calc_stocktimes
from Production import Production
from Gui import Gui, load_app, ex


__author__ = 'micha'


stock_times = {'ETH': {5: (750, 520), 15: (951, 520), 1: (1178, 520), 4: (750, 680), 8: (961, 680), 24: (1181, 680)},
               'home': {5: (750, 520), 15: (951, 520), 1: (1178, 520), 4: (750, 680), 8: (961, 680), 24: (1181, 680)},
               'yoga': calc_stocktimes((1150, 1824), (1310, 1834))}


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class FOE(Keys, Mouse):
    def __init__(self, location, load_gui=False):
        Keys.__init__(self)
        Mouse.__init__(self)
        self.Location = location
        self.OffSprings = {'ETH': (1000, 836), 'home': (977, 905), 'yoga': (1332, 1924)}  # -1080
        self.XMaxs = {'ETH': (1514, 578), 'home': (1596, 593), 'yoga': (1842, 1666)}
        self.OffSpring = self.OffSprings[location]
        self.XVector = self.XMaxs[location][0] - self.OffSpring[0], self.XMaxs[location][1] - self.OffSpring[1]
        self.XPix = 22.
        self.Houses = Production(houses=True)
        self.Provisions = Production(houses=False)
        self.StockTimes = stock_times[location]

        # gui
        if load_gui:
            self.App = load_app()
            self.Gui = Gui(self)

    def check(self, name):
        return self.Gui.CheckBoxes.B[name].isChecked()

    def get_box_entry(self, name):
        return self.Gui.ComboBoxes.B[name].currentText()

    def get_box_value(self, name):
        return self.Gui.SpinBoxes.B[name].value()

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
        y0 = 0
        self.move_map((160, 274 + y0), (1890, 1056 + y0))
        sleep(.1)
        p2s = {'home': (500, 275), 'ETH': (755, 327), 'yoga': (1059, 1410)}
        p2 = p2s[self.Location]
        self.move_map((1188, 589 + y0), p2)

    def switch_player_menu(self, on=True):
        self.click(277, 898) if not on else self.click(277, 1022)

    # endregion

    def farm_houses(self, short=None):
        short = self.check('Short') if short is None else short
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

    def plant_provisions(self, t=None, farm=None, timer=None, prnt=True):
        t = int(self.get_box_entry('Times')) if t is None else t
        farm = self.check('Farm') if farm is None else farm
        timer = self.check('Timer') if timer is None else timer
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
        if timer:
            self.Gui.start_pbar(get_time(t))
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
                self.plant_provisions(5, farm=not first_loop, timer=False, prnt=True)
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

    def mopo_tavern(self, n=None, mopo=None, tavern=None):
        x, y = self.get_mouse_position()
        mopo = self.check('Mopo') if mopo is None else mopo
        tavern = self.check('Tavern') if tavern is None else tavern
        n = self.get_box_value('Mopo') if n is None else n
        for _ in xrange(n):
            if mopo:
                self.motivate()
            if tavern:
                self.tavernate()
            self.click(220, 984)
            sleep(1)
        self.press_alt_tab()
        self.move_to(x, y)

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
    locations = ['ETH', 'home', 'yoga']
    parser = ArgumentParser()
    parser.add_argument('location', nargs='?', type=int, default=1)
    parser.add_argument('-g', '--gui', action='store_true')
    args = parser.parse_args()
    z = FOE(locations[args.location], args.gui)
    if args.gui:
        ex(z.App.exec_())
