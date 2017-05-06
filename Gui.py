#!/usr/bin/env python
# --------------------------------------------------------
#       GUI for the Forge of Empires project
# created on March 4th 2017 by M. Reichmann (micha.reichmann@gmail.com)
# --------------------------------------------------------

from PyQt4 import QtGui
from sys import exit as ex
from functools import partial
from time import time, sleep
from Utils import windows


class Gui(QtGui.QMainWindow):

    def __init__(self, foe=None):
        super(Gui, self).__init__()

        self.Foe = foe

        self.configure()

        self.MenuBar = MenuBar(self)
        self.CheckBoxes = CheckBoxes(self)
        # self.ProgressBar = self.create_progress_bar()
        self.ComboBoxes = ComboBoxes(self)
        self.SpinBoxes = SpinBoxes(self)
        self.Buttons = Buttons(self)

        self.show()

    def configure(self):
        self.setGeometry(500, 300, 500, 150) if windows else self.setGeometry(1400, 1600, 500, 200)
        self.setWindowTitle('Forge of Empires Helper')
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))

    def create_progress_bar(self):
        pbar = QtGui.QProgressBar(self)
        pbar.setGeometry(200, 30, 250, 20)
        return pbar

    def start_pbar(self, t):
        start = time()
        self.ProgressBar.setMaximum(t)
        now = time()
        while now - start <= t:
            self.ProgressBar.setValue(now - start)
            now = time()
            sleep(.01)


class MenuBar(object):

    def __init__(self, gui):
        self.Window = gui
        self.Menues = {}
        self.load()

    def load(self):
        self.add_menu('File')
        self.add_menu_entry('File', 'Exit', 'Ctrl+Q', close_app, 'Close the Application')
        self.add_menu_entry('File', 'Font', 'Ctrl+F', self.font_choice, 'Open font dialog')

    def add_menu(self, name):
        self.Window.statusBar()
        main_menu = self.Window.menuBar()
        self.Menues[name] = main_menu.addMenu('&{n}'.format(n=name))

    def add_menu_entry(self, menu, name, shortcut, func, tip=''):
        action = QtGui.QAction('&{n}'.format(n=name), self.Window)
        action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(func)
        self.Menues[menu].addAction(action)

    def font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.Window.CheckBoxes.B['Short'].setFont(font)


class Buttons(object):

    def __init__(self, gui):
        self.Window = gui
        self.Foe = gui.Foe
        self.load()

    def load(self):
        spacing = 30 if windows else 40
        y = range(20, 10 * spacing, spacing)
        # self.make_button('Quit', close_app, 419, 90)
        self.make_button('Farm Houses', self.Foe.farm_houses, 2, y[0], [None])
        self.make_button('Provisions', self.Foe.plant_provisions, 2, y[1], [None, None, None])
        self.make_button('Mopo', self.Foe.mopo_tavern, 2, y[2], [None, None, None])
        self.make_button('Loop', self.Foe.plant_loop, 2, y[3], [60, 8])

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
        x = [80, 140] if windows else [150, 240]
        spacing = 30 if windows else 40
        y = range(22, 10 * spacing, spacing)
        self.make_checkbox('Short', x[0], y[0], checked=True)
        self.make_checkbox('Farm', x[0], y[1], checked=True)
        self.make_checkbox('Timer', x[1], y[1], checked=False)
        self.make_checkbox('Mopo', x[0], y[2], checked=True)
        self.make_checkbox('Tavern', x[1], y[2], checked=True)

    def make_checkbox(self, name, x, y, checked=False):
        box = QtGui.QCheckBox(name, self.Window)
        # box.stateChanged.connect(func)
        box.move(x, y)
        box.setChecked(checked)
        self.B[name] = box


class ComboBoxes(object):

    def __init__(self, gui):
        self.Window = gui
        self.B = {}
        self.load()

    def load(self):
        x = 200 if windows else 350
        spacing = 30 if windows else 40
        y = range(20, 10 * spacing, spacing)
        self.create('Times', x, y[1], [5, 15, 1, 4, 8, 24])

    def create(self, name, x, y, items):
        combo_box = QtGui.QComboBox(self.Window)
        combo_box.addItems([str(item) for item in items])
        combo_box.move(x, y)
        combo_box.resize(combo_box.minimumSizeHint())
        combo_box.setCurrentIndex(1)
        self.B[name] = combo_box
        # comboBox.activated[str].connect(self.style_choice)


class SpinBoxes(object):

    def __init__(self, gui):
        self.Window = gui
        self.B = {}
        self.load()

    def load(self):
        x = 200 if windows else 350
        spacing = 30 if windows else 40
        y = range(20, 10 * spacing, spacing)
        self.create('Mopo', x, y[2], 1, 15, 5)

    def create(self, name, x, y, minv, maxv, start=None, step=1):
        start = minv if start is None else start
        box = QtGui.QSpinBox(self.Window)
        box.setRange(minv, maxv)
        box.setSingleStep(step)
        box.setValue(start)
        box.move(x, y)
        box.resize(box.minimumSizeHint())
        self.B[name] = box
        # comboBox.activated[str].connect(self.style_choice)


def close_app():
    print 'Closing application'
    ex(2)


def idle(test):
    print test
    pass


def load_app():
    return QtGui.QApplication([5])


if __name__ == '__main__':

    app = load_app()
    g = Gui()
    ex(app.exec_())
