from GUIElements import *

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur', 'lastsur', 'lastwin', 'lastele' 'windows', 'windows_lock', 'elements', 'elements_lock']
	
	def __init__(self):
		self.lastcur = 0
		self.lastsur = 0
		self.lastwin = 0
		self.lastele = 0
		self.surfaces_lock = False
		self.displays_lock = False
		self.cursors_lock = False
		self.windows_lock = False
		self.elements_lock = False
		self.cursors = {}
		self.surfaces = {}
		self.windows = {}
		self.elements = {}
		
	def newSurface(self):
		newSur = surface()
		added = False
		surfaceNo = 0
		while(added == False):
			if(self.surfaces_lock==False):
				self.surfaces_lock = True
				if (len(self.surfaces)==0):
					self.surfaces["1"] = newSur
					surfaceNo = 1
					self.lastsur = 1
				else:
					self.lastsur=self.lastsur+1
					self.surfaces[str(self.lastsur)] = newSur
					surfaceNo = self.lastsur		
				self.surfaces_lock = False
				added = True
		return surfaceNo

	def newCursor(self, surface, x, y):
		newCur = cursor(x,y)
		added = False
		cursorNo = 0
		while(added == False):
			if(self.cursors_lock==False):
				self.cursors_lock = True
				if (len(self.cursors)==0):
					self.cursors[str(1)] = newCur
					cursorNo = 1
					self.lastcur = 1
				else:
					self.lastcur=self.lastcur+1
					self.cursors[str(self.lastcur)] = newCur
					cursorNo = self.lastcur		
				self.cursors_lock = False
				added = True
		self.surfaces[str(surface)].addCursor(cursorNo)
		return cursorNo
		
	def findCursor(self, cursorNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsCur(cursorNo)==True):
				location = int(key)
		return location
	
	def moveCursor(self, cursorNo, xDist, yDist):
		self.cursors[str(cursorNo)].move(xDist,yDist) #TODO Handle when moves to different screen
		
	def setCursorPos(self, cursorNo, xLoc, yLoc, surface):
		self.cursors[str(cursorNo)].setLoc(xLoc,yLoc)
		origSur = self.findCursor(cursorNo)
		if(origSur != surface):
			self.surfaces[str(origSur)].removeCursor(cursorNo)
			self.surfaces[str(surface)].addCursor(cursorNo)
			
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
	
	def newWindow(self, surface, x, y, xWid, yWid, name):
		newWin = window(x,y,xWid,yWid,name)
		added = False
		windowNo = 0
		while(added == False):
			if(self.windows_lock==False):
				self.windows_lock = True
				if (len(self.windows)==0):
					self.windows[str(1)] = newWin
					windowNo = 1
					self.lastwin = 1
				else:
					self.lastwin=self.lastwin+1
					self.windows[str(self.lastwin)] = newWin
					windowNo = self.lastwin		
				self.windows_lock = False
				added = True
		self.surfaces[str(surface)].addWindow(windowNo)
		return windowNo
	
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
	
	def newCircle(self, windowNo, x, y, radius, lineColor, fillColor):
		newCir = circle(x, y, radius, lineColor, fillColor)
		added = False
		elementNo = 0
		while(added == False):
			if(self.elements_lock==False):
				self.elements_lock = True
				if (len(self.elements)==0):
					self.elements[str(1)] = newCir
					elementNo = 1
					self.lastele = 1
				else:
					self.lastele=self.lastele+1
					self.elements[str(self.lastele)] = newCir
					elementNo = self.lastele		
				self.elements_lock = False
				added = True
		self.windows[str(windowNo)].addElement(elementNo)
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