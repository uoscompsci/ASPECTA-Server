from GUI import *

class apiMessageParser:
	__slots__ = ['GUI']
	
	def __init__(self):
		self.GUI=GUI()
			
	def newSurface(self,pieces):
		surfaceNo = self.GUI.newSurface()
		print("Surface Number: " + str(surfaceNo))
		
	def newCursor(self,pieces):
		cursorNo = self.GUI.newCursor(pieces[1],pieces[2],pieces[3])
		print("Cursor Number: " + str(cursorNo))
		
	def newWindow(self,pieces):
		windowNo = self.GUI.newWindow(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5],pieces[6])
		print("Window Number: " + str(windowNo))
		
	def mouseLeftDown(self,pieces):
		loc = self.GUI.leftDown(pieces[1])
		print "Left mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mouseLeftUp(self,pieces):
		loc = self.GUI.leftUp(pieces[1])
		print "Left mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def mouseMiddleDown(self,pieces):
		loc = self.GUI.middleDown(pieces[1])
		print "Middle mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mouseMiddleUp(self,pieces):
		loc = self.GUI.middleUp(pieces[1])
		print "Middle mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def mouseRightDown(self,pieces):
		loc = self.GUI.rightDown(pieces[1])
		print "Right mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def mouseRightUp(self,pieces):
		loc = self.GUI.rightUp(pieces[1])
		print "Right mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		
	def moveCursor(self,pieces):
		self.GUI.moveCursor(pieces[1],pieces[2],pieces[3])
		
	def relocateCursor(self,pieces):
		self.GUI.setCursorPos(pieces[1],pieces[2],pieces[3],pieces[4])
		
	def getCursorPosition(self,pieces):
		loc = self.GUI.getCursorPos(pieces[1])
		print "Cursor at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def moveWindow(self,pieces):
		self.GUI.moveWindow(pieces[1],pieces[2],pieces[3])
		
	def relocateWindow(self,pieces):
		self.GUI.setWindowPos(pieces[1],pieces[2],pieces[3],pieces[4])
		
	def setWindowWidth(self,pieces):
		self.GUI.setWindowWidth(pieces[1],pieces[2])
		
	def setWindowHeight(self,pieces):
		self.GUI.setWindowHeight(pieces[1],pieces[2])
		
	def getWindowPosition(self,pieces):
		loc = self.GUI.getWindowPos(pieces[1])
		print "Window at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def getWindowWidth(self,pieces):
		width = self.GUI.getWindowWidth(pieces[1])
		print "Window width = " + str(width)
		
	def getWindowHeight(self,pieces):
		height = self.GUI.getWindowHeight(pieces[1])
		print "Window height = " + str(height)
		
	def stretchWindowDown(self,pieces):
		self.GUI.stretchWindowDown(pieces[1],pieces[2])
		
	def stretchWindowUp(self,pieces):
		self.GUI.stretchWindowUp(pieces[1],pieces[2])
		
	def stretchWindowLeft(self,pieces):	
		self.GUI.stretchWindowLeft(pieces[1],pieces[2])
		
	def stretchWindowRight(self,pieces):
		self.GUI.stretchWindowRight(pieces[1],pieces[2])
		
	def setWindowName(self,pieces):
		self.GUI.setWindowName(pieces[1],pieces[2])
		
	def getWindowName(self,pieces):
		name = self.GUI.getWindowName(pieces[1])
		print "Window name = " + name
		
	messages = {'new_surface' : newSurface,
			'new_cursor' : newCursor,
			'new_window' : newWindow,
			'mouse_l' : mouseLeftDown,
			'mouse_lu' : mouseLeftUp,
			'mouse_m' : mouseMiddleDown,
			'mouse_mu' : mouseMiddleUp,
			'mouse_r' : mouseRightDown,
			'mouse_ru' : mouseRightUp,
			'move_cursor' : moveCursor,
			'relocate_cursor' : relocateCursor,
			'get_cursor_pos' : getCursorPosition,
			'move_window' : moveWindow,
			'relocate_window' : relocateWindow,	
			'set_window_width' : setWindowWidth,
			'set_window_height' : setWindowHeight,
			'get_window_pos' : getWindowPosition,
			'get_window_width' : getWindowWidth,
			'get_window_height' : getWindowHeight,
			'stretch_window_down' : stretchWindowDown,
			'stretch_window_up' : stretchWindowUp,
			'stretch_window_left' : stretchWindowLeft,
			'stretch_window_right' : stretchWindowRight,
			'set_window_name' : setWindowName,
			'get_window_name' : getWindowName
	}
	
	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		self.messages[pieces[0]](self,pieces)