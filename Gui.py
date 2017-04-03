#!/usr/bin/env python
# --------------------------------------------------------
#       GUI for the Forge of Empires project
# created on March 4th 2017 by M. Reichmann (micha.reichmann@gmail.com)
# --------------------------------------------------------

from PyQt4 import QtGui
from sys import argv, exit
from foe import FOE
from functools import partial


class Gui(QtGui.QMainWindow):

    def __init__(self, foe):
        super(Gui, self).__init__()

        self.Foe = foe

        self.configure()

        self.Buttons = Buttons(self)
        self.Buttons.load()

        self.show()

    def configure(self):
        self.setGeometry(500, 300, 500, 150)
        self.setWindowTitle('Forge of Empires Helper')
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))


class Buttons(object):

    def __init__(self, gui):
        self.Window = gui
        self.Foe = gui.Foe

    def load(self):
        self.make_button('Quit', close_app, 419, 90)
        self.make_button('Farm Short Houses', self.Foe.farm_houses, 0, 0, [1])
        self.make_button('Farm Houses', self.Foe.farm_houses, 110, 0, [0])
        self.make_button('Provisions15', self.Foe.plant_provisions, 0, 30, [15, 1, 1, 1])
        self.make_button('Provisions15NoFarm', self.Foe.plant_provisions, 110, 30, [15, 0, 1, 1])
        self.make_button('Loop', self.Foe.plant_loop, 0, 60, [60, 8])
        self.make_button('Mopo', self.Foe.mopo, 0, 90, [5])
        self.make_button('Mopo + Tavern', self.Foe.mopo_tavern, 110, 90, [5, 1, 1])

    def make_button(self, name, func, x, y, args=None):
        btn = QtGui.QPushButton(name, self.Window)
        func = partial(func, *args) if args else func
        btn.clicked.connect(func)
        btn.resize(btn.minimumSizeHint())
        btn.move(x, y)


def close_app():
    print 'Closing application'
    exit(2)


if __name__ == '__main__':

    z = FOE(location='home')
    app = QtGui.QApplication(argv)
    g = Gui(z)
    exit(app.exec_())
