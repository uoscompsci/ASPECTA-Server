from GUI import *

class apiMessageProcessor:
	__slots__ = ['GUI']
	
	def __init__(self):
		self.GUI=GUI()

	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		cmd = pieces[0]
		if cmd == 'new_surface':
			surfaceNo = self.GUI.newSurface()
			print("Surface Number: " + str(surfaceNo))
		if cmd == 'new_cursor':
			print 'here1'
			cursorNo = self.GUI.newCursor(pieces[1],pieces[2],pieces[3])
			print("Cursor Number: " + str(cursorNo))
		if cmd == 'mouse_l':
			loc = self.GUI.leftDown(pieces[1])
			print "Left mouse down at x = " + loc[0] + " y = " + loc[1] + "\n"
		elif cmd == 'mouse_lu':
			loc = self.GUI.leftUp(pieces[1])
			print "Left mouse up at x = " + loc[0] + " y = " + loc[1] + " held for " + str(loc[2])  + " seconds\n"
		elif cmd == 'mouse_m':
			loc = self.GUI.middleDown(pieces[1])
			print "Middle mouse down at x = " + loc[0] + " y = " + loc[1] + "\n"
		elif cmd == 'mouse_mu':
			loc = self.GUI.middleUp(pieces[1])
			print "Middle mouse up at x = " + loc[0] + " y = " + loc[1] + " held for " + str(loc[2])  + " seconds\n"
		elif cmd == 'mouse_r':
			loc = self.GUI.rightDown(pieces[1])
			print "Right mouse down at x = " + loc[0] + " y = " + loc[1] + "\n"
		elif cmd == 'mouse_ru':
			loc = self.GUI.rightUp(pieces[1])
			print "Right mouse up at x = " + loc[0] + " y = " + loc[1] + " held for " + str(loc[2])  + " seconds\n"
