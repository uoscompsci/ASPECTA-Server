from GUI import *

class apiMessageParser:
	__slots__ = ['GUI']
	
	def __init__(self):
		self.GUI=GUI()
			
	def newSurf(self,pieces):
		surfaceNo = self.GUI.newSurface()
		print("Surface Number: " + str(surfaceNo))
		
	def newCurs(self,pieces):
		cursorNo = self.GUI.newCursor(pieces[1],pieces[2],pieces[3])
		print("Cursor Number: " + str(cursorNo))
		
	def newWind(self,pieces):
		windowNo = self.GUI.newWindow(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5],pieces[6])
		print("Window Number: " + str(windowNo))
		
	def mousel(self,pieces):
		loc = self.GUI.leftDown(pieces[1])
		print "Left mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mouselu(self,pieces):
		loc = self.GUI.leftUp(pieces[1])
		print "Left mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def mousem(self,pieces):
		loc = self.GUI.middleDown(pieces[1])
		print "Middle mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mousemu(self,pieces):
		loc = self.GUI.middleUp(pieces[1])
		print "Middle mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def mouser(self,pieces):
		loc = self.GUI.rightDown(pieces[1])
		print "Right mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mouseru(self,pieces):
		loc = self.GUI.rightUp(pieces[1])
		print "Right mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def moveCurs(self,pieces):
		self.GUI.moveCursor(pieces[1],pieces[2],pieces[3])
		
	def reloCurs(self,pieces):
		self.GUI.setCursorPos(pieces[1],pieces[2],pieces[3],pieces[4])
		
	def getCursPos(self,pieces):
		loc = self.GUI.getCursorPos(pieces[1])
		print "Cursor at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def moveWind(self,pieces):
		self.GUI.moveWindow(pieces[1],pieces[2],pieces[3])
		
	def relocWind(self,pieces):
		self.GUI.setWindowPos(pieces[1],pieces[2],pieces[3],pieces[4])
		
	def setWindWid(self,pieces):
		self.GUI.setWindowWidth(pieces[1],pieces[2])
		
	def setWindHeigh(self,pieces):
		self.GUI.setWindowHeight(pieces[1],pieces[2])
		
	def getWindPos(self,pieces):
		loc = self.GUI.getWindowPos(pieces[1])
		print "Window at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def getWindWid(self,pieces):
		width = self.GUI.getWindowWidth(pieces[1])
		print "Window width = " + str(width)
		
	def getWindHeigh(self,pieces):
		height = self.GUI.getWindowHeight(pieces[1])
		print "Window height = " + str(height)
		
	def strWindDown(self,pieces):
		self.GUI.stretchWindowDown(pieces[1],pieces[2])
		
	def strWindUp(self,pieces):
		self.GUI.stretchWindowUp(pieces[1],pieces[2])
		
	def strWindLeft(self,pieces):	
		self.GUI.stretchWindowLeft(pieces[1],pieces[2])
		
	def strWindRight(self,pieces):
		self.GUI.stretchWindowRight(pieces[1],pieces[2])
		
	def setWindName(self,pieces):
		self.GUI.setWindowName(pieces[1],pieces[2])
		
	def getWindName(self,pieces):
		name = self.GUI.getWindowName(pieces[1])
		print "Window name = " + name
		
	messages = {'new_surface' : newSurf,
			'new_cursor' : newCurs,
			'new_window' : newWind,
			'mouse_l' : mousel,
			'mouse_lu' : mouselu,
			'mouse_m' : mousem,
			'mouse_mu' : mousemu,
			'mouse_r' : mouser,
			'mouse_ru' : mouseru,
			'move_cursor' : moveCurs,
			'relocate_cursor' : reloCurs,
			'get_cursor_pos' : getCursPos,
			'move_window' : moveWind,
			'relocate_window' : relocWind,	
			'set_window_width' : setWindWid,
			'set_window_height' : setWindHeigh,
			'get_window_pos' : getWindPos,
			'get_window_width' : getWindWid,
			'get_window_height' : getWindHeigh,
			'stretch_window_down' : strWindDown,
			'stretch_window_up' : strWindUp,
			'stretch_window_left' : strWindLeft,
			'stretch_window_right' : strWindRight,
			'set_window_name' : setWindName,
			'get_window_name' : getWindName
	}
	
	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		self.messages[pieces[0]](self,pieces)