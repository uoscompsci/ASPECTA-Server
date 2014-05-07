from GUIElements import *
import threading
from math import *

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur', 'lastsur', 'lastwin', 'lastele' 'windows', 'windows_lock', 'elements', 'elements_lock', 'setup_surface_visible']
	
	def __init__(self):
		self.lastcur = 0
		self.lastsur = 0
		self.lastwin = 0
		self.lastele = 0
		self.surfaces_lock = threading.Lock()
		self.displays_lock = threading.Lock()
		self.cursors_lock = threading.Lock()
		self.windows_lock = threading.Lock()
		self.elements_lock = threading.Lock()
		self.cursors = {}
		self.surfaces = {}
		self.windows = {}
		self.elements = {}
		self.surfaces["0"] = surface("server")
		self.setup_surface_visible = False
		
	def hideSetupSurface(self):
		self.setup_surface_visible = False
		
	def showSetupSurface(self):
		self.setup_surface_visible = True
		
	def getSetupSurfaceVisibilty(self):
		return self.setup_surface_visible
		
	def newSurface(self, owner):
		newSur = surface(owner)
		surfaceNo = 0
		with self.surfaces_lock:
			if (len(self.surfaces)==0):
				self.surfaces["1"] = newSur
				surfaceNo = 1
				self.lastsur = 1
			else:
				self.lastsur=self.lastsur+1
				self.surfaces[str(self.lastsur)] = newSur
				surfaceNo = self.lastsur		
		return surfaceNo
	
	def newSurfaceWithID(self, owner, ID):
		surfaceNo = self.newSurface(owner)
		self.surfaces[set(surfaceNo)].setID(ID)
		return surfaceNo
	
	def getSurfaceID(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getID()
	
	def setSurfaceID(self, surfaceNo, ID):
		self.surfaces[str(surfaceNo)].setID(ID)
		
	def getSurfaceOwner(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getOwner()

	def newCursor(self, surface, x, y):
		newCur = cursor(x,y)
		cursorNo = 0
		with self.cursors_lock:
			if (len(self.cursors)==0):
				self.cursors[str(1)] = newCur
				cursorNo = 1
				self.lastcur = 1
			else:
				self.lastcur=self.lastcur+1
				self.cursors[str(self.lastcur)] = newCur
				cursorNo = self.lastcur		
		self.surfaces[str(surface)].addCursor(cursorNo)
		return cursorNo
	
	def newCursorWithID(self, ID):
		cursorNo = self.newCursor()
		self.cursors[set(cursorNo)].setID(ID)
		return cursorNo
		
	def findCursor(self, cursorNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsCur(cursorNo)==True):
				location = int(key)
		return location
	
	def moveCursor(self, cursorNo, xDist, yDist):
		self.cursors[str(cursorNo)].move(xDist,yDist) #TODO Handle when moves to different screen
		
	def testMoveCursor(self, cursorNo, xDist, yDist):
		return self.cursors[str(cursorNo)].testMove(xDist,yDist) #TODO Handle when moves to different screen
		
	def rotateCursorClockwise(self,cursorNo,degrees):
		self.cursors[str(cursorNo)].rotateClockwise(degrees)
		
	def rotateCursorAnticlockwise(self,cursorNo,degrees):
		self.cursors[str(cursorNo)].rotateAnticlockwise(degrees)
		
	def getCursorRotation(self,cursorNo):
		return self.cursors[str(cursorNo)].getRotation()
		
	def setCursorPos(self, cursorNo, xLoc, yLoc, surface):
		self.cursors[str(cursorNo)].setLoc(xLoc,yLoc)
		origSur = self.findCursor(cursorNo)
		if(origSur != surface):
			self.surfaces[str(origSur)].removeCursor(cursorNo)
			self.surfaces[str(surface)].addCursor(cursorNo)
			
	def setCursorX(self, cursorNo, pos):
		self.cursors[str(cursorNo)].setX(pos)
		
	def setCursorY(self, cursorNo, pos):
		self.cursors[str(cursorNo)].setY(pos)
			
	def removeCursor(self,cursorNo):
		surNo = self.findCursor(cursorNo)
		self.surfaces[str(surNo)].removeCursor(cursorNo)
		self.cursors.pop(str(cursorNo),None)
		
	def leftDown(self, cursorNo):
		self.cursors[str(cursorNo)].setStateLDown()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc)

	def middleDown(self, cursorNo):
		self.cursors[str(cursorNo)].setStateMDown()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc)

	def rightDown(self, cursorNo):
		self.cursors[str(cursorNo)].setStateRDown()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc)

	def leftUp(self, cursorNo):
		secondsDown = self.cursors[str(cursorNo)].setStateLUp()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc,secondsDown)
	
	def middleUp(self, cursorNo):
		secondsDown = self.cursors[str(cursorNo)].setStateMUp()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc,secondsDown)

	def rightUp(self, cursorNo):
		secondsDown = self.cursors[str(cursorNo)].setStateRUp()
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc,secondsDown)
	
	def getCursorPos(self, cursorNo):
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc)
	
	def newWindow(self, owner, surface, x, y, xWid, yWid, name):
		newWin = window(owner,x,y,xWid,yWid,name)
		windowNo = 0
		with self.windows_lock:
			if (len(self.windows)==0):
				self.windows[str(1)] = newWin
				windowNo = 1
				self.lastwin = 1
			else:
				self.lastwin=self.lastwin+1
				self.windows[str(self.lastwin)] = newWin
				windowNo = self.lastwin
		self.surfaces[str(surface)].addWindow(windowNo)
		return windowNo
	
	def newWindowWithID(self, owner, ID, surface, x, y, xWid, yWid, name):
		windowNo = self.newWindow(owner, surface, x, y, xWid, yWid, name)
		self.windows[set(windowNo)].setID(ID)
		return windowNo
	
	def getWindowID(self, windowNo):
		return self.windows[str(windowNo)].getID()
	
	def setWindowID(self, windowNo, ID):
		self.windows[str(windowNo)].setID(ID)
		
	def getWindowOwner(self, windowNo):
		return self.windows[str(windowNo)].getOwner()
	
	def findWindow(self, windowNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsWin(windowNo)==True):
				location = int(key)
		return location
	
	def moveWindow(self, windowNo, xDist, yDist):
		self.windows[str(windowNo)].drag(xDist,yDist) #TODO Handle when moves to different screen
		
	def setWindowPos(self, windowNo, xLoc, yLoc, surface):
		self.windows[str(windowNo)].setLoc(xLoc,yLoc)
		origSur = self.findWindow(windowNo)
		if(origSur != surface):
			self.surfaces[str(origSur)].removeWindow(windowNo)
			self.surfaces[str(surface)].addWindow(windowNo)
			
	def removeWindow(self,windowNo):
		surNo = self.findWindow(windowNo)
		self.surfaces[str(surNo)].removeWindow(windowNo)
		self.windows.pop(str(windowNo),None)

	def setWindowHeight(self,windowNo,height):
		self.windows[str(windowNo)].setHeight(height)
		
	def setWindowWidth(self,windowNo,width):
		self.windows[str(windowNo)].setWidth(width)
		
	def getWindowHeight(self,windowNo):
		return self.windows[str(windowNo)].getHeight()
	
	def getWindowWidth(self,windowNo):
		return self.windows[str(windowNo)].getWidth()
	
	def stretchWindowRight(self,windowNo,dist):
		self.windows[str(windowNo)].stretchRight(dist)
		
	def stretchWindowLeft(self,windowNo,dist):
		self.windows[str(windowNo)].stretchLeft(dist)
		
	def stretchWindowUp(self,windowNo,dist):
		self.windows[str(windowNo)].stretchUp(dist)
		
	def stretchWindowDown(self,windowNo,dist):
		self.windows[str(windowNo)].stretchDown(dist)
		
	def setWindowName(self,windowNo,name):
		self.windows[str(windowNo)].setName(name)
		
	def getWindowName(self,windowNo):
		return self.windows[str(windowNo)].getName()
	
	def getWindowPos(self, windowNo):
		xloc = self.windows[str(windowNo)].getX()
		yloc = self.windows[str(windowNo)].getY()
		return (xloc,yloc)
	
	def findElement(self, elementNo):
		location = 0
		for key in self.windows:
			if(self.windows[key].containsEle(elementNo)==True):
				location = int(key)
		return location
	
	def newElement(self,element, windowNo):
		elementNo = 0
		with self.elements_lock:
			if (len(self.elements)==0):
				self.elements[str(1)] = element
				elementNo = 1
				self.lastele = 1
			else:
				self.lastele=self.lastele+1
				self.elements[str(self.lastele)] = element
				elementNo = self.lastele
		self.windows[str(windowNo)].addElement(elementNo)
		return elementNo
	
	def newCircle(self, owner, windowNo, x, y, radius, lineColor, fillColor):
		newCir = circle(owner, x, y, radius, lineColor, fillColor)
		elementNo = self.newElement(newCir, windowNo)
		return elementNo
	
	def newCircleWithID(self, owner, ID, windowNo, x, y, radius, lineColor, fillColor):
		elementNo = self.newCircle(owner, windowNo, x, y, radius, lineColor, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
		
	def setCirclePos(self, elementNo, xLoc, yLoc, window):
		self.elements[str(elementNo)].setCenter(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != window):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(window)].addElement(elementNo)
		
	def setCircleRad(self, elementNo, radius):
		self.elements[str(elementNo)].setRadius(radius)
		
	def getCircleRad(self, elementNo):
		rad = self.elements[str(elementNo)].getRadius()
		return rad
		
	def getCirclePos(self, elementNo):
		xloc = self.elements[str(elementNo)].getCenterX()
		yloc = self.elements[str(elementNo)].getCenterY()
		return (xloc,yloc)
	
	def getEleType(self, elementNo):
		return self.elements[str(elementNo)].checkType()
	
	def setCircleFill(self, elementNo, color):
		self.elements[str(elementNo)].setFillColor(color)
		
	def setCircleLine(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
		
	def getCircleFill(self, elementNo):
		return self.elements[str(elementNo)].getFillColor()
		
	def getCircleLine(self, elementNo):
		return self.elements[str(elementNo)].getLineColor()
	
	def newLine(self, owner, windowNo, x1, y1, x2, y2, color):
		newLine = line(owner, x1, y1, x2, y2, color)
		elementNo = self.newElement(newLine, windowNo)
		return elementNo
	
	def newLineWithID(self, owner, ID, windowNo, x1, y1, x2, y2, color):
		elementNo = self.newLine(owner, windowNo, x1, y1, x2, y2, color)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setLineStart(self,elementNo,x,y):
		self.elements[str(elementNo)].setStart(x,y)
		
	def setLineEnd(self,elementNo,x,y):
		self.elements[str(elementNo)].setEnd(x,y)
		
	def getLineStart(self,elementNo):
		xloc = self.elements[str(elementNo)].getStartX()
		yloc = self.elements[str(elementNo)].getStartY()
		return (xloc,yloc)
	
	def getLineEnd(self,elementNo):
		xloc = self.elements[str(elementNo)].getEndX()
		yloc = self.elements[str(elementNo)].getEndY()
		return (xloc,yloc)
	
	def setLineColor(self,elementNo,color):
		self.elements[str(elementNo)].setColor(color)
		
	def getLineColor(self,elementNo):
		return self.elements[str(elementNo)].getColor()
	
	def newLineStrip(self, owner, windowNo, x, y, color):
		newLineStrip = lineStrip(owner, x, y, color)
		elementNo = self.newElement(newLineStrip, windowNo)
		return elementNo
	
	def newLineStripWithID(self, owner, ID, windowNo, x, y, color):
		elementNo = self.newLineStrip(owner, windowNo, x, y, color)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def addLineStripPoint(self, elementNo, x, y):
		self.elements[str(elementNo)].addPoint(x,y)
		
	def addLineStripPointAt(self, elementNo, x, y, index):
		self.elements[str(elementNo)].addPointAt(x,y,index)
		
	def getLineStripPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def moveLineStripPoint(self, elementNo, pointNo, x, y):
		self.elements[str(elementNo)].setPoint(pointNo, x, y)
		
	def getLineStripColor(self, elementNo):
		color = self.elements[str(elementNo)].getColor()
		return color
	
	def setLineStripColor(self, elementNo, color):
		self.elements[str(elementNo)].setColor(color)
		
	def getLineStripPointsCount(self, elementNo):
		return self.elements[str(elementNo)].getNumPoints()
	
	def newPolygon(self, owner, windowNo, x, y, lineColor, fillColor):
		newPoly = polygon(owner, x, y, lineColor, fillColor)
		elementNo = self.newElement(newPoly, windowNo)
		return elementNo
	
	def newPolygonWithID(self, owner, ID, windowNo, x, y, lineColor, fillColor):
		elementNo = self.newPolygon(owner, windowNo, x, y, lineColor, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def addPolygonPoint(self, elementNo, x, y):
		self.elements[str(elementNo)].addPoint(x,y)
		
	def getPolygonPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def movePolygonPoint(self, elementNo, pointNo, x, y):
		self.elements[str(elementNo)].setPoint(pointNo, x, y)
		
	def getPolygonFillColor(self, elementNo):
		color = self.elements[str(elementNo)].getFillColor()
		return color
	
	def setPolygonFillColor(self, elementNo, color):
		self.elements[str(elementNo)].setFillColor(color)
		
	def getPolygonLineColor(self, elementNo):
		color = self.elements[str(elementNo)].getLineColor()
		return color
	
	def setPolygonLineColor(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
		
	def getPolygonPointsCount(self, elementNo):
		return self.elements[str(elementNo)].getNumPoints()
	
	def newRectangle(self, owner, windowNo, x, y, width, height, lineColor, fillColor):
		newRect = rectangle(owner, x, y, width, height, lineColor, fillColor)
		elementNo = self.newElement(newRect, windowNo)
		return elementNo
	
	def newRectangleWithID(self, owner, ID, windowNo, x, y, width, height, lineColor, fillColor):
		elementNo = self.newRectangle(owner, windowNo, x, y, width, height, lineColor, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setRectangleTopLeft(self, elementNo, x, y):
		self.elements[str(elementNo)].setTopLeft(x,y)
		
	def getRectangleTopLeft(self, elementNo):
		xloc = self.elements[str(elementNo)].getTopLeftX()
		yloc = self.elements[str(elementNo)].getTopLeftY()
		return (xloc,yloc)
	
	def getRectangleTopRight(self, elementNo):
		xloc = self.elements[str(elementNo)].getTopRightX()
		yloc = self.elements[str(elementNo)].getTopRightY()
		return (xloc,yloc)
	
	def getRectangleBottomRight(self, elementNo):
		xloc = self.elements[str(elementNo)].getBottomRightX()
		yloc = self.elements[str(elementNo)].getBottomRightY()
		return (xloc,yloc)

	def getRectangleBottomLeft(self, elementNo):
		xloc = self.elements[str(elementNo)].getBottomLeftX()
		yloc = self.elements[str(elementNo)].getBottomLeftY()
		return (xloc,yloc)
	
	def setRectangleWidth(self, elementNo, width):
		self.elements[str(elementNo)].setWidth(width)
		
	def getRectangleWidth(self, elementNo):
		return int(self.elements[str(elementNo)].getWidth())
		
	def setRectangleHeight(self, elementNo, height):
		self.elements[str(elementNo)].setHeight(height)
		
	def getRectangleHeight(self, elementNo):
		return int(self.elements[str(elementNo)].getHeight())
		
	def getRectangleFillColor(self, elementNo):
		color = self.elements[str(elementNo)].getFillColor()
		return color
	
	def setRectangleFillColor(self, elementNo, color):
		self.elements[str(elementNo)].setFillColor(color)
		
	def getRectangleLineColor(self, elementNo):
		color = self.elements[str(elementNo)].getLineColor()
		return color
	
	def setRectangleLineColor(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
	
	def newText(self, owner, windowNo, text, x, y, pt, font, color):
		newText = textBox(owner, text, x, y, pt, font, color)
		elementNo = self.newElement(newText, windowNo)
		return elementNo
	
	def newTextWithID(self, owner, ID, windowNo, text, x, y, pt, font, color):
		elementNo = self.newText(owner, windowNo, text, x, y, pt, font, color)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setText(self, elementNo, text):
		self.elements[str(elementNo)].setText(text)
		
	def getText(self, elementNo):
		return self.elements[str(elementNo)].getText()
	
	def setTextPos(self, elementNo, xLoc, yLoc, window):
		self.elements[str(elementNo)].setLocation(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != window):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(window)].addElement(elementNo)
			
	def getTextPos(self, elementNo):
		xloc = self.elements[str(elementNo)].getLocationX()
		yloc = self.elements[str(elementNo)].getLocationY()
		return (xloc,yloc)
	
	def setPtSize(self, elementNo, ptSize):
		self.elements[str(elementNo)].setPt(ptSize)
		
	def getPtSize(self, elementNo):
		return self.elements[str(elementNo)].getPt()
	
	def getFont(self, elementNo):
		return self.elements[str(elementNo)].getFont()
	
	def setFont(self,elementNo,font):
		self.elements[str(elementNo)].setFont(font)
		
	def setTextColor(self,elementNo,color):
		self.elements[str(elementNo)].setColor(color)
		
	def getTextColor(self,elementNo):
		return self.elements[str(elementNo)].getColor()
	
	def showElement(self,elementNo):
		self.elements[str(elementNo)].show()
		
	def hideElement(self,elementNo):
		self.elements[str(elementNo)].hide()
		
	def checkElementVisibility(self,elementNo):
		return self.elements[str(elementNo)].isVisible()
	
	def getElementID(self, elementNo):
		return self.elements[str(elementNo)].getID()
	
	def setElementID(self, elementNo, ID):
		self.elements[str(elementNo)].setID(ID)
		
	def getElementOwner(self, elementNo):
		return self.elements[str(elementNo)].getOwner()
	
	def getCursors(self,surfaceNo):
		return self.surfaces[str(surfaceNo)].getCursors()
	
	def getWindows(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getWindows()
	
	def getElements(self, windowNo):
		return self.windows[str(windowNo)].getElements()
	
	def getClickedElements(self, surfaceNo, x, y):
		windows = self.getWindows(surfaceNo)
		hits = []
		for windowNo in windows:
			elements = self.getElements(windowNo)
			for elementNo in elements:
				if(self.getEleType(elementNo) == "circle"):
					pos = self.getCirclePos(elementNo)
					rad = float(self.getCircleRad(elementNo))
					dist = None
					if(x!=pos[0] and y!=pos[1]):
						dist=sqrt(pow(abs(float(pos[0])-float(x)),2)+pow(abs(float(pos[1])-float(y)),2))
					elif(x==pos[0]):
						dist=abs(float(pos[1])-float(y))
					elif(y==pos[1]):
						dist=abs(float(pos[0])-float(x))
					if(dist<=rad):
						hits.append(elementNo)
		return hits
	
	#Based on code from https://developer.coronalabs.com/code/checking-if-point-inside-rotated-rectangle
	def isPointInsideRectangle(self, rectRot, rectTlX, rectTlY, rectHeight, rectWidth, x, y):
		c = cos(-rectRot*pi/180)
		s = sin(-rectRot*pi/180)
		
		#Unrotate point according to rectangle rotation
		rotX = rectTlX + c * (x - rectTlX) - s * (y - rectTlY)
		rotY = rectTlY + s * (x - rectTlX) + c * (y - rectTlY)
		
		#Calculate bounds of unrotated rectangle
		leftX = rectTlX
		rightX = rectTlX + rectWidth
		topY = rectTlY
		bottomY = rectTlY + rectHeight
		return leftX <= rotX and rotX <= rightX and topY <= rotY and rotY<= bottomY