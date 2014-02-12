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
		
	def newCircle(self,pieces):
		elementNo = self.GUI.newCircle(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5],pieces[6])
		print("Element Number: " + str(elementNo))
		
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
		
	def relocateCircle(self,pieces):
		name = self.GUI.setCirclePos(pieces[1],pieces[2],pieces[3],pieces[4])
		
	def getCirclePosition(self,pieces):
		loc = self.GUI.getCirclePos(pieces[1])
		print "Circle at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	messages = {'new_surface' : (newSurface,1), #No parameters
			'new_cursor' : (newCursor,4), #[1]=SurfaceNo  [2]=x  [3]=y
			'new_window' : (newWindow,7), #[1]=SurfaceNo  [2]=x  [3]=y  [4]=width  [5]=height  [6]=name
			'new_circle' : (newCircle,7), #[1]=WindowNo  [2]=x  [3]=y  [4]=Radius  [5]=LineColor  [6]=FillColor
			'mouse_l' : (mouseLeftDown,2), #[1]=CursorNo
			'mouse_lu' : (mouseLeftUp,2), #[1]=CursorNo
			'mouse_m' : (mouseMiddleDown,2), #[1]=CursorNo
			'mouse_mu' : (mouseMiddleUp,2), #[1]=CursorNo
			'mouse_r' : (mouseRightDown,2), #[1]=CursorNo
			'mouse_ru' : (mouseRightUp,2), #[1]=CursorNo
			'move_cursor' : (moveCursor,4), #[1]=CursorNo  [2]=xDistance  [3]=yDistance
			'relocate_cursor' : (relocateCursor,5), #[1]=CursorNo  [2]=x  [3]=y  [4]=Surface
			'get_cursor_pos' : (getCursorPosition,2), #[1]=CursorNo
			'move_window' : (moveWindow,4), #[1]=WindowNo  [2]=xDistance  [3]=yDistance
			'relocate_window' : (relocateWindow,5),	#[1]=WindowNo  [2]=x  [3]=y  [4]=Surface
			'set_window_width' : (setWindowWidth,3), #[1]=WindowNo  [2]=Width
			'set_window_height' : (setWindowHeight,3), #[1]=WindowNo  [2]=Height
			'get_window_pos' : (getWindowPosition,2), #[1]=WindowNo
			'get_window_width' : (getWindowWidth,2), #[1]=WindowNo
			'get_window_height' : (getWindowHeight,2), #[1]=WindowNo
			'stretch_window_down' : (stretchWindowDown,3), #[1]=WindowNo  [2]=Distance
			'stretch_window_up' : (stretchWindowUp,3), #[1]=WindowNo  [2]=Distance
			'stretch_window_left' : (stretchWindowLeft,3), #[1]=WindowNo  [2]=Distance
			'stretch_window_right' : (stretchWindowRight,3), #[1]=WindowNo  [2]=Distance
			'set_window_name' : (setWindowName,3), #[1]=WindowNo  [2]=Name
			'get_window_name' : (getWindowName,2), #[1]=WindowNo
			'relocate_circle' : (relocateCircle,5), #[1]=ElementNo  [2]=x  [3]=y  [4]=windowNo
			'get_circle_pos' : (getCirclePosition,2) #[1]=ElementNo
	}
	
	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		try:
			if(len(pieces)==self.messages[pieces[0]][1]):
				self.messages[pieces[0]][0](self,pieces)
			else:
				print "Invalid number of arguments (" + str(len(pieces)-1) + " instead of " + str(self.messages[pieces[0]][1]-1) + ")"
		except KeyError:
			print "Invalid API call"