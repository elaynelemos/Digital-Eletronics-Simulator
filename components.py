"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
*   Atividade: pt-br/ este código parametriza os elementos entrada (Entry), porta (Gate) e conector (Wire) 
*                     do simulador de eletrônica digital enquanto define a manipulação básica.
*              en-us/ this code parametrize the elements Entry, Gate and Wire of the digital eletronics
*                     simulator while defines the basic manipulation of it.
*
"""

from __future__ import annotations

from typing import List
from operator import xor
from util import *
# import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

RELATIVE_GATEIN_X = 0
RELATIVE_GATEIN_Y = 0
RELATIVE_GATEOUT_X = 0
RELATIVE_GATEOUT_Y = 0

ORIENTATION_LR = 0
ORIENTATION_UD = 1
ORIENTATION_RL = 2
ORIENTATION_DU = 3
N_ENTRIES = 2

GATE_TYPE_NOT = 0
GATE_TYPE_OR = 1
GATE_TYPE_AND = 2
GATE_TYPE_XOR = 3
GATE_TYPE_NOR = 4
GATE_TYPE_NAND = 5
GATE_TYPE_XNOR = 6

COLOR_TRUE = Color(r=192.0/255)
COLOR_FALSE = Color(b=192.0/255)

"""COMPONENT CLASSES > look at Coords, stopped there
"""

# Entry: Represents a logic entry. It has a value itself.
#       Then cannot be connected to other entries (only outputs its own value).


class Entry(Element):
    # the attributes (private) only can be reached by getters and setters.
    __value: bool = None
    __coords: Coords = None
    __orientation = ORIENTATION_LR
    __size = POINT_SPACE*4

    # the constructor of Entry receives a logic value and the Coords where the entry should be placed.
    def __init__(self, coords: Coords = Coords(0.0, 0.0)) -> None:
        super().__init__()
        self.setCoords(coords)

    def getValue(self) -> bool:
        return self.__value

    def getCoords(self) -> Coords:
        return self.__coords

    def setValue(self, value: bool) -> bool:  # returns True if succeeds.
        try:
            if not(isinstance(value, bool)):
                raise ValueError(
                    "ValueError: Logic value expected to entry. You entered a(n): ", type(value))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__value = value
            return True

    def toogleV(self) -> bool:
        try:
            if self.__value is not None:
                self.__value = xor(self.__value, True)
                return True
            else:
                raise AttributeError("Entry value not defined!")
        except AttributeError as ae:
            print(ae)
            return False

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

    def draw(self):
        # line
        c = line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*3/4)
        d = line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*1/4, l=True)

        # Polygon
        if self.__value:
            COLOR_TRUE.apply()
        else:
            COLOR_FALSE.apply()

        glBegin(GL_POLYGON)
        rect_around(c, 1/4*self.__size, p=3-self.__orientation)
        d.apply()
        glEnd()

        # bord
        COLOR_STROKE.apply()
        glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINE_LOOP)
        rect_around(c, 1/4*self.__size, p=3-self.__orientation)
        d.apply()
        glEnd()

        # number
        if self.__value:
            digit_around(c, 1/4*0.6*self.__size, 1)
        else:
            digit_around(c, 1/4*0.6*self.__size, 0)

        # self.getCoords().draw()

        return self


class Checker(Element):
    # the attributes (private) only can be reached by getters and setters.
    __value: bool = None
    __coords: Coords = None
    __orientation = ORIENTATION_RL
    __size = POINT_SPACE*3

    # the constructor of Entry receives a logic value and the Coords where the entry should be placed.
    def __init__(self, coords: Coords = Coords(0.0, 0.0)) -> None:
        super().__init__()
        self.setCoords(coords)

    def getValue(self) -> bool:
        return self.__value

    def getCoords(self) -> Coords:
        return self.__coords

    def setValue(self, value: bool) -> bool:  # returns True if succeeds.
        try:
            if not(isinstance(value, bool)):
                raise ValueError(
                    "ValueError: Logic value expected to entry. You entered a(n): ", type(value))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__value = value
            return True

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

    def draw(self):

        # line
        c = line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*2/3, l=True)

        # Polygon
        if self.__value:
            COLOR_TRUE.apply()
        else:
            COLOR_FALSE.apply()

        glBegin(GL_POLYGON)
        rect_around(c, 1/3*self.__size, p=3-self.__orientation)
        glEnd()

        # bord
        COLOR_STROKE.apply()
        glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINE_LOOP)
        rect_around(c, 1/3*self.__size, p=3-self.__orientation)
        glEnd()

        # number
        if self.__value:
            digit_around(c, 1/3*0.6*self.__size, 1)
        else:
            digit_around(c, 1/3*0.6*self.__size, 0)

        # self.getCoords().draw()

        return self


class Display(Element):
    __checks = [None]*4
    __coords: Coords = None
    __fill: Color = Color()
    __ligh_on: Color = Color(r=1.0)
    __ligh_off: Color = Color(r=0.2)
    __orientation = ORIENTATION_RL
    __size = POINT_SPACE*4

    def __init__(self, coords: Coords = Coords(0.0, 0.0)):
        self.setCoords(coords)
        c = Coords(0.0, 0.0)
        for i in range(4):
            self.__checks[i] = Checker()
            # definindo a rotação do componente
            if self.__orientation % 2 == 0:  # LR or RL
                self.__checks[i].setCoords(c.sum(Coords(self.__size*1/2, -self.__size*3/8 + i*self.__size*1/4)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*1/2, -self.__size*3/8 + i*self.__size*1/4)))
            else:                       # UD or DU
                self.__checks[i].setCoords(c.sum(Coords(-self.__size*3/8 + i*self.__size*1/4, self.__size*1/2)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*3/8 + i*self.__size*1/4, -self.__size*1/2)))

    def getCheck(self, i: int):
        if(i < 4 and i >= 0):
            return self.__checks[i]
        return None

    def setCheck(self, i: int, v: bool):
        if(i < 4 and i >= 0):
            self.__checks[i].setValue(v)
        return self

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

        c = Coords(0.0, 0.0)
        for i in range(4):
            # definindo a rotação do componente
            if self.__orientation % 2 == 0:  # LR or RL
                self.__checks[i].setCoords(c.sum(Coords(self.__size*1/2, -self.__size*3/8 + i*self.__size*1/4)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*1/2, -self.__size*3/8 + i*self.__size*1/4)))
            else:                       # UD or DU
                self.__checks[i].setCoords(c.sum(Coords(-self.__size*3/8 + i*self.__size*1/4, self.__size*1/2)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*3/8 + i*self.__size*1/4, -self.__size*1/2)))

    def draw(self):
        v = 0
        for i in range(4):
            v += (2**i)*(1 if self.__checks[i].getValue() else 0)

        # Rect

        self.__fill.apply()
        glBegin(GL_POLYGON)
        rect_around(self.__coords, (self.__size/4 if self.__orientation % 2 == 0 else self.__size *
                                    1/2), (self.__size*1/2 if self.__orientation % 2 == 0 else self.__size/4))
        glEnd()

        # OFF Digit
        self.__ligh_off.apply()
        digit_around(self.__coords, self.__size *
                     (0.9 if self.__orientation % 2 == 0 else 0.5)/3, 8)

        # ON Digit
        self.__ligh_on.apply()
        digit_around(self.__coords, self.__size *
                     (0.9 if self.__orientation % 2 == 0 else 0.5)/3, v)

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.__coords.glTranslate()

        for i in self.__checks:
            line_orientation(i.getCoords(), self.__orientation, l=True)
        glPopMatrix()


# Gate: Represents the main logic gates (or, and, xor, nor, nand) those must receives a pair of
#      logic values and are able to output its interpretation.
class Gate(Element):
    id: int = 0
    # the attributes (private) only can be reached by getters and setters.
    __gatetype: int = None
    __entry: List[Entry] = []
    __coords: Coords = None
    __out: Coords = None

    __fill: Color = Color(r=1.0, g=0.9, b=0.8)
    __orientation = ORIENTATION_LR
    __size = POINT_SPACE*5

    # the constructor of Gate receives the gate type, two logic values and the Coords where it
    # should be placed.
    def __init__(self, gatetype: int, coords: Coords) -> None:
        # gate types: 0=not, 1=or, 2=and, 3=xor, 4=nor, 5=nand, 6=xnor
        self.setGateType(gatetype)
        self.setCoords(coords)  # position of the gate
        self.setName("G" + str(Gate.id))

    def getGateType(self) -> int:
        return self.__gatetype

    def getIn(self, i: int) -> Entry:
        try:
            if self.__entry is not None and len(self.__entry)>i and self.__entry[i] is not None:
                return self.__entry[i]
            else:
                raise AttributeError("Entry not defined!")
        except AttributeError as ae:
            print(ae)
            return None

    def getCoords(self) -> Coords:
        return self.__coords

    def getOutCoords(self) -> Coords:
        return self.__out

    def __updateCoords(self) -> Gate:
        self.__entry = []

        #If is not a Not Gate, then this will have two entries
        isntNot = False
        self.__entry.append(Entry())
        if self.__gatetype != GATE_TYPE_NOT:
            isntNot = True
            self.__entry.append(Entry())

        # Configures orientation
        if self.__orientation == ORIENTATION_LR:
            self.__out = self.__coords.sum(Coords(self.__size/2,0))
            self.__entry[0].setCoords(self.__coords.sum(Coords(-self.__size/2,0)))
            if isntNot:
                self.__entry[1].setCoords(self.__entry[0].getCoords().sum(Coords(0,+self.__size/5)))
                self.__entry[0].setCoords(self.__entry[0].getCoords().sum(Coords(0,-self.__size/5)))
        if self.__orientation == ORIENTATION_RL:
            self.__out = self.__coords.sum(Coords(-self.__size/2,0))
            self.__entry[0].setCoords(self.__coords.sum(Coords(self.__size/2,0)))
            if isntNot:
                self.__entry[1].setCoords(self.__entry[0].getCoords().sum(Coords(0,+self.__size/5)))
                self.__entry[0].setCoords(self.__entry[0].getCoords().sum(Coords(0,-self.__size/5)))
        if self.__orientation == ORIENTATION_UD:
            self.__out = self.__coords.sum(Coords(0,self.__size/2))
            self.__entry[0].setCoords(self.__coords.sum(Coords(0,-self.__size/2)))
            if isntNot:
                self.__entry[1].setCoords(self.__entry[0].getCoords().sum(Coords(+self.__size/5,0)))
                self.__entry[0].setCoords(self.__entry[0].getCoords().sum(Coords(-self.__size/5,0)))
        if self.__orientation == ORIENTATION_DU:
            self.__out = self.__coords.sum(Coords(0,-self.__size/2))
            self.__entry[0].setCoords(self.__coords.sum(Coords(0,self.__size/2)))
            if isntNot:
                self.__entry[1].setCoords(self.__entry[0].getCoords().sum(Coords(+self.__size/5,0)))
                self.__entry[0].setCoords(self.__entry[0].getCoords().sum(Coords(-self.__size/5,0)))

        

    def setGateType(self, gatetype) -> bool:  # returns True if succeeds.
        try:
            # Type validation.
            if not(isinstance(gatetype, int)) or isinstance(gatetype, bool):
                raise ValueError(
                    "ValueError: integer expected to gate classification. You entered a(n): ", type(gatetype))
            elif gatetype < 0 or gatetype > 6:  # validation of gate classification.
                raise ValueError(
                    "ValueError: gate classification not defined! Expected between 1 and 5 including both. You entered", gatetype)
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__gatetype = gatetype
            self.__updateCoords()
            return True

    def setIn(self, entry) -> bool:  # returns True if succeeds.
        try:
            for i in entry:
                if i.getValue() is not None:
                    self.__entry.append(i)
                else:
                    raise ValueError(
                        "ValueError: Logic value expected to the gate entries. You entered a(n): ", type(i))
        except ValueError as ve:
            print(ve)
            self.__entry = []
            return False
        else:
            return True
    
    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation
        self.__updateCoords()


    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def gateOut(self) -> Entry:
        A = Entry(coords=self.__coords.sum(self.__out))

        if self.getGateType() == GATE_TYPE_NOT:
            A.setValue(not self.getIn(0).getValue())
        elif self.getGateType() == GATE_TYPE_OR:
            A.setValue(self.getIn(0).getValue() or self.getIn(1).getValue())
        elif self.getGateType() == GATE_TYPE_AND:
            A.setValue(self.getIn(0).getValue() and self.getIn(1).getValue())
        elif self.getGateType() == GATE_TYPE_XOR:
            A.setValue(self.getIn(0).getValue() != self.getIn(1).getValue())
        elif self.getGateType() == GATE_TYPE_NOR:
            A.setValue(not(self.getIn(0).getValue()
                           or self.getIn(1).getValue()))
        elif self.getGateType() == GATE_TYPE_NAND:
            A.setValue(not(self.getIn(0).getValue()
                           and self.getIn(1).getValue()))
        elif self.getGateType() == GATE_TYPE_XNOR:
            A.setValue(self.getIn(0).getValue() == self.getIn(1).getValue())
        return A

    def draw(self):
        if self.getGateType() == GATE_TYPE_NOT:
            pass

        if self.getGateType() == GATE_TYPE_AND or self.getGateType() == GATE_TYPE_NAND:
            pass
        elif self.getGateType() == GATE_TYPE_OR or self.getGateType() == GATE_TYPE_XOR or self.getGateType() == GATE_TYPE_NOR or self.getGateType() == GATE_TYPE_XNOR:
            pass
            if self.getGateType() == GATE_TYPE_XOR or self.getGateType() == GATE_TYPE_XNOR:
                pass

        if self.getGateType() == GATE_TYPE_NOT or self.getGateType() == GATE_TYPE_NOR or self.getGateType() == GATE_TYPE_NAND or self.getGateType() == GATE_TYPE_XNOR:
            pass

        return self


# Wire: Represents the connector of the logic circuit. It's defined as a list of unique
#      Coords. Once connected to an logic component carries its value from start to end points.
class Wire(Element):
    fill: Color = Color(g=64.0/255)
    # the attributes (private) only can be reached by getters and setters.
    __points: List[Coords] = []

    # the constructor of Wire receives a list of Coords (points) to define itself.
    def __init__(self, points: List[Coords]) -> None:
        super().__init__()
        self.insertWireP(points)

    # TODO #fix insertion function
    # returns true if points is correctly inserted.
    def insertWireP(self, points: List[Coords]) -> bool:
        ctrl = True
        try:
            for i in points:
                x = i.getX()
                y = i.getY()
                if x >= 0 and y >= 0:
                    for j in self.__points:
                        if j.getX() == x and j.getY() == y:
                            ctrl = False
                            break
                    if ctrl:
                        self.__points.append(i)
                    ctrl = True
            # self.refactorWire()
            # validation of condition to be a wire (line).
            if len(self.__points) < 2:
                raise AttributeError("Not enough points to a wire!")
        except AttributeError as ae:
            self.__points = []
            print(ae)
            return False
        else:
            return True

    def getWireP(self) -> List[Coords]:
        return self.__points

    def getWireStartP(self) -> Coords:
        return self.__points[0]

    def getWireEndP(self) -> Coords:
        l = len(self.__points)
        if l > 0:
            return self.__points[l-1]
        else:
            return self.__points[0]

    def getWireNextP(self, reference: Coords) -> Coords:
        for i in self.__points:
            if i.getX() == reference.getX() and i.getY() == reference.getY():
                return self.__points[self.__points.index(i) + 1]

    # TODO fix refactor function
    # reduce the number of points if they are at the same line.
    def refactorWire(self) -> None:
        ctrl = len(self.__points)-2
        i = 0
        while (ctrl - i):
            if self.__points[i].getX() == self.__points[i+1].getX() and self.__points[i].getX() == self.__points[i+2].getX():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1
        i = 0
        while (ctrl - i):
            if self.__points[i].getY() == self.__points[i+1].getY() and self.__points[i].getY() == self.__points[i+2].getY():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1

    def draw(self):
        return self


"""FUNCTIONS
"""
# Each is[Component](): verifies the respective data type of a component. Returns True if its correct.


def isEntry(component) -> bool:
    return isinstance(component, Entry)


def isGate(component) -> bool:
    return isinstance(component, Gate)


def isWire(component) -> bool:
    return isinstance(component, Wire)

# isEqualPoints(): receives two pairs of Coords and returns True if they have the same x and y.


def isEqualPoints(c1: Coords, c2: Coords) -> bool:
    if c1.getX() == c2.getX() and c1.getY() == c2.getY():
        return True
    return False

# wiredComponent(): receives an Wire and other component then verifies if the component is connected
#                  to the Wire begin or end (True if positive). Entry can only be connected to the
#                  Wire start point.


def wiredComponent(w: Wire, component) -> bool:
    if isGate(component) and (isEqualPoints(w.getWireStartP(), component.getCoords()) or isEqualPoints(w.getWireEndP(), component.getCoords())):
        return True
    elif isEntry(component) and isEqualPoints(w.getWireStartP(), component.getCoords()):
        return True
    else:
        return False

# connectedComponents(): to be connected the components c1 and c2 must be wired one at start and
#                       other to end of the Wire component.


def connectedComponents(w: Wire, c1, c2) -> bool:
    return (wiredComponent(w, c1) and wiredComponent(w, c2) and
            not(isEqualPoints(c1.getCoords(), c2.getCoords())))


"""
e = Wire([Coords(10,20),Coords(10,20),Coords(10,40),Coords(10,30)])
print(len(e.getWireP()))

e.refactorWire()
print(len(e.getWireP()))

print(e.getWireEndP().getY())

e.insertWireP([Coords(50,70)])

print(e.getWireEndP().getY())
"""

"""
    #basic test ahead
    e1 = Entry(False, Coords(10,20))
    e2 = Entry(False, Coords(10,30))
    w = Wire((Coords(10,20),Coords(50,20),Coords(10,20),Coords(90,40)))
    g = Gate(1, e1.getValue(), e2.getValue(), Coords(20,40))

    print(connectedComponents(w,e1,g))
"""

"""    def refactorWire(self) -> None: #reduce the number of points if they are at the same line.
        l = len(self.__coords)-3
        print(l)
        for i in range(l):
            if self.__coords[i].getX()==self.__coords[i+1].getX() and self.__coords[i].getX()==self.__coords[i+2].getX():
                self.__coords.pop(i+1)
                print(len(self.__coords))
        for i in range(l):
            if self.__coords[i].getY()==self.__coords[i+1].getY() and self.__coords[i].getY()==self.__coords[i+2].getY():
                self.__coords.pop(i+1)
                
"""
