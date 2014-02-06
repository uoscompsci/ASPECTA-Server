import datetime

class cursor:
    __slots__ = ['id', 'loc', 'stateL', 'stateM', 'stateR', 'downTimeL', 'downTimeR', 'downTimeM']

    def __init__(self, x, y):
        self.loc.setX(x)
        self.loc.setY(y)
        self.stateL = "up"
        self.stateM = "up"
        self.stateR = "up"

    def moveX(self, distance):
        self.loc.setX(self.loc.getX()+distance)


    def moveY(self, distance):
        self.loc.setY(self.loc.getY()+distance)

    def move(self, xdis, ydis):
        self.moveX(xdis)
        self.moveY(ydis)

    def setX(self, loc):
        self.loc.setX(loc)

    def setY(self, loc):
        self.loc.setY(loc)

    def setLoc(self, xloc, yloc):
        self.setX(xloc)
        self.setY(yloc)

    def getX(self):
        return self.loc.getX()

    def getY(self):
        return self.loc.getY()

    def getStateL(self):
        return self.stateL

    def getStateR(self):
        return self.stateR

    def getStateM(self):
        return self.stateM

    def setStateLUp(self):
        self.stateL = "Up"
        now = datetime.datetime.now()
        clickTime = (now-self.downTimeL).total_seconds()
        return clickTime

    def setStateRUp(self):
        self.stateR = "Up"
        now = datetime.datetime.now()
        clickTime = (now-self.downTimeR).total_seconds()
        return clickTime

    def setStateMUp(self):
        self.stateM = "Up"
        now = datetime.datetime.now()
        clickTime = (now-self.downTimeM).total_seconds()
        return clickTime
        
    def setStateLDown(self):
        self.downTimeL=datetime.datetime.now()
        self.stateL = "Down"

    def setStateRDown(self):
        self.downTimeR=datetime.datetime.now()
        self.stateR = "Down"

    def setStateMDown(self):
        self.downTimeM=datetime.datetime.now()
        self.stateM = "Down"

class window:
    __slots__ = ['elements', 'loc', 'xsize', 'ysize', 'subwindows', 'name', 'type']

    def __init__(self, xloc, yloc, xsize, ysize, name):
        self.type = "window"
        self.loc.setX(xloc)
        self.loc.setY(yloc)
        self.xsize = xsize
        self.ysize = ysize
        self.name = name

    def stretchLeft(self, distance):
        self.loc.setX(self.loc.getX()-distance)
        self.xsize = self.xsize+distance

    def stretchRight(self, distance):
        self.xsize = self.xsize+distance

    def stretchUp(self, distance):
        self.loc.setY(self.loc.getY()-distance)
        self.ysize = self.ysize+distance

    def stretchDown(self, distance):
        self.ysize = self.ysize+distance

    def dragX(self, xdist):
        self.loc.setX(self.loc.getX()+xdist)

    def dragY(self, ydist):
        self.loc.setY(self.loc.getY()+ydist)

    def drag(self, xdist, ydist):
        self.dragX(xdist)
        self.dragY(ydist)

    def setXLoc(self, xloc):
        self.loc.setX(xloc)

    def setYLoc(self, yloc):
        self.loc.setY(yloc)

    #location of a window is the coordinate of its top-left point on its superwindow
    def setLoc(self, xloc, yloc):
        self.setXLoc(xloc)
        self.setYLoc(yloc)

    #elements and subwindows

class surface(window):
    __slots__ = ['toLeft', 'toRight', 'above', 'below']

    def __init__(self):
        self.type = "surface"

    def setLeft(self, surface):
        self.toLeft = surface

    def getLeft(self):
        return self.toLeft

    def setRight(self, surface):
        self.toRight = surface

    def getRight(self):
        return self.toRight

    def setUp(self, surface):
        self.above = surface

    def getUp(self):
        return self.above

    def setDown(self, surface):
        self.below = surface

    def getDown(self):
        return self.below

class element:
    __slots__ = ['elementType', 'visible']

    def show(self):
        self.visible = False

    def hide(self):
        self.visible = True

    def checkType(self):
        return self.elementType

class circle(element):
    __slots__ = ['coord', 'radius', 'lineColor', 'fillColor']

    def __init__(self, coord, radius, lineColor, fillColor):
        self.elementType = "circle"
        self.coord = coord
        self.radius = radius
        self.lineColor = lineColor
        self.fillColor = fillColor

    def getCenter(self):
        return self.coord

    def setCenter(self, coord):
        self.coord = coord

    def getRadius(self):
        return self.radius

    def setRadius(self, rad):
        self.radius = rad

    def setLineColor(self, color):
        self.lineColor = color

    def getLineColor(self):
        return self.lineColor

    def setFillColor(self, color):
        self.fillColor = color

    def getFillColor(self):
        return self.fillColor

class line(element):
    __slots__ = ['coord1', 'coord2', 'color']

    def __init__(self, coord1, coord2, color):
        self.elementType = "line"
        self.coord1 = coord1
        self.coord2 = coord2
        self.color = color

    def setStart(self, x, y):
        self.coord1.reposition(x,y)

    def setEnd(self, x, y):
        self.coord2.reposition(x,y)

    def getStartX(self):
        return self.coord1.getX()

    def getStartY(self):
        return self.coord1.getY()

    def getEndX(self):
        return self.coord2.getX()

    def getEndY(self):
        return self.coord2.getY()

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

class lineStrip(element):
    __slots__ = ['points', 'color']

    def __init__(self, point, color):
        self.points = [point]
        self.color = color

    def addPoint(self, point):
        self.points.append(point)

    def getPoint(self, number):
        return self.points[number-1]

    def setPoint(self, number, x, y):
        self.points[number-1].reposition(x, y)

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

class polygon(element):
    __slots__ = ['points', 'lineColor', 'fillColor']

    def __init__(self, points, lineColor, fillColor):
        self.points = points
        self.lineColor = lineColor
        self.fillColor = fillColor

    def setLineColor(self, color):
        self.lineColor = color

    def getLineColor(self):
        return self.lineColor

    def setFillColor(self, color):
        self.fillColor = color

    def getFillColor(self):
        return self.fillColor

    def getPoint(self, number):
        return self.points[number-1]

    def setPoint(self, number, x, y):
        self.points[number-1].reposition(x, y)

    def getNumPoints(self):
        return len(self.points)

class text(element):
    __slots__ = ['text', 'coord', 'pt', 'font', 'color']

    def __init__(self, text, coord, pt, font, color):
        self.elementType = "text"
        self.text = text
        self.coord = coord
        self.pt = pt
        self.font = font
        self.color = color

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def setLocation(self, x, y):
        self.coord.reposition(x,y)

    def getLocation(self):
        return self.coord

    def setPt(self, size):
        self.pt = size

    def getPt(self):
        return self.pt

    def setFont(self, font):
        self.font = font

    def getFont(self):
        return self.font

    def setColor(self,color):
        self.color = color

    def getColor(self):
        return self.color

class point2D:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def reposition(self, x, y):
        self.setX(x)
        self.setY(y)
