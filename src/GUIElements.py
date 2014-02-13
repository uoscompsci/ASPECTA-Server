import datetime

class cursor:
    __slots__ = ['id', 'loc', 'stateL', 'stateM', 'stateR', 'downTimeL', 'downTimeR', 'downTimeM']

    def __init__(self, x, y):
        #self.loc=point2D(x,y)
        self.stateL = "up"
        self.stateM = "up"
        self.stateR = "up"
        self.loc = point2D(x,y)

    def moveX(self, distance):
        self.loc.setX(self.loc.getX()+int(distance))


    def moveY(self, distance):
        self.loc.setY(self.loc.getY()+int(distance))

    def move(self, xdis, ydis):
        self.moveX(xdis)
        self.moveY(ydis)

    def setX(self, loc):
        self.loc.setX(int(loc))

    def setY(self, loc):
        self.loc.setY(int(loc))

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
    __slots__ = ['elements', 'loc', 'xsize', 'ysize', 'subwindows', 'name']

    def __init__(self, xloc, yloc, xsize, ysize, name):
        self.loc = point2D(xloc,yloc)
        self.xsize = int(xsize)
        self.ysize = int(ysize)
        self.name = name
        self.elements = []

    def stretchLeft(self, distance):
        self.loc.setX(self.loc.getX()-int(distance))
        self.xsize = self.xsize+int(distance)

    def stretchRight(self, distance):
        self.xsize = self.xsize+int(distance)

    def stretchUp(self, distance):
        self.loc.setY(self.loc.getY()-int(distance))
        self.ysize = self.ysize+int(distance)

    def stretchDown(self, distance):
        self.ysize = self.ysize+int(distance)

    def dragX(self, xdist):
        self.loc.setX(int(self.loc.getX())+int(xdist))

    def dragY(self, ydist):
        self.loc.setY(int(self.loc.getY())+int(ydist))

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

    def getX(self):
        return self.loc.getX()
    
    def getY(self):
        return self.loc.getY()
    
    def setWidth(self, width):
        self.xsize = width
        
    def setHeight(self, height):
        self.ysize = height
        
    def getWidth(self):
        return self.xsize
    
    def getHeight(self):
        return self.ysize
    
    def setName(self,name):
        self.name=name
        
    def getName(self):
        return self.name
    
    def addElement(self,elementNo):
        self.elements.append(elementNo)
        
    def removeElement(self, elementNo):
        for x in range(0, len(self.elements)):
            if(self.elements[x]==elementNo):
                self.elements.pop(x)
    
    def containsEle(self, elementNo):
        found = False
        for x in range(0, len(self.elements)):
            if(int(self.elements[x])==int(elementNo)):
                found = True
        return found

class surface():
    __slots__ = ['toLeft', 'toRight', 'above', 'below', 'cursors', 'windows']

    def __init__(self):
        self.cursors = []
        self.windows = []

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
    
    def addCursor(self, cursorNo):
        self.cursors.append(cursorNo)
        
    def removeCursor(self, cursorNo):
        for x in range(0, len(self.cursors)):
            if(self.cursors[x]==cursorNo):
                self.cursors.pop(x)
    
    def containsCur(self, cursorNo):
        found = False
        for x in range(0, len(self.cursors)):
            if(int(self.cursors[x])==int(cursorNo)):
                found = True
        return found
    
    def addWindow(self, windowNo):
        self.windows.append(windowNo)
        
    def removeWindow(self, windowNo):
        for x in range(0, len(self.windows)):
            if(self.windows[x]==windowNo):
                self.windows.pop(x)
    
    def containsWin(self, windowNo):
        found = False
        for x in range(0, len(self.windows)):
            if(int(self.windows[x])==int(windowNo)):
                found = True
        return found
        
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

    def __init__(self, x, y, radius, lineColor, fillColor):
        self.elementType = "circle"
        self.coord = point2D(x,y)
        self.radius = radius
        self.lineColor = lineColor
        self.fillColor = fillColor

    def getCenterX(self):
        return self.coord.getX()
    
    def getCenterY(self):
        return self.coord.getY()
    
    def setCenterX(self,x):
        self.coord.setX(x)
        
    def setCenterY(self,y):
        self.coord.setY(y)

    def setCenter(self, x, y):
        self.setCenterX(x)
        self.setCenterY(y)

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

    def __init__(self, x1, y1, x2, y2, color):
        self.elementType = "line"
        self.coord1 = point2D(x1,y1)
        self.coord2 = point2D(x2,y2)
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

    def __init__(self, x, y, color):
        self.elementType = "lineStrip"
        self.points = [point2D(x,y)]
        self.color = color

    def addPoint(self, x, y):
        self.points.append(point2D(x,y))

    def getPointX(self, number):
        return self.points[int(number)-1].getX()
    
    def getPointY(self, number):
        return self.points[int(number)-1].getY()

    def setPoint(self, number, x, y):
        self.points[int(number)-1].reposition(x, y)

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color
        
    def getNumPoints(self):
        return len(self.points)

class polygon(element):
    __slots__ = ['points', 'lineColor', 'fillColor']

    def __init__(self, x, y, lineColor, fillColor):
        self.elementType = "polygon"
        self.points = [point2D(x,y)]
        self.lineColor = lineColor
        self.fillColor = fillColor
        
    def addPoint(self, x, y):
        self.points.append(point2D(x,y))

    def getPointX(self, number):
        return self.points[int(number)-1].getX()
    
    def getPointY(self, number):
        return self.points[int(number)-1].getY()

    def setPoint(self, number, x, y):
        self.points[number-1].reposition(x, y)

    def getNumPoints(self):
        return len(self.points)
    
    def setLineColor(self, color):
        self.lineColor = color

    def getLineColor(self):
        return self.lineColor

    def setFillColor(self, color):
        self.fillColor = color

    def getFillColor(self):
        return self.fillColor

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
        self.x = int(x)
        self.y = int(y)

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
