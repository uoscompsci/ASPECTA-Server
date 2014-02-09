from GUIElements import *

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur', 'lastsur']
	
	def __init__(self):
		self.lastcur = 0
		self.lastsur = 0
		self.surfaces_lock = False
		self.displays_lock = False
		self.cursors_lock = False
		self.cursors = {}
		self.surfaces = {}
		
	def newSurface(self):
		newSur = surface()
		added = False
		surfaceNo = 0
		while(added == False):
			if(self.surfaces_lock==False):
				self.surfaces_lock = True
				if (len(self.surfaces)==0):
					self.surfaces["1"] = newSur
					print(self.surfaces)
					print(len(self.surfaces))
					surfaceNo = 1
					self.lastsur = 1
				else:
					self.lastsur=self.lastsur+1
					self.surfaces[str(self.lastsur)] = newSur
					print(self.surfaces)
					print(len(self.surfaces))
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
				print (self.cursors)
				if (len(self.cursors)==0):
					self.cursors[str(1)] = newCur
					cursorNo = 1
					self.lastcur = 1
					print(self.cursors)
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
			if(self.surfaces[key].containsCur(cursorNo)==True): #TODO still need to implement
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