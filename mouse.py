__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from pymouse import PyMouse


# ============================================
# CLASS DEFINITION
# ============================================
class Mouse:

    def __init__(self):
        self.m = PyMouse()
        self.suppress_xlib_output(2)

    def get_mouse_position(self):
        return self.m.position()

    def press(self, x, y, button=1):
        self.m.press(x, y, button)

    def release(self, x, y, button=1):
        self.m.release(x, y, button)

    @staticmethod
    def suppress_xlib_output(num):
        for i in range(num):
            print '\r\033[1A' + 46 * ' ',
        print