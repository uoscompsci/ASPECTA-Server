from GUIElements import *

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur']
	
	def __init__(self):
		self.lastcur = 0
		self.surfaces_lock = False
		self.displays_lock = False
		self.cursors_lock = False

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
					self.lastcur++
					self.cursors[str(self.lastcur)] = newCur
					cursorNo = self.lastcur		
				self.cursors_lock = False
				added = true
		self.surfaces[surface].addCursor(cursorNo) #TODO still need to implement
		return cursorNo
	
	def moveCursor(self, cursorNo, xDist, yDist):
		self.cursors[str(cursorNo)].move(xDist,yDist)
		
	def findCursor(self, cursorNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsCur(cusorNo)==True): #TODO still need to implement
				location = int(key)
		return location
		
	def setCursorPos(self, cursorNo, xLoc, yLoc, surface):
		self.cursors[str(cursorNo)].setLoc(xLoc,yLoc)
		origSur = self.findCursor(cursorNo)
		if(origSur != surface):
			surfaces[str(origSur)].removeCursor(cursorNo) #TODO still need to implement
			surfaces[str(surface)].addCursor(cursorNo)
			
	def removeCursor(self,cursorNo):
		location = 0
		surNo = self.findCursor(cursorNo)
		self.surfaces[str(surNo)].removeCursor(cursorNo)
		self.cursors.pop(str(cursorNo),None)