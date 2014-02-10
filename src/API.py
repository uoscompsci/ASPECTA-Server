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
		if cmd == 'new_cursor': #Creates a new cursor given a surface and coordinates, the ID number for that cursor is returned
			cursorNo = self.GUI.newCursor(pieces[1],pieces[2],pieces[3])
			print("Cursor Number: " + str(cursorNo))
		if cmd == 'mouse_l': #Clicks the left mouse button down on the selected cursor
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
