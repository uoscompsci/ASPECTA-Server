import datetime
import math
from ConfigParser import SafeConfigParser
from bezier import *
from straightcoons import *

class cursor:
    __slots__ = ['id', 'loc', 'stateL', 'stateM', 'stateR', 'downTimeL', 'downTimeR', 'downTimeM', 'rotaton']

    def __init__(self, x, y):
        #self.loc=point2D(x,y)
        self.stateL = "up"
        self.stateM = "up"
        self.stateR = "up"
        self.loc = point2D(x,y)
        self.rotation = 0

    def moveX(self, distance):
        if(self.rotation==0):
            self.loc.setX(self.loc.getX()+int(distance))
        elif(self.rotation==180):
            self.loc.setX(self.loc.getX()-int(distance))
        elif(self.rotation==90):
            self.loc.setY(self.loc.getY()-int(distance))
        elif(self.rotation==270):
            self.loc.setY(self.loc.getY()+int(distance))
        elif(self.rotation>0 and self.rotation<90):
            radians = math.radians(self.rotation)
            ydist = -math.sin(radians)*int(distance)
            xdist = math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>90 and self.rotation<180):
            radians = math.radians(self.rotation-90)
            xdist = -math.sin(radians)*int(distance)
            ydist = -math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>180 and self.rotation<270):
            radians = math.radians(self.rotation-180)
            ydist = math.sin(radians)*int(distance)
            xdist = -math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>270):
            radians = math.radians(self.rotation-270)
            xdist = math.sin(radians)*int(distance)
            ydist = math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
            
    def testMoveX(self, distance):
        if(self.rotation==0):
            return (int(distance),0)
        elif(self.rotation==180):
            return (-int(distance),0)
        elif(self.rotation==90):
            return (0,-int(distance))
        elif(self.rotation==270):
            return (0,int(distance))
        elif(self.rotation>0 and self.rotation<90):
            radians = math.radians(self.rotation)
            ydist = -math.sin(radians)*int(distance)
            xdist = math.cos(radians)*int(distance)
            return (xdist, ydist)
        elif(self.rotation>90 and self.rotation<180):
            radians = math.radians(self.rotation-90)
            xdist = -math.sin(radians)*int(distance)
            ydist = -math.cos(radians)*int(distance)
            return (xdist,ydist)
        elif(self.rotation>180 and self.rotation<270):
            radians = math.radians(self.rotation-180)
            ydist = math.sin(radians)*int(distance)
            xdist = -math.cos(radians)*int(distance)
            return (xdist,ydist)
        elif(self.rotation>270):
            radians = math.radians(self.rotation-270)
            xdist = math.sin(radians)*int(distance)
            ydist = math.cos(radians)*int(distance)
            return (xdist,ydist)

    def moveY(self, distance):
        if(self.rotation==0):
            self.loc.setY(self.loc.getY()+int(distance))
        elif(self.rotation==180):
            self.loc.setY(self.loc.getY()-int(distance))
        elif(self.rotation==90):
            self.loc.setX(self.loc.getX()+int(distance))
        elif(self.rotation==270):
            self.loc.setX(self.loc.getX()-int(distance))
        elif(self.rotation>0 and self.rotation<90):
            radians = math.radians(self.rotation)
            xdist = math.sin(radians)*int(distance)
            ydist = math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>90 and self.rotation<180):
            radians = math.radians(self.rotation-90)
            ydist = -math.sin(radians)*int(distance)
            xdist = math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>180 and self.rotation<270):
            radians = math.radians(self.rotation-180)
            xdist = -math.sin(radians)*int(distance)
            ydist = -math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
        elif(self.rotation>270):
            radians = math.radians(self.rotation-270)
            ydist = math.sin(radians)*int(distance)
            xdist = -math.cos(radians)*int(distance)
            self.loc.setX(self.loc.getX()+xdist)
            self.loc.setY(self.loc.getY()+ydist)
            
    def testMoveY(self, distance):
        if(self.rotation==0):
            return (0,int(distance))
        elif(self.rotation==180):
            return (0,-int(distance))
        elif(self.rotation==90):
            return (int(distance),0)
        elif(self.rotation==270):
            return (-int(distance),0)
        elif(self.rotation>0 and self.rotation<90):
            radians = math.radians(self.rotation)
            xdist = math.sin(radians)*int(distance)
            ydist = math.cos(radians)*int(distance)
            return (xdist,ydist)
        elif(self.rotation>90 and self.rotation<180):
            radians = math.radians(self.rotation-90)
            ydist = -math.sin(radians)*int(distance)
            xdist = math.cos(radians)*int(distance)
            return (xdist,ydist)
        elif(self.rotation>180 and self.rotation<270):
            radians = math.radians(self.rotation-180)
            xdist = -math.sin(radians)*int(distance)
            ydist = -math.cos(radians)*int(distance)
            return (xdist,ydist)
        elif(self.rotation>270):
            radians = math.radians(self.rotation-270)
            ydist = math.sin(radians)*int(distance)
            xdist = -math.cos(radians)*int(distance)
            return (xdist,ydist)

    def move(self, xdist, ydist):
        self.moveX(xdist)
        self.moveY(ydist)
        
    def getX(self):
        return self.loc.getX()

    def getY(self):
        return self.loc.getY()
        
    def testMove(self, xdist, ydist):
        dists1 = self.testMoveX(xdist)
        dists2 = self.testMoveY(ydist)
        return (self.getX()+dists1[0]+dists2[0],self.getY()+dists1[1]+dists2[1])

    def setX(self, loc):
        self.loc.setX(float(loc))

    def setY(self, loc):
        self.loc.setY(float(loc))

    def setLoc(self, xloc, yloc):
        self.setX(xloc)
        self.setY(yloc)

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
        
    def getRotation(self):
        return self.rotation
    
    def rotateClockwise(self, degrees):
        self.rotation = self.rotation + int(degrees)
        if(self.rotation>=360):
            self.rotation = self.rotation%360
            
    def rotateAnticlockwise(self, degrees):
        self.rotation = self.rotation - int(degrees)
        if(self.rotation<0):
            self.rotation = self.rotation%360

class window:
    __slots__ = ['elements', 'loc', 'xsize', 'ysize', 'subwindows', 'name', 'windowID', 'owner', 'app', 'appno', 'subscribers', 'adminMode']

    def __init__(self, owner, app, appno, xloc, yloc, xsize, ysize, name):
        self.loc = point2D(xloc,yloc)
        self.xsize = int(xsize)
        self.ysize = int(ysize)
        self.name = name
        self.elements = []
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = [owner]
        self.adminMode = False
        
    def subscribe(self, app):
        if(app in self.subscribers==False):
            self.subscribers.append(app)
        
    def getID(self):
        return self.windowID
    
    def setID(self, ID):
        self.windowID = ID
        
    def getOwner(self):
        return self.owner
    
    def getAppDetails(self):
        return (self.app,self.appno)

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

    #location of a window is the coordinate of its top-left point on its parent window/surface
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
        popped = False
        for x in range(0, len(self.elements)):
            if(popped==False):
                if(self.elements[x]==elementNo):
                    self.elements.pop(x)
                    popped=True
    
    def containsEle(self, elementNo):
        found = False
        for x in range(0, len(self.elements)):
            if(int(self.elements[x])==int(elementNo)):
                found = True
        return found
    
    def getElements(self):
        return self.elements
    
    def becomeAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = True
            return True
        else:
            return False
        
    def stopBeingAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = False
            return True
        else:
            return False

class surface():
    __slots__ = ['toLeft', 'toRight', 'above', 'below', 'cursors', 'windows', 'surfaceID', 'owner', 'app', 'appno', 'subscribers', 'adminMode', 'curveResolution', 'meshPoints', 'defined']

    def __init__(self, owner, app, appno):
        self.cursors = []
        self.windows = []
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        self.defined = False
        
    def setPoints(self, topPoints, bottomPoints, leftPoints, rightPoints):
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.curveResolution = parser.getint('surfaces','curveResolution')
        ccalc = coonsCalc(topPoints[0],topPoints[len(topPoints)-1],bottomPoints[len(bottomPoints)-1],bottomPoints[0],topPoints,bottomPoints,leftPoints,rightPoints)
        self.meshPoints = ccalc.getCoonsPoints(self.curveResolution,self.curveResolution)
        self.defined = True
        
    def subscribe(self, app):
        if(app in self.subscribers==False):
            self.subscribers.append(app)
        
    def getID(self):
        return self.surfaceID
    
    def setID(self, ID):
        self.surfaceID = ID
        
    def getOwner(self):
        return self.owner
    
    def getAppDetails(self):
        return (self.app,self.appno)

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
    
    def getCursors(self):
        return self.cursors
    
    def getWindows(self):
        return self.windows
    
    def becomeAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = True
            return True
        else:
            return False
        
    def stopBeingAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = False
            return True
        else:
            return False
        
    def isDefined(self):
        return self.defined
    
    def undefine(self):
        self.defined = False
        
class element:
    __slots__ = ['elementType', 'visible', 'elementID', 'owner', 'app', 'appno', 'subscribers', 'adminMode']

    def subscribe(self, app):
        if(app in self.subscribers==False):
            self.subscribers.append(app)
    
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        
    def isVisible(self):
        return self.visible

    def checkType(self):
        return self.elementType
    
    def getID(self):
        return self.elementID
    
    def setID(self, ID):
        self.elementID = ID
        
    def getOwner(self):
        return self.owner
    
    def getAppDetails(self):
        return (self.app,self.appno)
    
    def becomeAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = True
            return True
        else:
            return False
        
    def stopBeingAdmin(self, app, appno):
        if(app==self.app and str(appno)==str(self.appno)):
            self.adminMode = False
            return True
        else:
            return False

class circle(element):
    __slots__ = ['coord', 'radius', 'lineColor', 'fillColor', 'sides']

    def __init__(self, owner, app, appno, x, y, radius, lineColor, fillColor, sides):
        self.elementType = "circle"
        self.coord = point2D(x,y)
        self.radius = radius
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.visible=True
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        self.sides = int(sides)

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
    
    def getSides(self):
        return self.sides
    
    def setSides(self, sides):
        self.sides = int(sides)

class line(element):
    __slots__ = ['coord1', 'coord2', 'color', 'width']

    def __init__(self, owner, app, appno, x1, y1, x2, y2, color, width):
        self.elementType = "line"
        self.coord1 = point2D(x1,y1)
        self.coord2 = point2D(x2,y2)
        self.color = color
        self.visible=True
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        self.width = width

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
    
    def getWidth(self):
        return self.width
    
    def setWidth(self, width):
        self.width = width

class lineStrip(element):
    __slots__ = ['points', 'color', 'width']

    def __init__(self, owner, app, appno, x, y, color, width):
        self.elementType = "lineStrip"
        self.points = [point2D(x,y)]
        self.color = color
        self.visible=True
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        self.width = width

    def addPoint(self, x, y):
        self.points.append(point2D(x,y))
        
    def addPointAt(self, x, y, index):
        self.points.insert(index, point2D(x,y))
        
    def getPointX(self, number):
        return self.points[int(number)].getX()
    
    def getPointY(self, number):
        return self.points[int(number)].getY()

    def setPoint(self, number, x, y):
        self.points[int(number)].reposition(x, y)

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color
        
    def getWidth(self):
        return self.width
    
    def setWidth(self, width):
        self.width = width
        
    def getNumPoints(self):
        return len(self.points)
    
    def setContent(self, content):
        self.points = []
        split1 = content.split(";")
        for x in range(0,len(split1)):
            split2 = split1[x].split(":")
            self.points.append(point2D(split2[0],split2[1]))

class polygon(element):
    __slots__ = ['points', 'lineColor', 'fillColor']

    def __init__(self, owner, app, appno, x, y, lineColor, fillColor):
        self.elementType = "polygon"
        self.points = [point2D(x,y)]
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.visible=True
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        
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
    
class rectangle(element):
    __slots__ = ['topLeft', 'width', 'height', 'lineColor', 'fillColor']
    
    def __init__(self, owner, app, appno, tlx, tly, width, height, lineColor, fillColor):
        self.elementType = "rectangle"
        self.topLeft = point2D(tlx,tly)
        self.width = width
        self.height = height
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False
        
    def getTopLeftX(self):
        return self.topLeft.getX()
    
    def getTopLeftY(self):
        return self.topLeft.getY()
    
    def setTopLeft(self,x,y):
        return self.topLeft.reposition(x,y)
    
    def getTopRightX(self):
        return self.topLeft.getX()+int(width)
    
    def getTopRightY(self):
        return self.topLeft.getY()
    
    def getBottomRightX(self):
        return self.topLeft.getX()+int(width)
    
    def getBottomRightY(self):
        return self.topLeft.getY()+int(height)
    
    def getBottomLeftX(self):
        return self.topLeft.getX()
    
    def getBottomLeftY(self):
        return self.topLeft.getY()+int(height)
    
    def setWidth(self, width):
        self.width = width
    
    def getWidth(self):
        return self.width
    
    def setHeight(self, height):
        self.height = height
    
    def getHeight(self):
        return self.height
    
    def setLineColor(self, color):
        self.lineColor = color

    def getLineColor(self):
        return self.lineColor

    def setFillColor(self, color):
        self.fillColor = color

    def getFillColor(self):
        return self.fillColor
    
class textBox(element):
    __slots__ = ['text', 'coord', 'pt', 'font', 'color']

    def __init__(self, owner, app, appno, text, x, y, pt, font, color):
        self.elementType = "text"
        self.text = text
        self.coord = point2D(x,y)
        self.pt = int(pt)
        self.font = font
        self.color = color
        self.visible=True
        self.owner = owner
        self.app = app
        self.appno = appno
        self.subscribers = []
        self.adminMode = False

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def setLocation(self, x, y):
        self.coord.reposition(x,y)

    def getLocationX(self):
        return self.coord.getX()
    
    def getLocationY(self):
        return self.coord.getY()

    def setPt(self, size):
        self.pt = int(size)

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
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

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
