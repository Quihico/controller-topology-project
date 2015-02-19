#
# Copyright (c) 2014 Garrett Brown
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

BUTTON_RECTANGLE = 'rectangle'
BUTTON_CIRCLE    = 'circle'
BUTTON_DPAD      = 'dpad'

class Button(object):
    def __init__(self, geometry):
        self._geometry = geometry

    def Type(self):
        return self._geometry

    @staticmethod
    def FromNode(node):
        if node.tag =='button':
            geometry = node.attrib.get('geometry')
            if geometry == BUTTON_RECTANGLE:
                return Rectangle.FromNode(node)
            elif geometry == BUTTON_CIRCLE:
                return Circle.FromNode(node)
        elif node.tag == BUTTON_DPAD:
            return Dpad.FromNode(node)
        return None

class Rectangle(Button):
    def __init__(self, x1, y1, x2, y2):
        super(Rectangle, self).__init__(BUTTON_RECTANGLE)
        self._x1, self._x2 = ((x1, x2) if x1 <= x2 else (x2, x1))
        self._y1, self._y2 = ((y1, y2) if y1 <= y2 else (y2, y1))

    def Coords(self):
        return self._x1, self._y1, self._x2, self._y2

    def Point1(self):
        return self._x1, self._y1

    def Point2(self):
        return self._x2, self._y2

    def Center(self):
        return (self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2

    def Width(self):
        return self._x2 - self._x1

    def Height(self):
        return self._y2 - self._y1

    @staticmethod
    def FromNode(node):
        try:
            x1 = int(node.attrib.get('x1'))
            y1 = int(node.attrib.get('y1'))
            x2 = int(node.attrib.get('x2'))
            y2 = int(node.attrib.get('y2'))
            return Rectangle(x1, y1, x2, y2)
        except ValueError:
            pass
        return None

class Circle(Button):
    def __init__(self, x, y, r):
        super(Circle, self).__init__(BUTTON_CIRCLE)
        self._x = x
        self._y = y
        self._r = r

    def Center(self):
        return self._x, self._y

    def Radius(self):
        return self._r

    @staticmethod
    def FromNode(node):
        try:
            x = int(node.attrib.get('x'))
            y = int(node.attrib.get('y'))
            r = int(node.attrib.get('radius'))
            return Circle(x, y, r)
        except ValueError:
            pass
        return None

class Dpad(Button):
    def __init__(self, up, right, down, left):
        super(Dpad, self).__init__(BUTTON_DPAD)
        self._up = up
        self._right = right
        self._down = down
        self._left = left

    def Directions(self):
        return self._up, self._right, self._down, self._left

    @staticmethod
    def FromNode(node):
        buttons = [ ]
        for button_child in node:
            button = Button.FromNode(button_child)
            if button:
                buttons.append(button)

        up = None
        right = None
        down = None
        left = None
        if len(buttons) == 4:
            for i in range(len(buttons)):
                if up is None or buttons[i].Center()[1] < up.Center()[1]:
                    up_index = i
                    up = buttons[i]
            buttons = buttons[0 : up_index] + buttons[up_index + 1 : ]

            for i in range(len(buttons)):
                if right is None or buttons[i].Center()[0] > right.Center()[0]:
                    right_index = i
                    right = buttons[i]
            buttons = buttons[0 : right_index] + buttons[right_index + 1 : ]

            for i in range(len(buttons)):
                if down is None or buttons[i].Center()[1] > down.Center()[1]:
                    down_index = i
                    down = buttons[i]
            buttons = buttons[0 : down_index] + buttons[down_index + 1 : ]

            left = buttons[0]

            return Dpad(up, right, down, left)
        return None

