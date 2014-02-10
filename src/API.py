from GUI import *

class apiMessageParser:
	__slots__ = ['GUI']
	
	def __init__(self):
		self.GUI=GUI()

	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		cmd = pieces[0]
		if cmd == 'new_surface': #Creates a new surface, the ID number for that surface is returned
			surfaceNo = self.GUI.newSurface()
			print("Surface Number: " + str(surfaceNo))
		elif cmd == 'new_cursor': #Creates a new cursor given a surface and coordinates, the ID number for that cursor is returned
			cursorNo = self.GUI.newCursor(pieces[1],pieces[2],pieces[3])
			print("Cursor Number: " + str(cursorNo))
		elif cmd == 'new_window':
			windowNo = self.GUI.newWindow(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5],pieces[6])
			print("Window Number: " + str(windowNo))
		elif cmd == 'mouse_l': #Clicks the left mouse button down on the selected cursor
			loc = self.GUI.leftDown(pieces[1])
			print "Left mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		elif cmd == 'mouse_lu': #Depresses the left mouse button on the selected cursor
			loc = self.GUI.leftUp(pieces[1])
			print "Left mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		elif cmd == 'mouse_m': #Clicks the middle mouse button down on the selected cursor
			loc = self.GUI.middleDown(pieces[1])
			print "Middle mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		elif cmd == 'mouse_mu': #Depresses the middle mouse button on the selected cursor
			loc = self.GUI.middleUp(pieces[1])
			print "Middle mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		elif cmd == 'mouse_r': #Clicks the right mouse button down on the selected cursor
			loc = self.GUI.rightDown(pieces[1])
			print "Right mouse down at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		elif cmd == 'mouse_ru': #Depresses the right mouse button on the selected cursor
			loc = self.GUI.rightUp(pieces[1])
			print "Right mouse up at x = " + str(loc[0]) + " y = " + str(loc[1]) + " held for " + str(loc[2])  + " seconds\n"
		elif cmd == 'move_cursor': #Moves cursor by the specified distance
			self.GUI.moveCursor(pieces[1],pieces[2],pieces[3])
		elif cmd == 'relocate_cursor': #Moves cursor to the specified position on the specified surface
			self.GUI.setCursorPos(pieces[1],pieces[2],pieces[3],pieces[4])
		elif cmd == 'get_cursor_pos': #gets the position of the cursor
			loc = self.GUI.getCursorPos(pieces[1])
			print "Cursor at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		elif cmd == 'move_window':
			self.GUI.moveWindow(pieces[1],pieces[2],pieces[3])
		elif cmd == 'relocate_window':
			self.GUI.setWindowPos(pieces[1],pieces[2],pieces[3],pieces[4])
		elif cmd == 'set_window_width':
			self.GUI.setWindowWidth(pieces[1],pieces[2])
		elif cmd == 'set_window_height':
			self.GUI.setWindowHeight(pieces[1],pieces[2])
		elif cmd == 'get_window_pos':
			loc = self.GUI.getWindowPos(pieces[1])
			print "Window at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		elif cmd == 'get_window_width':
			width = self.GUI.getWindowWidth(pieces[1])
			print "Window width = " + str(width)
		elif cmd == 'get_window_height':
			height = self.GUI.getWindowHeight(pieces[1])
			print "Window height = " + str(height)
		elif cmd == 'stretch_window_down':
			self.GUI.stretchWindowDown(pieces[1],pieces[2])
		elif cmd == 'stretch_window_up':
			self.GUI.stretchWindowUp(pieces[1],pieces[2])
		elif cmd == 'stretch_window_left':
			self.GUI.stretchWindowLeft(pieces[1],pieces[2])
		elif cmd == 'stretch_window_right':
			self.GUI.stretchWindowRight(pieces[1],pieces[2])
		elif cmd == 'set_window_name':
			self.GUI.setWindowName(pieces[1],pieces[2])
		elif cmd == 'get_window_name':
			name = self.GUI.getWindowName(pieces[1])
			print "Window name = " + name