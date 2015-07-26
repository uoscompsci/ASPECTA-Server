from GUIElements import *
import threading
from math import *
import time

class GUI:
	__slots__ = ['surfaces', 'surfaces_lock', 'displays', 'displays_lock', 'cursors', 'cursors_lock', 'lastcur', 'lastsur', 'lastwin', 'lastele' 'canvases', 'canvases_lock', 'elements', 'elements_lock', 'setup_surface_visible']
	
	correctDirect = {'right' : {0 : 'right', 1 : 'bottom', 2 : 'left', 3 : "top"},
				'bottom' : {0 : 'bottom', 1 : 'left', 2 : 'top', 3 : "right"},
				'left' : {0 : 'left', 1 : 'top', 2 : 'right', 3 : "bottom"},
				'top' : {0 : 'top', 1 : 'right', 2 : 'bottom', 3 : "left"}
				}
	
	def __init__(self, width, height):
		parser = SafeConfigParser()
		parser.read("config.ini")
		self.winWidth = parser.getint('display', 'HorizontalRes')
		self.winHeight = parser.getint('display', 'VerticalRes')
		self.lastcur = 0
		self.lastsur = 0
		self.lastwin = 0
		self.lastele = 0
		self.surfaces_lock = threading.Lock()
		self.displays_lock = threading.Lock()
		self.cursors_lock = threading.Lock()
		self.canvases_lock = threading.Lock()
		self.elements_lock = threading.Lock()
		self.cursors = {}
		self.surfaces = {}
		self.canvases = {}
		self.elements = {}
		self.connections = []
		self.surfaces["0"] = surface("server", "server", "0", "setup")
		self.setSurfacePixelWidth(0, width)
		self.setSurfacePixelHeight(0, height)
		self.setup_surface_visible = False
		
	def winWidPropToPix(self, win, prop):
		width = self.getCanvasWidth(win)
		return float(prop)*width
		
	def winHeiPropToPix(self, win, prop):
		height = self.getCanvasHeight(win)
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
		canvases = self.getCanvases(surfaceNo)
		cursors = self.getCursors(surfaceNo)
		for x in range(0,len(canvases)):
			elements = self.getElements(canvases[x])
			for y in range(0,len(elements)):
				self.removeElement(elements[y], canvases[x])
		for x in range(0,len(cursors)):
			self.removeCursor(cursors[x])
		canvasRemovalThread = threading.Thread(target=self.delayedCanvasRemoval, args=[canvases]) #Creates the display thread
		canvasRemovalThread.start()
		
	def delayedCanvasRemoval(self,canvases):
		time.sleep(3)
		for x in range(0,len(canvases)):
			self.removeCanvas(canvases[x])
	
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
			self.setCursorPos(cursorNo, finalLoc[0], finalLoc[1], "pos", surface)
		else:
			self.setCursorPos(cursorNo, finalLoc[0], finalLoc[1], "pos", self.findCursor(cursorNo))
		
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
		
	def setCursorPos(self, cursorNo, xLoc, yLoc, coorSys, surface):
		if(coorSys=="prop"):
			xLoc = self.surfWidPropToPix(surface, xLoc)
			yLoc = self.surfHeiPropToPix(surface, yLoc)
		elif(coorSys=="real"):
			xLoc = self.surfWidMetToPix(surface, xLoc)
			yLoc = self.surfHeiMetToPix(surface, yLoc)
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
	
	def newCanvas(self, owner, app, appno, surface, x, y, xWid, yWid, coorSys, name):
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
		newWin = canvas(owner,app,appno,x,y,xWid,yWid,name)
		canvasNo = 0
		with self.canvases_lock:
			if (len(self.canvases)==0):
				self.canvases[str(1)] = newWin
				canvasNo = 1
				self.lastwin = 1
			else:
				self.lastwin=self.lastwin+1
				self.canvases[str(self.lastwin)] = newWin
				canvasNo = self.lastwin
		self.surfaces[str(surface)].addCanvas(canvasNo)
		return canvasNo
	
	def newCanvasWithID(self, owner, app, appno, ID, surface, x, y, xWid, yWid, coorSys, name):
		canvasNo = self.newCanvas(owner, app, appno, surface, x, y, xWid, yWid, coorSys, name)
		self.canvases[set(canvasNo)].setID(ID)
		return canvasNo
	
	def subscribeToCanvas(self, app, canvasNo):
		self.canvases[str(canvasNo)].subscribe(app)
	
	def getCanvasID(self, canvasNo):
		return self.canvases[str(canvasNo)].getID()
	
	def setCanvasID(self, canvasNo, ID):
		self.canvases[str(canvasNo)].setID(ID)
		
	def getCanvasOwner(self, canvasNo):
		return self.canvases[str(canvasNo)].getOwner()
	
	def getCanvasAppDetails(self, canvasNo):
		return self.canvases[str(canvasNo)].getAppDetails()
	
	def getCanvasesByID(self, ID):
		found = []
		for x in range(0,len(self.canvases)):
			if(self.canvases[str(x)].getID()==ID):
				found.append(x)
		return found
	
	def getCanvasesByOwner(self, owner):
		found = []
		for x in range(0,len(self.canvases)):
			if(self.canvases[str(x)].getOwner()==owner):
				found.append(x)
		return found
	
	def getCanvasesByAppName(self, app):
		found = []
		for x in range(0,len(self.canvases)):
			if(self.canvases[str(x)].getAppDetails()[0]==app):
				found.append(x)
		return found
	
	def getCanvasesByAppDetails(self, app, appno):
		found = []
		for x in range(0,len(self.canvases)):
			details = self.canvases[str(x)].getAppDetails()
			if(details[0]==app and details[1]==appno):
				found.append(x)
		return found
	
	def findCanvas(self, canvasNo):
		location = 0
		for key in self.surfaces:
			if(self.surfaces[key].containsWin(canvasNo)==True):
				location = int(key)
		return location
	
	def moveCanvas(self, canvasNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidPropToPix(surfaceNo, xDist)
			yDist = self.surfHeiPropToPix(surfaceNo, yDist)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		self.canvases[str(canvasNo)].drag(xDist,yDist) #TODO Handle when moves to different screen
		
	def setCanvasPos(self, canvasNo, xLoc, yLoc, coorSys, surface):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			xLoc = self.surfWidPropToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiPropToPix(surfaceNo, yLoc)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.canvases[str(canvasNo)].setLoc(xLoc,yLoc)
		origSur = self.findCanvas(canvasNo)
		if(origSur != surface):
			self.surfaces[str(origSur)].removeCanvas(canvasNo)
			self.surfaces[str(surface)].addCanvas(canvasNo)
			
	def removeCanvas(self,canvasNo):
		surNo = self.findCanvas(canvasNo)
		self.surfaces[str(surNo)].removeCanvas(canvasNo)
		self.canvases.pop(str(canvasNo),None)

	def setCanvasHeight(self,canvasNo,height,coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			height = self.surfHeiPropToPix(surfaceNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			height = self.surfHeiMetToPix(surfaceNo, height)
		self.canvases[str(canvasNo)].setHeight(height)
		
	def setCanvasWidth(self,canvasNo,width,coorSys):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			width = self.surfWidPropToPix(surfaceNo, width)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.canvases[str(canvasNo)].setWidth(width)
		
	def getCanvasHeight(self,canvasNo):
		return self.canvases[str(canvasNo)].getHeight()
	
	def getCanvasWidth(self,canvasNo):
		return self.canvases[str(canvasNo)].getWidth()
	
	def stretchCanvasRight(self,canvasNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfWidPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfWidMetToPix(surfaceNo, dist)
		self.canvases[str(canvasNo)].stretchRight(dist)
		
	def stretchCanvasLeft(self,canvasNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfWidPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfWidMetToPix(surfaceNo, dist)
		self.canvases[str(canvasNo)].stretchLeft(dist)
		
	def stretchCanvasUp(self,canvasNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfHeiPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfHeiMetToPix(surfaceNo, dist)
		self.canvases[str(canvasNo)].stretchUp(dist)
		
	def stretchCanvasDown(self,canvasNo,dist):
		if(coorSys=="prop"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfHeiPropToPix(surfaceNo, dist)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			dist = self.surfHeiMetToPix(surfaceNo, dist)
		self.canvases[str(canvasNo)].stretchDown(dist)
		
	def setCanvasName(self,canvasNo,name):
		self.canvases[str(canvasNo)].setName(name)
		
	def getCanvasName(self,canvasNo):
		return self.canvases[str(canvasNo)].getName()
	
	def getCanvasPos(self, canvasNo):
		xloc = self.canvases[str(canvasNo)].getX()
		yloc = self.canvases[str(canvasNo)].getY()
		return (xloc,yloc)
	
	def becomeCanvasAdmin(self, canvasNo, app, appno):
		return self.canvases[str(canvasNo)].becomeAdmin(app, appno)
		
	def stopBeingCanvasAdmin(self, canvasNo, app, appno):
		return self.canvases[str(canvasNo)].stopBeingAdmin(app, appno)
	
	def findElement(self, elementNo):
		location = 0
		for key in self.canvases:
			if(self.canvases[key].containsEle(elementNo)==True):
				location = int(key)
		return location
	
	def findCursor(self, cursorNo):
		location = -1
		for key in self.surfaces:
			if(self.surfaces[key].containsCur(cursorNo)==True):
				location = int(key)
		return location
	
	def newElement(self,element, canvasNo):
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
		self.canvases[str(canvasNo)].addElement(elementNo)
		return elementNo
	
	def newCircle(self, owner, app, appno, canvasNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides):
		if(coorSys=="prop"):
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
			radius = self.winWidPropToPix(canvasNo, radius)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			radius = self.surfWidMetToPix(surfaceNo, radius)
		newCir = circle(owner, app, appno, x, y, radius, lineColor, lineWidth, fillColor, sides)
		elementNo = self.newElement(newCir, canvasNo)
		return elementNo
	
	def newCircleWithID(self, owner, app, appno, ID, canvasNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides):
		elementNo = self.newCircle(owner, app, appno, canvasNo, x, y, radius, coorSys, lineColor, lineWidth, fillColor, sides)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
		
	def setCirclePos(self, elementNo, xLoc, yLoc, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xLoc = self.winWidPropToPix(canvasNo, xLoc)
			yLoc = self.winHeiPropToPix(canvasNo, yLoc)
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.elements[str(elementNo)].setCenter(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != canvasNo):
			self.canvases[str(origWin)].removeElement(elementNo)
			self.canvases[str(canvasNo)].addElement(elementNo)

	def shiftCircle(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getCirclePos(elementNo)
		self.elements[str(elementNo)].setCenter(float(orig[0])+float(xDist),float(orig[1])+float(yDist))
		
	def setCircleRad(self, elementNo, radius, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			radius = self.winWidPropToPix(canvasNo, radius)
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
	
	def newLine(self, owner, app, appno, canvasNo, x1, y1, x2, y2, coorSys, color, width):
		if(coorSys=="prop"):
			x1 = self.winWidPropToPix(canvasNo, x1)
			y1 = self.winHeiPropToPix(canvasNo, y1)
			x2 = self.winWidPropToPix(canvasNo, x2)
			y2 = self.winHeiPropToPix(canvasNo, y2)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x1 = self.surfWidMetToPix(surfaceNo, x1)
			y1 = self.surfHeiMetToPix(surfaceNo, y1)
			x2 = self.surfWidMetToPix(surfaceNo, x2)
			y2 = self.surfHeiMetToPix(surfaceNo, y2)
		newLine = line(owner, app, appno, x1, y1, x2, y2, color, width)
		elementNo = self.newElement(newLine, canvasNo)
		return elementNo
	
	def newLineWithID(self, owner, app, appno, ID, canvasNo, x1, y1, x2, y2, coorSys, color, width):
		elementNo = self.newLine(owner, app, appno, canvasNo, x1, y1, x2, y2, coorSys, color, width)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftLine(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		start = self.getLineStart(elementNo)
		end = self.getLineEnd(elementNo)
		self.elements[str(elementNo)].setStart(start[0]+xDist,start[1]+yDist)
		self.elements[str(elementNo)].setEnd(end[0]+xDist,end[1]+yDist)
		
	def relocateLine(self, elementNo, refPoint, x, y, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setStart(x,y)
		
	def setLineEnd(self,elementNo,x,y,coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
	
	def newLineStrip(self, owner, app, appno, canvasNo, x, y, coorSys, color, width):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newLineStrip = lineStrip(owner, app, appno, x, y, color, width)
		elementNo = self.newElement(newLineStrip, canvasNo)
		return elementNo
	
	def newLineStripWithID(self, owner, app, appno, ID, canvasNo, x, y, coorSys, color, width):
		elementNo = self.newLineStrip(owner, app, appno, canvasNo, x, y, coorSys, color, width)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftLineStrip(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		count = self.getLineStripPointsCount(elementNo)
		for x in range(0,count):
			orig = self.getLineStripPoint(elementNo, x)
			self.moveLineStripPoint(elementNo, x, orig[0]+xDist, orig[1]+yDist, "pix")
		
	def relocateLineStrip(self, elementNo, refPoint, x, y, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		orig = self.getLineStripPoint(elementNo, refPoint)
		differences = (x-orig[0],y-orig[1])
		self.shiftLineStrip(elementNo, differences[0], differences[1], "pix")
	
	def addLineStripPoint(self, elementNo, x, y, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPoint(x,y)
		
	def addLineStripPointAt(self, elementNo, x, y, coorSys, index):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPointAt(int(x),int(y),int(index))
		
	def getLineStripPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def moveLineStripPoint(self, elementNo, pointNo, x, y, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
	
	def newPolygon(self, owner, app, appno, canvasNo, x, y, coorSys, lineColor, lineWidth, fillColor):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newPoly = polygon(owner, app, appno, x, y, lineColor, lineWidth, fillColor)
		elementNo = self.newElement(newPoly, canvasNo)
		return elementNo
	
	def newPolygonWithID(self, owner, app, appno, ID, canvasNo, x, y, coorSys, lineColor, lineWidth, fillColor):
		elementNo = self.newPolygon(owner, app, appno, canvasNo, x, y, coorSys, lineColor, lineWidth, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def shiftPolygon(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		count = self.getPolygonPointsCount(elementNo)
		for x in range(0,count):
			orig = self.getPolygonPoint(elementNo, x)
			self.movePolygonPoint(elementNo, x, orig[0]+xDist, orig[1]+yDist, "pix")
		
	def relocatePolygon(self, elementNo, refPoint, x, y, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		orig = self.getPolygonPoint(elementNo, refPoint)
		differences = (x-orig[0],y-orig[1])
		self.shiftPolygon(elementNo, differences[0], differences[1], "pix")
	
	def addPolygonPoint(self, elementNo, x, y, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].addPoint(x,y)
		
	def getPolygonPoint(self, elementNo, pointNo):
		xloc = self.elements[str(elementNo)].getPointX(pointNo)
		yloc = self.elements[str(elementNo)].getPointY(pointNo)
		return (xloc,yloc)
	
	def movePolygonPoint(self, elementNo, pointNo, x, y, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
	
	def newRectangle(self, owner, app, appno, canvasNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
			width = self.winWidPropToPix(canvasNo, width)
			height = self.winHeiPropToPix(canvasNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			width = self.surfWidMetToPix(surfaceNo, width)
			height = self.surfHeiMetToPix(surfaceNo, height)
		newRect = rectangle(owner, app, appno, x, y, width, height, lineColor, lineWidth, fillColor)
		elementNo = self.newElement(newRect, canvasNo)
		return elementNo
	
	def newRectangleWithID(self, owner, app, appno, ID, canvasNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor):
		elementNo = self.newRectangle(owner, app, appno, canvasNo, x, y, width, height, coorSys, lineColor, lineWidth, fillColor)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setRectangleTopLeft(self, elementNo, x, y, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setTopLeft(x,y)
		origWin = self.findElement(elementNo)
		if(origWin != canvasNo):
			self.canvases[str(origWin)].removeElement(elementNo)
			self.canvases[str(canvasNo)].addElement(elementNo)
			
	def shiftRectangle(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getRectangleTopLeft(elementNo)
		self.elements[str(elementNo)].setTopLeft(orig[0]+float(xDist),orig[1]+float(yDist))
		
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
			canvasNo = self.findElement(elementNo)
			width = int(self.winWidPropToPix(canvasNo, width))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.elements[str(elementNo)].setWidth(width)
		
	def getRectangleWidth(self, elementNo):
		return int(self.elements[str(elementNo)].getWidth())
		
	def setRectangleHeight(self, elementNo, height, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			height = int(self.winHeiPropToPix(canvasNo, height))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
	
	def newTexRectangle(self, owner, app, appno, canvasNo, x, y, width, height, coorSys, texture):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
			width = self.winWidPropToPix(canvasNo, width)
			height = self.winHeiPropToPix(canvasNo, height)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
			width = self.surfWidMetToPix(surfaceNo, width)
			height = self.surfHeiMetToPix(surfaceNo, height)
		newRect = texRectangle(owner, app, appno, x, y, width, height, texture)
		elementNo = self.newElement(newRect, canvasNo)
		return elementNo
	
	def newTexRectangleWithID(self, owner, app, appno, ID, canvasNo, x, y, width, height, coorSys, texture):
		elementNo = self.newTexRectangle(owner, app, appno, canvasNo, x, y, width, height, coorSys, texture)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setTexRectangleTexture(self, elementNo, texture):
		self.elements[str(elementNo)].setTexture(texture)
		
	def getTexRectangleTexture(self, elementNo):
		return self.elements[str(elementNo)].getTexture()
	
	def setTexRectangleTopLeft(self, elementNo, x, y, coorSys, canvasNo):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			x = int(self.winWidPropToPix(canvasNo, x))
			y = int(self.winHeiPropToPix(canvasNo, y))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		self.elements[str(elementNo)].setTopLeft(x,y)
		origWin = self.findElement(elementNo)
		if(origWin != canvasNo):
			self.canvases[str(origWin)].removeElement(elementNo)
			self.canvases[str(canvasNo)].addElement(elementNo)
			
	def shiftTexRectangle(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
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
			canvasNo = self.findElement(elementNo)
			width = int(self.winWidPropToPix(canvasNo, width))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			width = self.surfWidMetToPix(surfaceNo, width)
		self.elements[str(elementNo)].setWidth(width)
		
	def getTexRectangleWidth(self, elementNo):
		return int(self.elements[str(elementNo)].getWidth())
		
	def setTexRectangleHeight(self, elementNo, height, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			height = int(self.winHeiPropToPix(canvasNo, height))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			height = self.surfHeiMetToPix(surfaceNo, height)
		self.elements[str(elementNo)].setHeight(height)
		
	def getTexRectangleHeight(self, elementNo):
		return int(self.elements[str(elementNo)].getHeight())
	
	def upToDateTexRectangle(self,elementNo):
		return self.elements[str(elementNo)].update()
	
	def newText(self, owner, app, appno, canvasNo, text, x, y, coorSys, pt, font, color):
		if(coorSys=="prop"):
			x = self.winWidPropToPix(canvasNo, x)
			y = self.winHeiPropToPix(canvasNo, y)
		elif(coorSys=="real"):
			surfaceNo = self.findCanvas(canvasNo)
			x = self.surfWidMetToPix(surfaceNo, x)
			y = self.surfHeiMetToPix(surfaceNo, y)
		newText = textBox(owner, app, appno, text, x, y, pt, font, color)
		elementNo = self.newElement(newText, canvasNo)
		return elementNo
	
	def newTextWithID(self, owner, app, appno, ID, canvasNo, text, x, y, coorSys, pt, font, color):
		elementNo = self.newText(owner, app, appno, canvasNo, text, x, y, coorSys, pt, font, color)
		self.elements[set(elementNo)].setID(ID)
		return elementNo
	
	def setText(self, elementNo, text):
		self.elements[str(elementNo)].setText(text)
		
	def getText(self, elementNo):
		return self.elements[str(elementNo)].getText()
	
	def setTextPos(self, elementNo, xLoc, yLoc, coorSys, canvas):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xLoc = int(self.winWidPropToPix(canvasNo, xLoc))
			yLoc = int(self.winHeiPropToPix(canvasNo, yLoc))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xLoc = self.surfWidMetToPix(surfaceNo, xLoc)
			yLoc = self.surfHeiMetToPix(surfaceNo, yLoc)
		self.elements[str(elementNo)].setLocation(xLoc,yLoc)
		origWin = self.findElement(elementNo)
		if(origWin != canvas):
			self.canvases[str(origWin)].removeElement(elementNo)
			self.canvases[str(canvas)].addElement(elementNo)
			
	def shiftText(self, elementNo, xDist, yDist, coorSys):
		if(coorSys=="prop"):
			canvasNo = self.findElement(elementNo)
			xDist = int(self.winWidPropToPix(canvasNo, xDist))
			yDist = int(self.winHeiPropToPix(canvasNo, yDist))
		elif(coorSys=="real"):
			canvasNo = self.findElement(elementNo)
			surfaceNo = self.findCanvas(canvasNo)
			xDist = self.surfWidMetToPix(surfaceNo, xDist)
			yDist = self.surfHeiMetToPix(surfaceNo, yDist)
		orig = self.getTextPos(elementNo)
		self.elements[str(elementNo)].setLocation(orig[0]+xDist,orig[1]+yDist)
			
	def removeElement(self, elementNo, canvas):
		self.elements[str(elementNo)].hide()
		canvas = str(canvas)
		removalThread = threading.Thread(target=self.delayedRemove, args=[canvas,elementNo]) #Creates the display thread
		removalThread.start()
		
	def delayedRemove(self, canvas, elementNo):
		time.sleep(2)
		self.canvases[canvas].removeElement(elementNo)
			
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
	
	def getCanvases(self, surfaceNo):
		return self.surfaces[str(surfaceNo)].getCanvases()
	
	def getElements(self, canvasNo):
		return self.canvases[str(canvasNo)].getElements()
	
	def getVisibleElements(self, canvasNo):
		found = []
		orig = self.canvases[str(canvasNo)].getElements()
		for x in range(0, len(orig)):
			try:
				if(self.elements[orig[x]].isVisible()):
					found.append(orig[x])
			except IndexError, e:
				pass
		return found
	
	def getClickedElements(self, surfaceNo, x, y):
		canvases = self.getCanvases(surfaceNo)
		hits = []
		for canvasNo in canvases:
			elements = self.getElements(canvasNo)
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