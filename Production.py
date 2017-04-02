#!/usr/bin/env python
# --------------------------------------------------------
#       Class to handle the productions sites for Forge of Empires
# created on March 4th 2017 by M. Reichmann (micha.reichmann@gmail.com)
# --------------------------------------------------------

from collections import OrderedDict
from numpy import sign
from Utils import is_int
from ConfigParser import ConfigParser
from json import loads


class Production(object):

    def __init__(self, houses=True):

        self.FileName = 'HousePoints.txt' if houses else 'ProvisionPoints.txt'
        self.Info = load_productions(houses)
        self.Points = read_points(self.FileName)
        self.ShortPoints = self.get_short_points() if houses else None
        self.Produced = OrderedDict([(f, 0) for f in [1, 1.2, 1.6]])

    def get_short_points(self):
        dic = OrderedDict()
        for point, typ in self.Points.iteritems():
            if self.Info[typ].keys()[0] not in [4, 8, 24]:
                dic[point] = typ
        return dic

    def add_production(self, typ, time=None):
        time = self.Info[typ].keys()[0] if time is None else time
        for factor in self.Produced:
            self.Produced[factor] += int(self.Info[typ][time] * factor)

    def reset_production(self):
        for factor in self.Produced:
            self.Produced[factor] = 0

    def print_production(self):
        print 'You already produced:'
        for factor, prod in self.Produced.iteritems():
            print '{f:3.0f}%:\t{p:6d}'.format(f=100 * factor, p=prod)


def read_points(name):
    f = open(name)
    lines = f.readlines()
    f.close()
    coods = OrderedDict()
    for line in lines:
        # skip empty lines and commented lines
        if len(line) < 2 or line.startswith('#'):
            continue
        data = [word.strip(' ') for word in line.strip('\n\r').split(' ') if word.strip(' ')]
        typ = data[-1].lower()
        data = [int(i) for i in data if is_int(i)]
        data += [1] if len(data) == 2 else []
        for i in xrange(abs(data[2])):
            coods[(data[0] + sign(data[2]) * 2 * i, data[1])] = typ
    return coods


def load_productions(houses):
    p = ConfigParser()
    p.read('production.conf')
    dic = {}
    section = 'Houses' if houses else 'Provisions'
    for option in p.options(section):
        if houses:
            value = loads(p.get(section, option))
            dic[option] = {value[1]: value[0]}
        else:
            value = p.getint(section, option)
            values = [value / float(i) for i in [30, 12, 5, 3, 2, 1]]
            dic[option] = {t: int(round(val, -1)) if (not value % 60 == 0 and value > 500) else int(val) for val, t in zip(values, [5, 15, 1, 4, 8, 24])}
    return dic


if __name__ == '__main__':

    z = Production(0)
