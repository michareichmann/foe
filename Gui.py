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

        self.MenuBar = MenuBar(self)
        self.CheckBoxes = CheckBoxes(self)
        self.Buttons = Buttons(self)

        self.show()

    def configure(self):
        self.setGeometry(500, 300, 500, 150)
        self.setWindowTitle('Forge of Empires Helper')
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))


class MenuBar(object):

    def __init__(self, gui):
        self.Window = gui
        self.load()

    def load(self):
        action = QtGui.QAction('&EXIT', self.Window)
        action.setShortcut("Ctrl+Q")
        action.setStatusTip('Leave The App')
        action.triggered.connect(close_app)

        self.Window.statusBar()

        main_menu = self.Window.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(action)


class Buttons(object):

    def __init__(self, gui):
        self.Window = gui
        self.Foe = gui.Foe
        self.load()

    def load(self):
        y = [30, 60, 90, 110]
        self.make_button('Quit', close_app, 419, 90)
        self.make_button('Farm Houses', self.Foe.farm_houses, 0, y[0], [None])
        self.make_button('Provisions15', self.Foe.plant_provisions, 0, y[1], [15, 1, 1, 1])
        self.make_button('Provisions15NoFarm', self.Foe.plant_provisions, 110, y[1], [15, 0, 1, 1])
        self.make_button('Loop', self.Foe.plant_loop, 0, y[2], [60, 8])
        self.make_button('Mopo', self.Foe.mopo, 0, y[3], [5])
        self.make_button('Mopo + Tavern', self.Foe.mopo_tavern, 110, y[3], [5, 1, 1])

    def make_button(self, name, func, x, y, args=None):
        btn = QtGui.QPushButton(name, self.Window)
        func = partial(func, *args) if args is not None else func
        btn.clicked.connect(func)
        btn.resize(btn.minimumSizeHint())
        btn.move(x, y)


class CheckBoxes(object):

    def __init__(self, gui):
        self.Window = gui
        self.B = {}
        self.load()

    def load(self):
        self.make_checkbox('Short', self.set_short, 80, 25, checked=True)

    def make_checkbox(self, name, func, x, y, checked=False):
        box = QtGui.QCheckBox(name, self.Window)
        box.stateChanged.connect(func)
        box.move(x, y)
        box.setChecked(checked)
        self.B[name] = box

    def set_short(self, state):
        print state
        self.Window.Foe.Vars['Short'] = state


def close_app():
    print 'Closing application'
    exit(2)


def idle(test):
    print test
    pass


if __name__ == '__main__':

    z = FOE(location='home')
    app = QtGui.QApplication(argv)
    g = Gui(z)
    exit(app.exec_())
