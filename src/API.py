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
		
	def newLine(self,pieces):
		elementNo = self.GUI.newLine(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5],pieces[6])
		print("Element Number: " + str(elementNo))
		
	def newLineStrip(self,pieces):
		elementNo = self.GUI.newLineStrip(pieces[1],pieces[2],pieces[3],pieces[4])
		print("Element Number: " + str(elementNo))
		
	def newPolygon(self,pieces):
		elementNo = self.GUI.newPolygon(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5])
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
		
	def getElementType(self,pieces):
		type = self.GUI.getEleType(pieces[1])
		print "Element type = " + type
		
	def setCircleLineColor(self,pieces):
		self.GUI.setCircleLine(pieces[1],pieces[2])
		
	def setCircleFillColor(self,pieces):
		self.GUI.setCircleFill(pieces[1],pieces[2])
		
	def getCircleLineColor(self,pieces):
		color = self.GUI.getCircleLine(pieces[1])
		print "Line color = " + color
		
	def getCircleFillColor(self,pieces):
		color = self.GUI.getCircleFill(pieces[1])
		print "Fill color = " + color
		
	def getCircleRadius(self,pieces):
		radius = self.GUI.getCircleRad(pieces[1])
		print "Radius = " + radius
		
	def setCircleRadius(self,pieces):
		self.GUI.setCircleRad(pieces[1],pieces[2])
		
	def getLineStart(self,pieces):
		loc = self.GUI.getLineStart(pieces[1])
		print "Line start at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def getLineEnd(self,pieces):
		loc = self.GUI.getLineEnd(pieces[1])
		print "Line end at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def setLineStart(self,pieces):
		self.GUI.setLineStart(pieces[1],pieces[2],pieces[3])
		
	def setLineEnd(self,pieces):
		self.GUI.setLineEnd(pieces[1],pieces[2],pieces[3])
		
	def setLineColor(self,pieces):
		self.GUI.setLineColor(pieces[1],pieces[2])
		
	def getLineColor(self,pieces):
		color = self.GUI.getLineColor(pieces[1])
		print "Line color = " + color
		
	def addLineStripPoint(self,pieces):
		self.GUI.addLineStripPoint(pieces[1],pieces[2],pieces[3])
		
	def getLineStripPoint(self,pieces):
		loc = self.GUI.getLineStripPoint(pieces[1],pieces[2])
		print "Point at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def moveLineStripPoint(self,pieces):
		self.GUI.moveLineStripPoint(pieces[1],pieces[2],pieces[3],pieces[4])		
		
	def getLineStripColor(self,pieces):
		color = self.GUI.getLineStripColor(pieces[1])
		print "Line strip color = " + color
		
	def setLineStripColor(self,pieces):
		self.GUI.setLineStripColor(pieces[1],pieces[2])
		
	def getLineStripPointCount(self,pieces):
		count = self.GUI.getLineStripPointsCount(pieces[1])
		print "Point count = " + str(count)
		
	def addPolygonPoint(self,pieces):
		self.GUI.addPolygonPoint(pieces[1],pieces[2],pieces[3])
		
	def getPolygonPoint(self,pieces):
		loc = self.GUI.getPolygonPoint(pieces[1],pieces[2])
		print "Point at x = " + str(loc[0]) + " y = " + str(loc[1]) + "\n"
		
	def movePolygonPoint(self,pieces):
		self.GUI.movePolygonPoint(pieces[1],pieces[2],pieces[3],pieces[4])		
		
	def getPolygonFillColor(self,pieces):
		color = self.GUI.getPolygonFillColor(pieces[1])
		print "Polygon fill color = " + color
		
	def setPolygonFillColor(self,pieces):
		self.GUI.setPolygonFillColor(pieces[1],pieces[2])
		
	def getPolygonLineColor(self,pieces):
		color = self.GUI.getPolygonLineColor(pieces[1])
		print "Polygon line color = " + color
		
	def setPolygonLineColor(self,pieces):
		self.GUI.setPolygonLineColor(pieces[1],pieces[2])
		
	def getPolygonPointCount(self,pieces):
		count = self.GUI.getPolygonPointsCount(pieces[1])
		print "Point count = " + str(count)
		
	messages = {'new_surface' : (newSurface,0), #No parameters
			'new_cursor' : (newCursor,3), #[1]=SurfaceNo  [2]=x  [3]=y
			'new_window' : (newWindow,6), #[1]=SurfaceNo  [2]=x  [3]=y  [4]=width  [5]=height  [6]=name
			'new_circle' : (newCircle,6), #[1]=WindowNo  [2]=x  [3]=y  [4]=Radius  [5]=LineColor  [6]=FillColor
			'new_line' : (newLine,6), #[1]=WindowNo  [2]=xStart  [3]=yStart  [4]=xEnd  [5]=yEnd  [6]=Color
			'new_line_strip' : (newLineStrip,4), #[1]=WindowNo  [2]=x  [3]=y  [4]=Color
			'new_polygon' : (newPolygon,5), #[1]=WindowNo  [2]=x  [3]=y  [4]=LineColor  [5]=FillColor
			'mouse_l' : (mouseLeftDown,1), #[1]=CursorNo
			'mouse_lu' : (mouseLeftUp,1), #[1]=CursorNo
			'mouse_m' : (mouseMiddleDown,1), #[1]=CursorNo
			'mouse_mu' : (mouseMiddleUp,1), #[1]=CursorNo
			'mouse_r' : (mouseRightDown,1), #[1]=CursorNo
			'mouse_ru' : (mouseRightUp,1), #[1]=CursorNo
			'move_cursor' : (moveCursor,3), #[1]=CursorNo  [2]=xDistance  [3]=yDistance
			'relocate_cursor' : (relocateCursor,4), #[1]=CursorNo  [2]=x  [3]=y  [4]=Surface
			'get_cursor_pos' : (getCursorPosition,1), #[1]=CursorNo
			'move_window' : (moveWindow,3), #[1]=WindowNo  [2]=xDistance  [3]=yDistance
			'relocate_window' : (relocateWindow,4),	#[1]=WindowNo  [2]=x  [3]=y  [4]=Surface
			'set_window_width' : (setWindowWidth,2), #[1]=WindowNo  [2]=Width
			'set_window_height' : (setWindowHeight,2), #[1]=WindowNo  [2]=Height
			'get_window_pos' : (getWindowPosition,1), #[1]=WindowNo
			'get_window_width' : (getWindowWidth,1), #[1]=WindowNo
			'get_window_height' : (getWindowHeight,1), #[1]=WindowNo
			'stretch_window_down' : (stretchWindowDown,2), #[1]=WindowNo  [2]=Distance
			'stretch_window_up' : (stretchWindowUp,2), #[1]=WindowNo  [2]=Distance
			'stretch_window_left' : (stretchWindowLeft,2), #[1]=WindowNo  [2]=Distance
			'stretch_window_right' : (stretchWindowRight,2), #[1]=WindowNo  [2]=Distance
			'set_window_name' : (setWindowName,2), #[1]=WindowNo  [2]=Name
			'get_window_name' : (getWindowName,1), #[1]=WindowNo
			'relocate_circle' : (relocateCircle,4), #[1]=ElementNo  [2]=x  [3]=y  [4]=windowNo
			'get_circle_pos' : (getCirclePosition,1), #[1]=ElementNo
			'get_element_type' : (getElementType,1), #[1]=ElementNo
			'set_circle_line_color' : (setCircleLineColor,2), #[1]=ElementNo  [2]=Color
			'set_circle_fill_color' : (setCircleFillColor,2), #[1]=ElementNo  [2]=Color
			'get_circle_line_color' : (getCircleLineColor,1), #[1]=ElementNo
			'get_circle_fill_color' : (getCircleFillColor,1), #[1]=ElementNo
			'set_circle_radius' : (setCircleRadius,2), #[1]=ElementNo  [2]=Radius
			'get_circle_radius' : (getCircleRadius,1), #[1]=ElementNo
			'get_line_start' : (getLineStart,1), # [1]=ElementNo
			'get_line_end' : (getLineEnd,1), #[1]=ElementNo
			'set_line_start' : (setLineStart,3), #[1]=ElementNo  [2]=x  [3]=y
			'set_line_end' : (setLineEnd,3), #[1]=ElementNo  [2]=x  [3]=y
			'set_line_color' : (setLineColor,2), #[1]=ElementNo  [2]=Color
			'get_line_color' : (getLineColor,1), #[1]=ElementNo
			'add_line_strip_point' : (addLineStripPoint,3), #[1]=ElementNo  [2]=x  [3]=y
			'get_line_strip_point' : (getLineStripPoint,2), #[1]=ElementNo  [2]=PointNo
			'move_line_strip_point' : (moveLineStripPoint,4), #[1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
			'get_line_strip_color' : (getLineStripColor,1), #[1]=ElementNo
			'set_line_strip_color' : (setLineStripColor,2), #[1]=ElementNo  [2]=Color
			'get_line_strip_point_count' : (getLineStripPointCount,1), #[1]=ElementNo
			'add_polygon_point' : (addPolygonPoint,3), #[1]=ElementNo  [2]=x  [3]=y
			'get_polygon_point' : (getPolygonPoint,2), #[1]=ElementNo  [2]=PointNo
			'move_polygon_point' : (movePolygonPoint,4), #[1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
			'get_polygon_fill_color' : (getPolygonFillColor,1), #[1]=ElementNo
			'set_polygon_fill_color' : (setPolygonFillColor,2), #[1]=ElementNo  [2]=Color
			'get_polygon_line_color' : (getPolygonLineColor,1), #[1]=ElementNo
			'set_polygon_line_color' : (setPolygonLineColor,2), #[1]=ElementNo  [2]=Color
			'get_polygon_point_count' : (getPolygonPointCount,1) #[1]=ElementNo
	}
	
	def processMessage(self, msg):
		print 'PROCESSING MESSAGE'
		print 'MESSAGE: ', msg, "\n"
		pieces = msg.split(',')
		try:
			if(len(pieces)-1==self.messages[pieces[0]][1]):
				self.messages[pieces[0]][0](self,pieces)
			else:
				print ('\033[1;31mInvalid number of arguments (' + str(len(pieces)-1) + ' instead of ' + str(self.messages[pieces[0]][1]) + ')\033[1;m')
		except KeyError:
			print ('\033[1;31mInvalid API call\033[1;m')