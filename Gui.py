#!/usr/bin/env python
# --------------------------------------------------------
#       GUI for the Forge of Empires project
# created on March 4th 2017 by M. Reichmann (micha.reichmann@gmail.com)
# --------------------------------------------------------

from PyQt4 import QtGui
from sys import argv


class Gui(object):

    def __init__(self):

        self.App = QtGui.QApplication(argv)
        self.Window = QtGui.QWidget()
        self.load_settings()

    def load_settings(self):
        self.Window.setGeometry(500, 300, 500, 500)
        self.Window.setWindowTitle('Forge of Empires Helper')


if __name__ == '__main__':

    z = Gui()
