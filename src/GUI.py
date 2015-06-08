from GUIElements import *
import threading
from math import *
import time

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur', 'lastsur', 'lastwin', 'lastele' 'windows', 'windows_lock', 'elements', 'elements_lock', 'setup_surface_visible']
	
	correctDirect = {'right' : {0 : 'right', 1 : 'bottom', 2 : 'left', 3 : "top"},
				'bottom' : {0 : 'bottom', 1 : 'left', 2 : 'top', 3 : "right"},
				'left' : {0 : 'left', 1 : 'top', 2 : 'right', 3 : "bottom"},
				'top' : {0 : 'top', 1 : 'right', 2 : 'bottom', 3 : "left"}
				}
	
	def __init__(self, width, height):
		parser = SafeConfigParser()
		parser.read("config.ini")
		self.winWidth = parser.getint('surfaces', 'windowWidth')
		self.winHeight = parser.getint('surfaces', 'windowHeight')
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
		self.connections = []
		self.surfaces["0"] = surface("server", "server", "0", "setup")
		self.setSurfacePixelWidth(0, width)
		self.setSurfacePixelHeight(0, height)
		self.setup_surface_visible = False
		
	def winWidPropToPix(self, win, prop):
		width = self.getWindowWidth(win)
		return float(prop)*width
		
	def winHeiPropToPix(self, win, prop):
		height = self.getWindowHeight(win)
		return float(prop)*height
		
	def surfWidPropToPix(self, surf, prop):
		width = self.getSurfacePixelWidth(surf)
		return float(prop)*width
		
	def surfHeiPropToPix(self, surf, prop):
		height = self.getSurfacePixelHeight(surf)
		return float(prop)*height
		
	def surfWidMetToPix(self, surf, met):
		width = self.getSurfacePixelWidth(surf)
		realWidth = self.getSurfaceRealWidth(surf)
		return float(width)/float(realWidth)*met
		
	def surfHeiMetToPix(self, surf, met):
		height = self.getSurfacePixelHeight(surf)
		realHeight = self.getSurfaceRealHeight(surf)
		return float(height)/float(realHeight)*met
		
	def hideSetupSurface(self):
		self.setup_surface_visible = False
		
	def showSetupSurface(self):
		self.setup_surface_visible = True
		
	def getSetupSurfaceVisibilty(self):
		return self.setup_surface_visible
		
	def newSurface(self, owner, app, appno):
		newSur = surface(owner, app, appno, "standard")
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
	
	def newSurfaceWithID(self, owner, app, appno, ID):
		surfaceNo = self.newSurface(owner, app, appno, "standard")
		self.surfaces[set(surfaceNo)].setID(ID)
		return surfaceNo
	
	def setSurfacePoints(self, surfaceNo, topPoints, bottomPoints, leftPoints, rightPoints):
		self.surfaces[str(surfaceNo)].setPoints(topPoints, bottomPoints, leftPoints, rightPoints)
	
	def subscribeToSurface(self, app, surfaceNo):
		self.surfaces[str(surfaceNo)].subscribe(app)
	
	def getSurfaceID(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getID()
	
	def setSurfaceID(self, surfaceNo, ID):
		self.surfaces[str(surfaceNo)].setID(ID)
		
	def getSurfaceOwner(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getOwner()
	
	def getSurfaceAppDetails(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getAppDetails()
	
	
	def getSurfaces(self):
		found = []
		for x in range(1,len(self.surfaces)):
			found.append(x)
		return found
	
	def getDefinedSurfaces(self):
		found = []
		for x in range(1,len(self.surfaces)):
			if(self.surfaces[str(x)].isDefined()==True):
				found.append(x)
		return found
	
	def setSurfaceType(self, surfaceNo, type):
		self.surfaces[str(surfaceNo)].setType(type)
		
	def getSurfaceType(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getType()
	
	def getSurfacePixelWidth(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getPixelWidth()
		
	def getSurfacePixelHeight(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getPixelHeight()
		
	def setSurfacePixelWidth(self, surfaceNo, width):
		self.surfaces[str(surfaceNo)].setPixelWidth(width)
		
	def setSurfacePixelHeight(self, surfaceNo, height):
		self.surfaces[str(surfaceNo)].setPixelHeight(height)
		
	def getSurfaceRealWidth(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getRealWidth()
		
	def getSurfaceRealHeight(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getRealHeight()
		
	def setSurfaceRealWidth(self, surfaceNo, width):
		self.surfaces[str(surfaceNo)].setRealWidth(width)
		
	def setSurfaceRealHeight(self, surfaceNo, height):
		self.surfaces[str(surfaceNo)].setRealHeight(height)
		
	def clearSurface(self, surfaceNo):
		windows = self.getWindows(surfaceNo)
		cursors = self.getCursors(surfaceNo)
		for x in range(0,len(windows)):
			elements = self.getElements(windows[x])
			for y in range(0,len(elements)):
				self.removeElement(elements[y], windows[x])
		for x in range(0,len(cursors)):
			self.removeCursor(cursors[x])
		windowRemovalThread = threading.Thread(target=self.delayedWindowRemoval, args=[windows]) #Creates the display thread
		windowRemovalThread.start()
		
	def delayedWindowRemoval(self,windows):
		time.sleep(3)
		for x in range(0,len(windows)):
			self.removeWindow(windows[x])
	
	def saveDefinedSurfaces(self, filename):
		file = open("layouts/" + filename + ".lyt", 'w')
		defSurfaces = self.getDefinedSurfaces()
		for z in range(0, len(defSurfaces)):
			top = self.surfaces[str(defSurfaces[z])].getTopPoints()
			bottom = self.surfaces[str(defSurfaces[z])].getBottomPoints()
			left = self.surfaces[str(defSurfaces[z])].getLeftPoints()
			right = self.surfaces[str(defSurfaces[z])].getRightPoints()
			owner = self.getSurfaceOwner(defSurfaces[z])
			app = self.getSurfaceAppDetails(defSurfaces[z])
			type = self.getSurfaceType(defSurfaces[z])
			pixwid = self.getSurfacePixelWidth(defSurfaces[z])
			pixhei = self.getSurfacePixelHeight(defSurfaces[z])
			realwid = self.getSurfaceRealWidth(defSurfaces[z])
			realhei = self.getSurfaceRealHeight(defSurfaces[z])
			file.write(str(defSurfaces[z]) + ";" + type + "\n")
			file.write(owner + ";" + app[0] + ";" + str(app[1]) + "\n")
			file.write(str(pixwid) + ";" + str(pixhei) + "\n")
			file.write(str(realwid) + ";" + str(realhei) + "\n")
			rot = self.getSurfaceRotation(defSurfaces[z])
			mir = self.getSurfaceMirrored(defSurfaces[z])
			file.write(str(rot) + ";" + str(mir) + "\n")
			file.write(top + "\n")
			file.write(bottom + "\n")
			file.write(left + "\n")
			file.write(right + "\n")
		file.write("#\n")
		for z in range(0, len(self.connections)):
			surf1 = self.connections[z].getSurface1()
			surf2 = self.connections[z].getSurface2()
			file.write(str(surf1[0]) + ":" + surf1[1] + ";" + str(surf2[0]) + ":" + surf2[1] + "\n")
		file.close()
		
	def loadDefinedSurfaces(self, filename):
		file = open("layouts/" + filename + ".lyt", 'r')
		check = file.readline().strip()
		check = check.split(";")
		layouts = []
		connections = []
		realSizes = ""
		if(len(self.surfaces)<2):
			self.newSurface("loaded", "loaded", 0)
			self.newSurface("loaded", "loaded", 0)
			self.newSurface("loaded", "loaded", 0)
			self.newSurface("loaded", "loaded", 0)
		while(check[0]!="#" and check[0]!=""):
			params = file.readline().strip()
			params = params.split(";")
			pixdim = file.readline().strip()
			pixdim = pixdim.split(";")
			realdim = file.readline().strip()
			realdim = realdim.split(";")
			rotmir = file.readline().strip()
			rotmir = rotmir.split(";")
			if(int(rotmir[0])==0):
				self.rotateSurfaceTo0(int(check[0]))
			elif(int(rotmir[0])==1):
				self.rotateSurfaceTo90(int(check[0]))
			elif(int(rotmir[0])==2):
				self.rotateSurfaceTo180(int(check[0]))
			elif(int(rotmir[0])==3):
				self.rotateSurfaceTo270(int(check[0]))
			if(rotmir[1]=="True"):
				if(self.getSurfaceMirrored(int(check[0]))==False):
					self.mirrorSurface(int(check[0]))
			elif(rotmir[1]=="False"):
				if(self.getSurfaceMirrored(int(check[0]))==True):
					self.mirrorSurface(int(check[0]))
				
			self.setSurfacePixelWidth(int(check[0]), int(pixdim[0]))
			self.setSurfacePixelHeight(int(check[0]), int(pixdim[1]))
			
			self.setSurfaceRealWidth(int(check[0]), int(realdim[0]))
			self.setSurfaceRealHeight(int(check[0]), int(realdim[1]))
			
			if(len(realSizes)!=0):
				realSizes += ";"
			realSizes += str(realdim[0]) + ":" + str(realdim[1])				
			
			top = file.readline().strip()
			bottom = file.readline().strip()
			left = file.readline().strip()
			right = file.readline().strip()
			self.setSurfaceType(int(check[0]), check[1])
			self.setSurfacePoints(int(check[0]), top, bottom, left, right)
			layouts.append(top + "&" + bottom + "&" + left + "&" + right)
			check = file.readline().strip()
			check = check.split(";")
		connection = file.readline().strip()
		while(connection!=""):
			connections.append(connection)
			connection = connection.split(";")
			side1 = connection[0].split(":")
			side2 = connection[1].split(":")
			self.connectSurfaces(side1[0], side1[1], side2[0], side2[1])
			connection = file.readline().strip()
		count = 0
		for x in self.surfaces:
			if self.surfaces[x].isDefined()==True:
				count += 1
		layoutstring = ""
		if(len(layouts)>0):
			layoutstring = layouts[0]
		for x in range(1,len(layouts)):
			layoutstring += "%" + layouts[x]
		connectstring = ""
		if(len(connections)>0):
			connectstring = connections[0]
		for x in range(1,len(connections)):
			connectstring += "%" + connections[x]
		return (count, layoutstring, connectstring, realSizes)
		
	def getSurfacesByID(self, ID):
		found = []
		for x in range(0,len(self.surfaces)):
			if(self.surfaces[str(x)].getID()==ID):
				found.append(x)
		return found
	
	def getSurfacesByOwner(self, owner):
		found = []
		for x in range(0,len(self.surfaces)):
			if(self.surfaces[str(x)].getOwner()==owner):
				found.append(x)
		return found
	
	def getSurfacesByAppName(self, app):
		found = []
		for x in range(0,len(self.surfaces)):
			if(self.surfaces[str(x)].getAppDetails()[0]==app):
				found.append(x)
		return found
	
	def getSurfacesByAppDetails(self, app, appno):
		found = []
		for x in range(0,len(self.surfaces)):
			details = self.surfaces[str(x)].getAppDetails()
			if(details[0]==app and details[1]==appno):
				found.append(x)
		return found
	
	def becomeSurfaceAdmin(self, surfaceNo, app, appno):
		return self.surfaces[str(surfaceNo)].becomeAdmin(app, appno)
		
	def stopBeingSurfaceAdmin(self, surfaceNo, app, appno):
		return self.surfaces[str(surfaceNo)].stopBeingAdmin(app, appno)
	
	def isSurfaceDefined(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].isDefined()
	
	def getSurfacePoints(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getPoints()
	
	def getSurfaceRotation(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getRotation()
		
	def getSurfaceMirrored(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getMirrored()
	
	def rotateSurfaceTo0(self, surfaceNo):
		self.surfaces[str(surfaceNo)].rotateTo0()
		
	def rotateSurfaceTo90(self, surfaceNo):
		self.surfaces[str(surfaceNo)].rotateTo90()
		
	def rotateSurfaceTo180(self, surfaceNo):
		self.surfaces[str(surfaceNo)].rotateTo180()
		
	def rotateSurfaceTo270(self, surfaceNo):
		self.surfaces[str(surfaceNo)].rotateTo270()
		
	def mirrorSurface(self, surfaceNo):
		self.surfaces[str(surfaceNo)].mirror()
		
	def connectSurfaces(self, surfaceNo1, side1, surfaceNo2, side2):
		newConnection = surfaceConnection(surfaceNo1, side1, surfaceNo2, side2)
		self.connections.append(newConnection)
		
	def disconnectSurfaces(self, surfaceNo1, side1, surfaceNo2, side2):
		notDisconnected = True
		for x in range(0,len(self.connections)):
			if(notDisconnected):
				sur1 = self.connections[x].getSurface1()
				if(sur1[0]==surfaceNo1 and sur1[1]==side1):
					sur2 = self.connections[x].getSurface2()
					if(sur2[0]==surfaceNo2 and sur2[1]==side2):
						notDisconnected = False
						self.connections.pop(x)
				elif(sur1[0]==surfaceNo2 and sur1[1]==side2):
					sur2 = self.connections[x].getSurface2()
					if(sur2[0]==surfaceNo1 and sur2[1]==side1):
						notDisconnected = False
						self.connections.pop(x)
	
	def checkSurfaceRenderUpdate(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].checkRenderUpdate()
	
	def undefineSurface(self, surfaceNo):
		self.surfaces[str(surfaceNo)].undefine()
	
	def newCursor(self, surface, x, y, coorSys):
		if(coorSys=="prop"):
			x = self.surfWidPropToPix(surface, x)
			y = self.surfHeiPropToPix(surface, y)
		elif(coorSys=="real"):
			x = self.surfWidMetToPix(surface, x)
			y = self.surfHeiMetToPix(surface, y)
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
	
	def newCursorWithID(self, ID, surface, x, y, coorSys):
		cursorNo = self.newCursor(surface, x, y, coorSys)
		self.cursors[set(cursorNo)].setID(ID)
		return cursorNo
		
	def findCursor(self, cursorNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsCur(cursorNo)==True):
				location = int(key)
		return location
	
	def moveCursor(self, cursorNo, xDist, yDist):
		xDist = float(xDist)
		yDist = float(yDist)
		loc = self.getCursorPos(cursorNo)
		finalLoc=[0,0]
		tempLoc = self.cursors[str(cursorNo)].testMove(xDist,yDist)
		testLoc=[tempLoc[0],tempLoc[1]]
		switchSurface=False
		surface=0
		if(self.findCursor(cursorNo)==0):
			if(testLoc[0] > self.winWidth):
				finalLoc[0] = self.winWidth
			elif(testLoc[0] < 0):
				finalLoc[0] = 0
			else:
				finalLoc[0] = testLoc[0]
			if(testLoc[1] > self.winHeight):
				finalLoc[1] = self.winHeight
			elif(testLoc[1] < 0):
				finalLoc[1] = 0
			else:
				finalLoc[1] = testLoc[1]
		else:
			if(testLoc[0] > self.getSurfacePixelWidth(self.findCursor(cursorNo))):
				conn = self.testForConnection(self.findCursor(cursorNo)-1,self.correctDirect["right"][self.getSurfaceRotation(self.findCursor(cursorNo))])
				if(conn[1]=="None"):
					finalLoc[0] = self.getSurfacePixelWidth(self.findCursor(cursorNo))
				else:
					switchSurface=True
					surface=int(conn[0])+1
					finalLoc[0] = testLoc[0]-self.getSurfacePixelWidth(self.findCursor(cursorNo))
			elif(testLoc[0] < 0):
				conn = self.testForConnection(self.findCursor(cursorNo)-1,self.correctDirect["left"][self.getSurfaceRotation(self.findCursor(cursorNo))])
				if(conn[1]=="None"):
					finalLoc[0] = 0
				else:
					switchSurface=True
					surface=int(conn[0])+1
					finalLoc[0] = self.getSurfacePixelWidth(self.findCursor(cursorNo))+testLoc[0]
			else:
				finalLoc[0] = testLoc[0]
			if(testLoc[1] > self.getSurfacePixelHeight(self.findCursor(cursorNo))):
				conn = self.testForConnection(self.findCursor(cursorNo)-1,self.correctDirect["top"][self.getSurfaceRotation(self.findCursor(cursorNo))])
				if(conn[1]=="None"):
					finalLoc[1] = self.getSurfacePixelHeight(self.findCursor(cursorNo))
				else:
					switchSurface=True
					surface=int(conn[0])+1
					finalLoc[1] = testLoc[1]-self.getSurfacePixelHeight(self.findCursor(cursorNo))
			elif(testLoc[1] < 0):
				conn = self.testForConnection(self.findCursor(cursorNo)-1,self.correctDirect["bottom"][self.getSurfaceRotation(self.findCursor(cursorNo))])
				if(conn[1]=="None"):
					finalLoc[1] = 0
				else:
					switchSurface=True
					surface=int(conn[0])+1
					finalLoc[1] = self.getSurfacePixelHeight(self.findCursor(cursorNo))+testLoc[1]
			else:
				finalLoc[1] = testLoc[1]
		if(switchSurface):
			self.setCursorPos(cursorNo, finalLoc[0], finalLoc[1], surface)
		else:
			self.setCursorPos(cursorNo, finalLoc[0], finalLoc[1], self.findCursor(cursorNo))
		
	def testForConnection(self, surfaceNo, side):
		found=False
		surfaceNo = str(surfaceNo)
		result=()
		for x in range(0,len(self.connections)):
			if(found==False):
				sur1 = self.connections[x].getSurface1()
				sur2 = self.connections[x].getSurface2()
				if(sur1[0]==surfaceNo and sur1[1]==side):
					result=(sur2[0],sur2[1])
					found=True
				elif(sur2[0]==surfaceNo and sur2[1]==side):
					result=(sur1[0],sur1[1])
					found=True
		if found:
			return result
		else:
			return (0,"None")
		
	def getCursorPos(self, cursorNo):
		return self.cursors[str(cursorNo)].getLoc()
	
	def getCursorMode(self, cursorNo):
		return self.cursors[str(cursorNo)].getMode()
	
	def setCursorWallMode(self, cursorNo):
		self.cursors[str(cursorNo)].setWallMode()
	
	def setCursorBlockMode(self, cursorNo):
		self.cursors[str(cursorNo)].setBlockMode()
	
	def setCursorScreenMode(self, cursorNo):
		self.cursors[str(cursorNo)].setScreenMode()
	
	def setCursorDefaultMode(self, cursorNo):
		self.cursors[str(cursorNo)].setDefaultMode()
		
	def testMoveCursor(self, cursorNo, xDist, yDist):
		return self.cursors[str(cursorNo)].testMove(xDist,yDist) #TODO Handle when moves to different screen
		
	def rotateCursorClockwise(self,cursorNo,degrees):
		self.cursors[str(cursorNo)].rotateClockwise(degrees)
		
	def rotateCursorAnticlockwise(self,cursorNo,degrees):
		self.cursors[str(cursorNo)].rotateAnticlockwise(degrees)
		
	def getCursorRotation(self,cursorNo):
		return self.cursors[str(cursorNo)].getRotation()
	
	def hideCursor(self, cursorNo):
		self.cursors[str(cursorNo)].hide()
		
	def showCursor(self, cursorNo):
		self.cursors[str(cursorNo)].show()
		
	def isCursorVisible(self, cursorNo):
		return self.cursors[str(cursorNo)].isVisible()
		
	def setCursorPos(self, cursorNo, xLoc, yLoc, surface):
		cursorNo = int(cursorNo)
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
	
	def getCursorPos(self, cursorNo):
		xloc = self.cursors[str(cursorNo)].getX()
		yloc = self.cursors[str(cursorNo)].getY()
		return (xloc,yloc)
	
	def newWindow(self, owner, app, appno, surface, x, y, xWid, yWid, coorSys, name):
		if(coorSys=="prop"):
			x = self.surfWidPropToPix(surface, x)
			y = self.surfHeiPropToPix(surface, y)
			xWid = self.surfWidPropToPix(surface, xWid)
			yWid = self.surfHeiPropToPix(surface, yWid)
		elif(coorSys=="real"):
			x = self.surfWidMetToPix(surface, x)
			y = self.surfHeiMetToPix(surface, y)
			xWid = self.surfWidMetToPix(surface, xWid)
			yWid = self.surfHeiMetToPix(surface, yWid)
		newWin = window(owner,app,appno,x,y,xWid,yWid,name)
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
	
	def newWindowWithID(self, owner, app, appno, ID, surface, x, y, xWid, yWid, coorSys, name):
		windowNo = self.newWindow(owner, app, appno, surface, x, y, xWid, yWid, coorSys, name)
		self.windows[set(windowNo)].setID(ID)
		return windowNo
	
	def subscribeToWindow(self, app, windowNo):
		self.windows[str(windowNo)].subscribe(app)
	
	def getWindowID(self, windowNo):
		return self.windows[str(windowNo)].getID()
	
	def setWindowID(self, windowNo, ID):
		self.windows[str(windowNo)].setID(ID)
		
	def getWindowOwner(self, windowNo):
		return self.windows[str(windowNo)].getOwner()
	
	def getWindowAppDetails(self, windowNo):
		return self.windows[str(windowNo)].getAppDetails()
	
	def getWindowsByID(self, ID):
		found = []
		for x in range(0,len(self.windows)):
			if(self.windows[str(x)].getID()==ID):
				found.append(x)
		return found
	
	def getWindowsByOwner(self, owner):
		found = []
		for x in range(0,len(self.windows)):
			if(self.windows[str(x)].getOwner()==owner):
				found.append(x)
		return found
	
	def getWindowsByAppName(self, app):
		found = []
		for x in range(0,len(self.windows)):
			if(self.windows[str(x)].getAppDetails()[0]==app):
				found.append(x)
		return found
	
	def getWindowsByAppDetails(self, app, appno):
		found = []
		for x in range(0,len(self.windows)):
			details = self.windows[str(x)].getAppDetails()
			if(details[0]==app and details[1]==appno):
				found.append(x)
		return found
	
	def findWindow(self, windowNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsWin(windowNo)==True):
				location = int(key)
		return location
	
	def moveWindow(self, windowNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidPropToPix(surfaceNo, xDist)
			yDist = self.surfHeiPropToPix(surfaceNo, yDist)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		self.windows[str(windowNo)].drag(xDist,yDist) #TODO Handle when moves to different screen
		
	def setWindowPos(self, windowNo, xLoc, yLoc, coorSys, surface):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			xLoc = self.surfWidPropToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiPropToPix(surfaceNo, yLoc)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.windows[str(windowNo)].setLoc(xLoc,yLoc)
		origSur = self.findWindow(windowNo)
		if(origSur != surface):
			self.surfaces[str(origSur)].removeWindow(windowNo)
			self.surfaces[str(surface)].addWindow(windowNo)
			
	def removeWindow(self,windowNo):
		surNo = self.findWindow(windowNo)
		self.surfaces[str(surNo)].removeWindow(windowNo)
		self.windows.pop(str(windowNo),None)

	def setWindowHeight(self,windowNo,height,coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			height = self.surfHeiPropToPix(surfaceNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			height = self.surfHeiMetToPix(surfaceNo, height)
		self.windows[str(windowNo)].setHeight(height)
		
	def setWindowWidth(self,windowNo,width,coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			width = self.surfWidPropToPix(surfaceNo, width)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.windows[str(windowNo)].setWidth(width)
		
	def getWindowHeight(self,windowNo):
		return self.windows[str(windowNo)].getHeight()
	
	def getWindowWidth(self,windowNo):
		return self.windows[str(windowNo)].getWidth()
	
	def stretchWindowRight(self,windowNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfWidPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfWidMetToPix(surfaceNo, dist)
		self.windows[str(windowNo)].stretchRight(dist)
		
	def stretchWindowLeft(self,windowNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfWidPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfWidMetToPix(surfaceNo, dist)
		self.windows[str(windowNo)].stretchLeft(dist)
		
	def stretchWindowUp(self,windowNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfHeiPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfHeiMetToPix(surfaceNo, dist)
		self.windows[str(windowNo)].stretchUp(dist)
		
	def stretchWindowDown(self,windowNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfHeiPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			dist = self.surfHeiMetToPix(surfaceNo, dist)
		self.windows[str(windowNo)].stretchDown(dist)
		
	def setWindowName(self,windowNo,name):
		self.windows[str(windowNo)].setName(name)
		
	def getWindowName(self,windowNo):
		return self.windows[str(windowNo)].getName()
	
	def getWindowPos(self, windowNo):
		xloc = self.windows[str(windowNo)].getX()
		yloc = self.windows[str(windowNo)].getY()
		return (xloc,yloc)
	
	def becomeWindowAdmin(self, windowNo, app, appno):
		return self.windows[str(windowNo)].becomeAdmin(app, appno)
		
	def stopBeingWindowAdmin(self, windowNo, app, appno):
		return self.windows[str(windowNo)].stopBeingAdmin(app, appno)
	
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
	
	def newCircle(self, owner, app, appno, windowNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides):
		if(coorSys=="prop"):
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
			radius = self.winWidPropToPix(windowNo, radius)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			radius = self.surfWidMetToPix(surfaceNo, radius)
		newCir = circle(owner, app, appno, x, y, radius, lineColor, lineWidth, fillColor, sides)
		elementNo = self.newElement(newCir, windowNo)
		return elementNo
	
	def newCircleWithID(self, owner, app, appno, ID, windowNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides):
		elementNo = self.newCircle(owner, app, appno, windowNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
		
	def setCirclePos(self, elementNo, xLoc, yLoc, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xLoc = self.winWidPropToPix(windowNo, xLoc)
			yLoc = self.winHeiPropToPix(windowNo, yLoc)
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.elements[str(elementNo)].setCenter(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != windowNo):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(windowNo)].addElement(elementNo)
		
	def setCircleRad(self, elementNo, radius, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			radius = self.winWidPropToPix(windowNo, radius)
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			radius = self.surfWidMetToPix(surfaceNo, radius)
		self.elements[str(elementNo)].setRadius(radius)
		
	def getCircleRad(self, elementNo):
		rad = self.elements[str(elementNo)].getRadius()
		return rad
		
	def getCirclePos(self, elementNo):
		xloc = self.elements[str(elementNo)].getCenterX()
		yloc = self.elements[str(elementNo)].getCenterY()
		return (xloc,yloc)
	
	def getCircleSides(self, elementNo):
		sides = self.elements[str(elementNo)].getSides()
		return sides
	
	def setCircleSides(self, elementNo, sides):
		self.elements[str(elementNo)].setSides(sides)
	
	def getEleType(self, elementNo):
		return self.elements[str(elementNo)].checkType()
	
	def setCircleFill(self, elementNo, color):
		self.elements[str(elementNo)].setFillColor(color)
		
	def setCircleLine(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
		
	def setCircleLineWidth(self, elementNo, width):
		self.elements[str(elementNo)].setLineWidth(width)
		
	def getCircleFill(self, elementNo):
		return self.elements[str(elementNo)].getFillColor()
		
	def getCircleLine(self, elementNo):
		return self.elements[str(elementNo)].getLineColor()
	
	def getCircleLineWidth(self, elementNo):
		return self.elements[str(elementNo)].getLineWidth()
	
	def upToDateCircle(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def borderTest(self, elementNo):
		return self.elements[str(elementNo)].borderTest()
	
	def newLine(self, owner, app, appno, windowNo, x1, y1, x2, y2, coorSys, color, width):
		if(coorSys=="prop"):
			x1 = self.winWidPropToPix(windowNo, x1)
			y1 = self.winHeiPropToPix(windowNo, y1)
			x2 = self.winWidPropToPix(windowNo, x2)
			y2 = self.winHeiPropToPix(windowNo, y2)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x1 = self.surfWidMetToPix(surfaceNo, x1)
			y1 = self.surfHeiMetToPix(surfaceNo, y1)
			x2 = self.surfWidMetToPix(surfaceNo, x2)
			y2 = self.surfHeiMetToPix(surfaceNo, y2)
		newLine = line(owner, app, appno, x1, y1, x2, y2, color, width)
		elementNo = self.newElement(newLine, windowNo)
		return elementNo
	
	def newLineWithID(self, owner, app, appno, ID, windowNo, x1, y1, x2, y2, coorSys, color, width):
		elementNo = self.newLine(owner, app, appno, windowNo, x1, y1, x2, y2, coorSys, color, width)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftLine(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		start = self.getLineStart(elementNo)
		end = self.getLineEnd(elementNo)
		self.elements[str(elementNo)].setStart(start[0]+xDist,start[1]+yDist)
		self.elements[str(elementNo)].setEnd(end[0]+xDist,end[1]+yDist)
		
	def relocateLine(self, elementNo, refPoint, x, y, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		orig = (0,0)
		if(refPoint==0):
			orig = self.getLineStart(elementNo)
		elif(refPoint==1):
			orig = self.getLineEnd(elementNo)
		differences = (x-orig[0],y-orig[1])
		self.shiftLine(elementNo, differences[0], differences[1], "pix")
	
	def setLineStart(self,elementNo,x,y,coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setStart(x,y)
		
	def setLineEnd(self,elementNo,x,y,coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
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
	
	def getLineWidth(self, elementNo):
		width = self.elements[str(elementNo)].getWidth()
		return width
	
	def setLineWidth(self, elementNo, width):
		self.elements[str(elementNo)].setWidth(width)
		
	def upToDateLine(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newLineStrip(self, owner, app, appno, windowNo, x, y, coorSys, color, width):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newLineStrip = lineStrip(owner, app, appno, x, y, color, width)
		elementNo = self.newElement(newLineStrip, windowNo)
		return elementNo
	
	def newLineStripWithID(self, owner, app, appno, ID, windowNo, x, y, coorSys, color, width):
		elementNo = self.newLineStrip(owner, app, appno, windowNo, x, y, coorSys, color, width)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftLineStrip(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		count = self.getLineStripPointsCount(elementNo)
		for x in range(0,count):
			orig = self.getLineStripPoint(elementNo, x)
			self.moveLineStripPoint(elementNo, x, orig[0]+xDist, orig[1]+yDist, "pix")
		
	def relocateLineStrip(self, elementNo, refPoint, x, y, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		orig = self.getLineStripPoint(elementNo, refPoint)
		differences = (x-orig[0],y-orig[1])
		self.shiftLineStrip(elementNo, differences[0], differences[1], "pix")
	
	def addLineStripPoint(self, elementNo, x, y, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPoint(x,y)
		
	def addLineStripPointAt(self, elementNo, x, y, coorSys, index):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPointAt(int(x),int(y),int(index))
		
	def getLineStripPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def moveLineStripPoint(self, elementNo, pointNo, x, y, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setPoint(pointNo, x, y)
		
	def getLineStripColor(self, elementNo):
		color = self.elements[str(elementNo)].getColor()
		return color
	
	def setLineStripColor(self, elementNo, color):
		self.elements[str(elementNo)].setColor(color)
		
	def getLineStripWidth(self, elementNo):
		width = self.elements[str(elementNo)].getWidth()
		return width
	
	def setLineStripWidth(self, elementNo, width):
		self.elements[str(elementNo)].setWidth(width)
		
	def getLineStripPointsCount(self, elementNo):
		return self.elements[str(elementNo)].getNumPoints()
	
	def setLineStripContent(self, elementNo, content):
		self.elements[str(elementNo)].setContent(content)
		
	def upToDateLineStrip(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newPolygon(self, owner, app, appno, windowNo, x, y, coorSys, lineColor, lineWidth, fillColor):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newPoly = polygon(owner, app, appno, x, y, lineColor, lineWidth, fillColor)
		elementNo = self.newElement(newPoly, windowNo)
		return elementNo
	
	def newPolygonWithID(self, owner, app, appno, ID, windowNo, x, y, coorSys, lineColor, lineWidth, fillColor):
		elementNo = self.newPolygon(owner, app, appno, windowNo, x, y, coorSys, lineColor, lineWidth, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftPolygon(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		count = self.getPolygonPointsCount(elementNo)
		for x in range(0,count):
			orig = self.getPolygonPoint(elementNo, x)
			self.movePolygonPoint(elementNo, x, orig[0]+xDist, orig[1]+yDist, "pix")
		
	def relocatePolygon(self, elementNo, refPoint, x, y, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		orig = self.getPolygonPoint(elementNo, refPoint)
		differences = (x-orig[0],y-orig[1])
		self.shiftPolygon(elementNo, differences[0], differences[1], "pix")
	
	def addPolygonPoint(self, elementNo, x, y, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPoint(x,y)
		
	def getPolygonPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def movePolygonPoint(self, elementNo, pointNo, x, y, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setPoint(pointNo, x, y)
		
	def getPolygonFillColor(self, elementNo):
		color = self.elements[str(elementNo)].getFillColor()
		return color
	
	def setPolygonFillColor(self, elementNo, color):
		self.elements[str(elementNo)].setFillColor(color)
		
	def getPolygonLineColor(self, elementNo):
		color = self.elements[str(elementNo)].getLineColor()
		return color
	
	def getPolygonLineWidth(self, elementNo):
		color = self.elements[str(elementNo)].getLineWidth()
		return color
	
	def setPolygonLineColor(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
		
	def setPolygonLineWidth(self, elementNo, width):
		self.elements[str(elementNo)].setLineWidth(width)
		
	def getPolygonPointsCount(self, elementNo):
		return self.elements[str(elementNo)].getNumPoints()
	
	def upToDatePolygon(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newRectangle(self, owner, app, appno, windowNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
			width = self.winWidPropToPix(windowNo, width)
			height = self.winHeiPropToPix(windowNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			width = self.surfWidMetToPix(surfaceNo, width)
			height = self.surfHeiMetToPix(surfaceNo, height)
		newRect = rectangle(owner, app, appno, x, y, width, height, lineColor, lineWidth, fillColor)
		elementNo = self.newElement(newRect, windowNo)
		return elementNo
	
	def newRectangleWithID(self, owner, app, appno, ID, windowNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor):
		elementNo = self.newRectangle(owner, app, appno, windowNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setRectangleTopLeft(self, elementNo, x, y, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setTopLeft(x,y)
		origWin = self.findElement(elementNo)
		if(origWin != windowNo):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(windowNo)].addElement(elementNo)
			
	def shiftRectangle(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getRectangleTopLeft(elementNo)
		self.elements[str(elementNo)].setTopLeft(orig[0]+xDist,orig[1]+yDist)
		
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
	
	def setRectangleWidth(self, elementNo, width, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			width = int(self.winWidPropToPix(windowNo, width))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.elements[str(elementNo)].setWidth(width)
		
	def getRectangleWidth(self, elementNo):
		return int(self.elements[str(elementNo)].getWidth())
		
	def setRectangleHeight(self, elementNo, height, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			height = int(self.winHeiPropToPix(windowNo, height))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			height = self.surfHeiMetToPix(surfaceNo, height)
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
	
	def getRectangleLineWidth(self, elementNo):
		color = self.elements[str(elementNo)].getLineWidth()
		return color
	
	def setRectangleLineColor(self, elementNo, color):
		self.elements[str(elementNo)].setLineColor(color)
		
	def setRectangleLineWidth(self, elementNo, width):
		self.elements[str(elementNo)].setLineWidth(width)
	
	def upToDateRectangle(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newTexRectangle(self, owner, app, appno, windowNo, x, y, width, height, coorSys, texture):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
			width = self.winWidPropToPix(windowNo, width)
			height = self.winHeiPropToPix(windowNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			width = self.surfWidMetToPix(surfaceNo, width)
			height = self.surfHeiMetToPix(surfaceNo, height)
		newRect = texRectangle(owner, app, appno, x, y, width, height, texture)
		elementNo = self.newElement(newRect, windowNo)
		return elementNo
	
	def newTexRectangleWithID(self, owner, app, appno, ID, windowNo, x, y, width, height, coorSys, texture):
		elementNo = self.newTexRectangle(owner, app, appno, windowNo, x, y, width, height, coorSys, texture)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setTexRectangleTexture(self, elementNo, texture):
		self.elements[str(elementNo)].setTexture(texture)
		
	def getTexRectangleTexture(self, elementNo):
		return self.elements[str(elementNo)].getTexture()
	
	def setTexRectangleTopLeft(self, elementNo, x, y, coorSys, windowNo):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(windowNo, x))
			y = int(self.winHeiPropToPix(windowNo, y))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setTopLeft(x,y)
		origWin = self.findElement(elementNo)
		if(origWin != windowNo):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(windowNo)].addElement(elementNo)
			
	def shiftTexRectangle(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getTexRectangleTopLeft(elementNo)
		self.elements[str(elementNo)].setTopLeft(orig[0]+xDist,orig[1]+yDist)
		
	def getTexRectangleTopLeft(self, elementNo):
		xloc = self.elements[str(elementNo)].getTopLeftX()
		yloc = self.elements[str(elementNo)].getTopLeftY()
		return (xloc,yloc)
	
	def getTexRectangleTopRight(self, elementNo):
		xloc = self.elements[str(elementNo)].getTopRightX()
		yloc = self.elements[str(elementNo)].getTopRightY()
		return (xloc,yloc)
	
	def getTexRectangleBottomRight(self, elementNo):
		xloc = self.elements[str(elementNo)].getBottomRightX()
		yloc = self.elements[str(elementNo)].getBottomRightY()
		return (xloc,yloc)

	def getTexRectangleBottomLeft(self, elementNo):
		xloc = self.elements[str(elementNo)].getBottomLeftX()
		yloc = self.elements[str(elementNo)].getBottomLeftY()
		return (xloc,yloc)
	
	def setTexRectangleWidth(self, elementNo, width, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			width = int(self.winWidPropToPix(windowNo, width))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.elements[str(elementNo)].setWidth(width)
		
	def getTexRectangleWidth(self, elementNo):
		return int(self.elements[str(elementNo)].getWidth())
		
	def setTexRectangleHeight(self, elementNo, height, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			height = int(self.winHeiPropToPix(windowNo, height))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			height = self.surfHeiMetToPix(surfaceNo, height)
		self.elements[str(elementNo)].setHeight(height)
		
	def getTexRectangleHeight(self, elementNo):
		return int(self.elements[str(elementNo)].getHeight())
	
	def upToDateTexRectangle(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newText(self, owner, app, appno, windowNo, text, x, y, coorSys, pt, font, color):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(windowNo, x)
			y = self.winHeiPropToPix(windowNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findWindow(windowNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newText = textBox(owner, app, appno, text, x, y, pt, font, color)
		elementNo = self.newElement(newText, windowNo)
		return elementNo
	
	def newTextWithID(self, owner, app, appno, ID, windowNo, text, x, y, coorSys, pt, font, color):
		elementNo = self.newText(owner, app, appno, windowNo, text, x, y, coorSys, pt, font, color)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setText(self, elementNo, text):
		self.elements[str(elementNo)].setText(text)
		
	def getText(self, elementNo):
		return self.elements[str(elementNo)].getText()
	
	def setTextPos(self, elementNo, xLoc, yLoc, coorSys, window):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xLoc = int(self.winWidPropToPix(windowNo, xLoc))
			yLoc = int(self.winHeiPropToPix(windowNo, yLoc))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.elements[str(elementNo)].setLocation(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != window):
			self.windows[str(origWin)].removeElement(elementNo)
			self.windows[str(window)].addElement(elementNo)
			
	def shiftText(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			windowNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(windowNo, xDist))
			yDist = int(self.winHeiPropToPix(windowNo, yDist))
		elif(coorSys=="real"):
			windowNo = self.findElement(elementNo)
			surfaceNo = self.findWindow(windowNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getTextPos(elementNo)
		self.elements[str(elementNo)].setLocation(orig[0]+xDist,orig[1]+yDist)
			
	def removeElement(self, elementNo, window):
		self.elements[str(elementNo)].hide()
		window = str(window)
		removalThread = threading.Thread(target=self.delayedRemove, args=[window,elementNo]) #Creates the display thread
		removalThread.start()
		
	def delayedRemove(self, window, elementNo):
		time.sleep(2)
		self.windows[window].removeElement(elementNo)
			
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
	
	def upToDateText(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def showElement(self,elementNo):
		self.elements[str(elementNo)].show()
		
	def hideElement(self,elementNo):
		self.elements[str(elementNo)].hide()
		
	def checkElementVisibility(self,elementNo):
		return self.elements[str(elementNo)].isVisible()
	
	def subscribeToElement(self, app, elementNo):
		self.elements[str(elementNo)].subscribe(app)
	
	def getElementID(self, elementNo):
		return self.elements[str(elementNo)].getID()
	
	def setElementID(self, elementNo, ID):
		self.elements[str(elementNo)].setID(ID)
		
	def getElementOwner(self, elementNo):
		return self.elements[str(elementNo)].getOwner()
	
	def getElementAppDetails(self, elementNo):
		return self.elements[str(elementNo)].getAppDetails()
	
	def getElementsByID(self, ID):
		found = []
		for x in range(0,len(self.elements)):
			if(self.elements[str(x)].getID()==ID):
				found.append(x)
		return found
	
	def getElementsByOwner(self, owner):
		found = []
		for x in range(0,len(self.elements)):
			if(self.elements[str(x)].getOwner()==owner):
				found.append(x)
		return found
	
	def getElementsByAppName(self, app):
		found = []
		for x in range(0,len(self.elements)):
			if(self.elements[str(x)].getAppDetails()[0]==app):
				found.append(x)
		return found
	
	def getElementsByAppDetails(self, app, appno):
		found = []
		for x in range(0,len(self.elements)):
			details = self.elements[str(x)].getAppDetails()
			if(details[0]==app and details[1]==appno):
				found.append(x)
		return found
	
	def becomeElementAdmin(self, elementNo, app, appno):
		return self.elements[str(elementNo)].becomeAdmin(app, appno)
		
	def stopBeingElementAdmin(self, elementNo, app, appno):
		return self.elements[str(elementNo)].stopBeingAdmin(app, appno)
	
	def getCursors(self,surfaceNo):
		return self.surfaces[str(surfaceNo)].getCursors()
	
	def getWindows(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getWindows()
	
	def getElements(self, windowNo):
		return self.windows[str(windowNo)].getElements()
	
	def getVisibleElements(self, windowNo):
		found = []
		orig = self.windows[str(windowNo)].getElements()
		for x in range(0, len(orig)):
			try:
				if(self.elements[orig[x]].isVisible()):
					found.append(orig[x])
			except IndexError, e:
				pass
		return found
	
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