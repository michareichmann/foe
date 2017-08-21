#!/usr/bin/env python

from time import sleep, time
from keys import Keys
from mouse import Mouse
from argparse import ArgumentParser
from Utils import finish_sound, get_time, calc_stocktimes, calc_goodtimes
from Production import Production
from Gui import Gui, load_app, ex
from ConfigParser import ConfigParser, NoOptionError
from json import loads
from os.path import join


__author__ = 'micha'


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class FOE(Keys, Mouse):
    def __init__(self, location, load_gui=False):
        Keys.__init__(self)
        Mouse.__init__(self)
        self.Location = location
        self.ConfigDir = 'config'
        self.XPix = 22.
        self.OffSpring = self.load_config('Gauge')[:2]
        self.XVector = self.load_xvec()
        self.Houses = Production(houses=True)
        self.Provisions = Production()
        self.Goods = Production(goods=True)
        self.StockTimes = self.load_stocktimes()
        self.GoodTimes = self.load_goodtimes()

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

    def load_config(self, section):
        conf = ConfigParser()
        conf.read(join(self.ConfigDir, 'Locations.conf'))
        try:
            return tuple(loads(conf.get(section, self.Location)))
        except NoOptionError:
            print 'Could not find {l} in section {s}'.format(l=self.Location, s=section)
            raise NoOptionError

    def load_xvec(self):
        return tuple([x22 - self.OffSpring[i] for i, x22 in enumerate(self.load_config('Gauge')[2:])])

    def load_stocktimes(self):
        lst = self.load_config('StockTimes')
        return calc_stocktimes(lst[:2], lst[2:])

    def load_goodtimes(self):
        lst = self.load_config('GoodTimes')
        return calc_goodtimes(lst[:2], lst[2:])

    # ======================================
    # region map manipulation
    def get_pos_from_mouse_pos(self, t=0):
        sleep(t)
        x, y = self.get_mouse_position()
        # length from offspring
        x, y = x - self.OffSpring[0], y - self.OffSpring[1]
        x1 = x * self.XPix / (2. * self.XVector[0]) + y * self.XPix / (2. * self.XVector[1])
        y1 = -x * self.XPix / (2. * self.XVector[0]) + y * self.XPix / (2. * self.XVector[1])
        if t:
            print '({:1.0f}, {:1.0f})'.format(x1, y1)
        return x1, y1

    def get_mouse_position(self, t=0):
        sleep(t)
        x, y = self.m.position()
        if t:
            print '({:1.0f}, {:1.0f})'.format(x, y)
        return x, y

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

    def goto_edge(self):
        lst = self.load_config('Edge')
        self.move_map(lst[:2], lst[2:])

    def goto_start_position(self,):
        self.goto_edge()
        sleep(.1)
        lst = self.load_config('Start')
        self.move_map(lst[:2], lst[2:])
        sleep(.1)

    def switch_player_menu(self, on=True):
        self.click(277, 898) if not on else self.click(277, 1022)

    # endregion

    def farm_houses(self, short=None):
        x, y = self.get_mouse_position()
        short = self.check('Short') if short is None else short
        self.goto_start_position()
        sleep(.2)
        points = self.Houses.ShortPoints if short else self.Houses.Points
        for i, (point, typ) in enumerate(points.iteritems()):
            sleep(.1)
            self.press(*point) if not i else self.move_to(*point)
            self.Houses.add_production(typ)
        self.release(*points.keys()[-1])
        sleep(.1)
        self.Houses.print_production()
        self.move_to(x, y)
        self.press_alt_tab()

    def farm_goods(self):
        self.farm_provisions(True)

    def farm_provisions(self, goods=False):
        production = self.Provisions if not goods else self.Goods
        for i, point in enumerate(production.Points.iterkeys()):
            sleep(.2)
            self.press(*point) if not i else self.move_to(*point)
        sleep(.2)
        self.release(*production.Points.keys()[-1])

    def plant_provisions(self, t=None, farm=None, timer=None, prnt=True, goods=False):
        t = int(self.get_box_entry('Times' if not goods else 'GoodTimes')) if t is None else t
        farm = self.check('Farm' if not goods else 'GoodFarm') if farm is None else farm
        timer = self.check('Timer') if timer is None else timer
        self.goto_start_position()
        sleep(.2)
        production = self.Provisions if not goods else self.Goods
        times = self.StockTimes if not goods else self.GoodTimes
        if farm:
            self.farm_provisions(goods)
            sleep(3)
        for i, (point, typ) in enumerate(production.Points.iteritems()):
            sleep(.5)
            self.click(*point)
            sleep(1)

            self.click(*times[t])
            production.add_production(typ, t)
        if prnt:
            production.print_production()
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
        lst = self.load_config('MoPo')
        x, y = lst[2:4]
        for _ in xrange(5):
            self.click(x, y)
            x -= lst[2] - lst[4]
            sleep(1)

    def open_next_player_menu(self):
        lst = self.load_config('MoPo')
        x, y = lst[:2]
        y -= lst[3] - lst[1]
        x -= (lst[2] - lst[4]) * 5
        self.click(x, y)

    def tavernate(self):
        lst = self.load_config('MoPo')
        x, y = lst[:2]
        for _ in xrange(5):
            self.click(x, y)
            x -= lst[2] - lst[4]
            sleep(1)
            # closing tavern menu
            self.click(x, y)
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
            self.open_next_player_menu()
            sleep(1)
        self.press_alt_tab()
        self.move_to(x, y)


if __name__ == '__main__':
    locations = ['ETH', 'home', 'yoga', 'psi', 'analysis']
    parser = ArgumentParser()
    parser.add_argument('location', nargs='?', type=int, default=1)
    parser.add_argument('-g', '--gui', action='store_true')
    args = parser.parse_args()
    z = FOE(locations[args.location], args.gui)
    if args.gui:
        ex(z.App.exec_())
