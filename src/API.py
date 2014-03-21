from GUI import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from threading import Thread

#Basis for PyOpenGL/PyGame code from http://www.jason.gd/str/pokaz/pygame_pyopengl_2d

class Texture():
# simple texture class
# designed for 32 bit png images (with alpha channel)
    def __init__(self, fileName):
        self.texID = 0
        self.LoadTexture(fileName)
    def LoadTexture(self, fileName): 
        try:
            textureSurface = pygame.image.load(fileName)
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            
            self.texID = glGenTextures(1)
            
            glBindTexture(GL_TEXTURE_2D, self.texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                        textureSurface.get_width(), textureSurface.get_height(),
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        except:
            print "can't open the texture: %s" % (fileName)
    def __del__(self):
        glDeleteTextures(self.texID)

class apiMessageParser:
    __slots__ = ['GUI']
    
    winWidth = 1280
    winHeight = 1024
    mouseLock = False
    
    def newSurface(self, pieces):
        surfaceNo = self.GUI.newSurface()
        return {'surfaceNo' : surfaceNo}
        
    def newCursor(self, pieces):
        cursorNo = self.GUI.newCursor(pieces[1], pieces[2], pieces[3])
        return {"cursorNo" : cursorNo}
        
    def newWindow(self, pieces):
        windowNo = self.GUI.newWindow(pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"windowNo" : windowNo}
        
    def newCircle(self, pieces):
        elementNo = self.GUI.newCircle(pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"elementNo" : elementNo}
        
    def newLine(self, pieces):
        elementNo = self.GUI.newLine(pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"elementNo" : elementNo}
        
    def newLineStrip(self, pieces):
        elementNo = self.GUI.newLineStrip(pieces[1], pieces[2], pieces[3], pieces[4])
        return {"elementNo" : elementNo}
        
    def newPolygon(self, pieces):
        elementNo = self.GUI.newPolygon(pieces[1], pieces[2], pieces[3], pieces[4], pieces[5])
        return {"elementNo" : elementNo}
        
    def newText(self, pieces):
        elementNo = self.GUI.newText(pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
        
    def mouseLeftDown(self, pieces):
        loc = self.GUI.leftDown(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def mouseLeftUp(self, pieces):
        loc = self.GUI.leftUp(pieces[1])
        return {"x" : loc[0], "y" : loc[1], "duration" : loc[2]}
        
    def mouseMiddleDown(self, pieces):
        loc = self.GUI.middleDown(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def mouseMiddleUp(self, pieces):
        loc = self.GUI.middleUp(pieces[1])
        return {"x" : loc[0], "y" : loc[1], "duration" : loc[2]}
        
    def mouseRightDown(self, pieces):
        loc = self.GUI.rightDown(pieces[1])
        return {"x" : str(loc[0]), "y" : str(loc[1])}
        
    def mouseRightUp(self, pieces):
        loc = self.GUI.rightUp(pieces[1])
        return {"x" : loc[0], "y" : loc[1], "duration" : loc[2]}
        
    def moveCursor(self, pieces):
        self.GUI.moveCursor(pieces[1], pieces[2], pieces[3])
        return {}
    
    def testMoveCursor(self, pieces):
        loc = self.GUI.testMoveCursor(pieces[1], pieces[2], pieces[3])
        return {'x' : loc[0], 'y' : loc[1]}
        
    def relocateCursor(self, pieces):
        self.GUI.setCursorPos(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def getCursorPosition(self, pieces):
        loc = self.GUI.getCursorPos(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
    
    def rotateCursorClockwise(self,pieces):
        self.GUI.rotateCursorClockwise(pieces[1],pieces[2])
        return {}
        
    def rotateCursorAnticlockwise(self,pieces):
        self.GUI.rotateCursorAnticlockwise(pieces[1],pieces[2])
        return {}
        
    def getCursorRotation(self,pieces):
        rot = self.GUI.getCursorRotation(pieces[1])
        return {"rotation" : rot}
        
    def moveWindow(self, pieces):
        self.GUI.moveWindow(pieces[1], pieces[2], pieces[3])
        return {}
        
    def relocateWindow(self, pieces):
        self.GUI.setWindowPos(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def setWindowWidth(self, pieces):
        self.GUI.setWindowWidth(pieces[1], pieces[2])
        return {}
        
    def setWindowHeight(self, pieces):
        self.GUI.setWindowHeight(pieces[1], pieces[2])
        return {}
        
    def getWindowPosition(self, pieces):
        loc = self.GUI.getWindowPos(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def getWindowWidth(self, pieces):
        width = self.GUI.getWindowWidth(pieces[1])
        return {"width" : width}
        
    def getWindowHeight(self, pieces):
        height = self.GUI.getWindowHeight(pieces[1])
        return {"height" : height}
        
    def stretchWindowDown(self, pieces):
        self.GUI.stretchWindowDown(pieces[1], pieces[2])
        return {}
        
    def stretchWindowUp(self, pieces):
        self.GUI.stretchWindowUp(pieces[1], pieces[2])
        return {}
        
    def stretchWindowLeft(self, pieces):    
        self.GUI.stretchWindowLeft(pieces[1], pieces[2])
        return {}
        
    def stretchWindowRight(self, pieces):
        self.GUI.stretchWindowRight(pieces[1], pieces[2])
        return {}
        
    def setWindowName(self, pieces):
        self.GUI.setWindowName(pieces[1], pieces[2])
        return {}
        
    def getWindowName(self, pieces):
        name = self.GUI.getWindowName(pieces[1])
        return {"name" : name}
        
    def relocateCircle(self, pieces):
        name = self.GUI.setCirclePos(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def getCirclePosition(self, pieces):
        loc = self.GUI.getCirclePos(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def getElementType(self, pieces):
        type = self.GUI.getEleType(pieces[1])
        return {"type" : type}
        
    def setCircleLineColor(self, pieces):
        self.GUI.setCircleLine(pieces[1], pieces[2])
        return {}
        
    def setCircleFillColor(self, pieces):
        self.GUI.setCircleFill(pieces[1], pieces[2])
        return {}
        
    def getCircleLineColor(self, pieces):
        color = self.GUI.getCircleLine(pieces[1])
        return {"color" : color}
        
    def getCircleFillColor(self, pieces):
        color = self.GUI.getCircleFill(pieces[1])
        return {"color" : color}
        
    def getCircleRadius(self, pieces):
        radius = self.GUI.getCircleRad(pieces[1])
        return {"radius" : radius}
        
    def setCircleRadius(self, pieces):
        self.GUI.setCircleRad(pieces[1], pieces[2])
        return {}
        
    def getLineStart(self, pieces):
        loc = self.GUI.getLineStart(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def getLineEnd(self, pieces):
        loc = self.GUI.getLineEnd(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def setLineStart(self, pieces):
        self.GUI.setLineStart(pieces[1], pieces[2], pieces[3])
        return {}
        
    def setLineEnd(self, pieces):
        self.GUI.setLineEnd(pieces[1], pieces[2], pieces[3])
        return {}
        
    def setLineColor(self, pieces):
        self.GUI.setLineColor(pieces[1], pieces[2])
        return {}
        
    def getLineColor(self, pieces):
        color = self.GUI.getLineColor(pieces[1])
        return {"color" : color}
        
    def addLineStripPoint(self, pieces):
        self.GUI.addLineStripPoint(pieces[1], pieces[2], pieces[3])
        return {}
        
    def getLineStripPoint(self, pieces):
        loc = self.GUI.getLineStripPoint(pieces[1], pieces[2])
        return {"x" : loc[0], "y" : loc[1]}
        
    def moveLineStripPoint(self, pieces):
        self.GUI.moveLineStripPoint(pieces[1], pieces[2], pieces[3], pieces[4])    
        return {}    
        
    def getLineStripColor(self, pieces):
        color = self.GUI.getLineStripColor(pieces[1])
        return {"color" : color}
        
    def setLineStripColor(self, pieces):
        self.GUI.setLineStripColor(pieces[1], pieces[2])
        return {}
        
    def getLineStripPointCount(self, pieces):
        count = self.GUI.getLineStripPointsCount(pieces[1])
        return {"count" : count}
        
    def addPolygonPoint(self, pieces):
        self.GUI.addPolygonPoint(pieces[1], pieces[2], pieces[3])
        return {}
        
    def getPolygonPoint(self, pieces):
        loc = self.GUI.getPolygonPoint(pieces[1], pieces[2])
        return {"x" : loc[0], "y" : loc[1]}
        
    def movePolygonPoint(self, pieces):
        self.GUI.movePolygonPoint(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def getPolygonFillColor(self, pieces):
        color = self.GUI.getPolygonFillColor(pieces[1])
        return {"color" : color}
        
    def setPolygonFillColor(self, pieces):
        self.GUI.setPolygonFillColor(pieces[1], pieces[2])
        return {}
        
    def getPolygonLineColor(self, pieces):
        color = self.GUI.getPolygonLineColor(pieces[1])
        return {"color" : color}
        
    def setPolygonLineColor(self, pieces):
        self.GUI.setPolygonLineColor(pieces[1], pieces[2])
        return {}
        
    def getPolygonPointCount(self, pieces):
        count = self.GUI.getPolygonPointsCount(pieces[1])
        return {"count" : count}
        
    def setText(self, pieces):
        self.GUI.setText(pieces[1], pieces[2])
        return {}
        
    def getText(self, pieces):
        text = self.GUI.getText(pieces[1])
        return {}
        
    def setTextPos(self, pieces):
        self.GUI.setTextPos(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def getTextPos(self, pieces):
        loc = self.GUI.getTextPos(pieces[1])
        return {"x" : loc[0], "y" : loc[1]}
        
    def setPointSize(self, pieces):
        self.GUI.setPtSize(pieces[1], pieces[2])
        return {}
        
    def getPointSize(self, pieces):
        size = self.GUI.getPtSize(pieces[1])
        return {"size" : size}
        
    def getTextFont(self, pieces):
        font = self.GUI.getFont(pieces[1])
        return {"font" : font}
        
    def setTextFont(self, pieces):
        self.GUI.setFont(pieces[1], pieces[2])
        return {}
        
    def getTextColor(self, pieces):
        color = self.GUI.getTextColor(pieces[1])
        return {"color" : color}
        
    def setTextColor(self, pieces):
        self.GUI.setTextColor(pieces[1], pieces[2])
        return {}
        
    def showElement(self, pieces):
        self.GUI.showElement(pieces[1])
        return {}
        
    def hideElement(self, pieces):
        self.GUI.hideElement(pieces[1])
        return {}
        
    def checkElementVisibility(self, pieces):
        visible = self.GUI.checkElementVisibility(pieces[1])
        return {"visible" : visible}
        
    messages = {'new_surface' : (newSurface, 0),  # No parameters
            'new_cursor' : (newCursor, 3),  # [1]=SurfaceNo  [2]=x  [3]=y
            'new_window' : (newWindow, 6),  # [1]=SurfaceNo  [2]=x  [3]=y  [4]=width  [5]=height  [6]=name
            'new_circle' : (newCircle, 6),  # [1]=WindowNo  [2]=x  [3]=y  [4]=Radius  [5]=LineColor  [6]=FillColor
            'new_line' : (newLine, 6),  # [1]=WindowNo  [2]=xStart  [3]=yStart  [4]=xEnd  [5]=yEnd  [6]=Color
            'new_line_strip' : (newLineStrip, 4),  # [1]=WindowNo  [2]=x  [3]=y  [4]=Color
            'new_polygon' : (newPolygon, 5),  # [1]=WindowNo  [2]=x  [3]=y  [4]=LineColor  [5]=FillColor
            'new_text' : (newText, 7),  # [1]=WindowNo  [2]=text  [3]=x  [4]=y  [5]=PointSize  [6]=Font  [7]=Color
            'mouse_l' : (mouseLeftDown, 1),  # [1]=CursorNo
            'mouse_lu' : (mouseLeftUp, 1),  # [1]=CursorNo
            'mouse_m' : (mouseMiddleDown, 1),  # [1]=CursorNo
            'mouse_mu' : (mouseMiddleUp, 1),  # [1]=CursorNo
            'mouse_r' : (mouseRightDown, 1),  # [1]=CursorNo
            'mouse_ru' : (mouseRightUp, 1),  # [1]=CursorNo
            'move_cursor' : (moveCursor, 3),  # [1]=CursorNo  [2]=xDistance  [3]=yDistance
            'test_move_cursor' : (testMoveCursor, 3),  # [1]=CursorNo  [2]=xDistance  [3]=yDistance
            'relocate_cursor' : (relocateCursor, 4),  # [1]=CursorNo  [2]=x  [3]=y  [4]=Surface
            'get_cursor_pos' : (getCursorPosition, 1),  # [1]=CursorNo
            'rotate_cursor_clockwise' : (rotateCursorClockwise,2), #[1]=CursorNo [2]=Degrees
            'rotate_cursor_anticlockwise' : (rotateCursorAnticlockwise,2), #[1]=CursorNo [2]=Degrees
            'get_cursor_rotation' : (getCursorRotation,1), #[1]=CursorNo
            'move_window' : (moveWindow, 3),  # [1]=WindowNo  [2]=xDistance  [3]=yDistance
            'relocate_window' : (relocateWindow, 4),  # [1]=WindowNo  [2]=x  [3]=y  [4]=Surface
            'set_window_width' : (setWindowWidth, 2),  # [1]=WindowNo  [2]=Width
            'set_window_height' : (setWindowHeight, 2),  # [1]=WindowNo  [2]=Height
            'get_window_pos' : (getWindowPosition, 1),  # [1]=WindowNo
            'get_window_width' : (getWindowWidth, 1),  # [1]=WindowNo
            'get_window_height' : (getWindowHeight, 1),  # [1]=WindowNo
            'stretch_window_down' : (stretchWindowDown, 2),  # [1]=WindowNo  [2]=Distance
            'stretch_window_up' : (stretchWindowUp, 2),  # [1]=WindowNo  [2]=Distance
            'stretch_window_left' : (stretchWindowLeft, 2),  # [1]=WindowNo  [2]=Distance
            'stretch_window_right' : (stretchWindowRight, 2),  # [1]=WindowNo  [2]=Distance
            'set_window_name' : (setWindowName, 2),  # [1]=WindowNo  [2]=Name
            'get_window_name' : (getWindowName, 1),  # [1]=WindowNo
            'relocate_circle' : (relocateCircle, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=windowNo
            'get_circle_pos' : (getCirclePosition, 1),  # [1]=ElementNo
            'get_element_type' : (getElementType, 1),  # [1]=ElementNo
            'set_circle_line_color' : (setCircleLineColor, 2),  # [1]=ElementNo  [2]=Color
            'set_circle_fill_color' : (setCircleFillColor, 2),  # [1]=ElementNo  [2]=Color
            'get_circle_line_color' : (getCircleLineColor, 1),  # [1]=ElementNo
            'get_circle_fill_color' : (getCircleFillColor, 1),  # [1]=ElementNo
            'set_circle_radius' : (setCircleRadius, 2),  # [1]=ElementNo  [2]=Radius
            'get_circle_radius' : (getCircleRadius, 1),  # [1]=ElementNo
            'get_line_start' : (getLineStart, 1),  # [1]=ElementNo
            'get_line_end' : (getLineEnd, 1),  # [1]=ElementNo
            'relocate_line_start' : (setLineStart, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'relocate_line_end' : (setLineEnd, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'set_line_color' : (setLineColor, 2),  # [1]=ElementNo  [2]=Color
            'get_line_color' : (getLineColor, 1),  # [1]=ElementNo
            'add_line_strip_point' : (addLineStripPoint, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'get_line_strip_point' : (getLineStripPoint, 2),  # [1]=ElementNo  [2]=PointNo
            'relocate_line_strip_point' : (moveLineStripPoint, 4),  # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
            'get_line_strip_color' : (getLineStripColor, 1),  # [1]=ElementNo
            'set_line_strip_color' : (setLineStripColor, 2),  # [1]=ElementNo  [2]=Color
            'get_line_strip_point_count' : (getLineStripPointCount, 1),  # [1]=ElementNo
            'add_polygon_point' : (addPolygonPoint, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'get_polygon_point' : (getPolygonPoint, 2),  # [1]=ElementNo  [2]=PointNo
            'relocate_polygon_point' : (movePolygonPoint, 4),  # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
            'get_polygon_fill_color' : (getPolygonFillColor, 1),  # [1]=ElementNo
            'set_polygon_fill_color' : (setPolygonFillColor, 2),  # [1]=ElementNo  [2]=Color
            'get_polygon_line_color' : (getPolygonLineColor, 1),  # [1]=ElementNo
            'set_polygon_line_color' : (setPolygonLineColor, 2),  # [1]=ElementNo  [2]=Color
            'get_polygon_point_count' : (getPolygonPointCount, 1),  # [1]=ElementNo
            'set_text' : (setText, 2),  # [1]=ElementNo  [2]=String
            'get_text' : (getText, 1),  # [1]=ElementNo
            'relocate_text' : (setTextPos, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=WindowNo
            'get_text_pos' : (getTextPos, 1),  # [1]=ElementNo
            'set_text_point_size' : (setPointSize, 2),  # [1]=ElementNo  [2]=PointSize
            'get_text_point_size' : (getPointSize, 1),  # [1]=ElementNo
            'get_text_font' : (getTextFont, 1),  # [1]=ElementNo
            'set_text_font' : (setTextFont, 2),  # [1]=ElementNo  [2]=Font
            'set_text_color' : (setTextColor, 2),  # [1]=ElementNo  [2]=Color
            'get_text_color' : (getTextColor, 1),  # [1]=ElementNo
            'show_element' : (showElement, 1),  # [1]=ElementNo
            'hide_element' : (hideElement, 1),  # [1]=ElementNo
            'check_element_visibility' : (checkElementVisibility, 1)  # [1]=ElementNo
    }
    
    def processMessage(self, msg):
        pieces = msg.split(',')
        data = ""
        try:
            if(len(pieces) - 1 == self.messages[pieces[0]][1]):
                data = self.messages[pieces[0]][0](self, pieces)
            else:
                data = {"error" : 2, "1" : str(len(pieces) - 1), "2" : str(self.messages[pieces[0]][1])}
        except KeyError:
            data = {"error" : 1}
        return data
    
    def getInput(self):
        mpb=pygame.mouse.get_pressed() # mouse pressed buttons
        kpb=pygame.key.get_pressed() # keyboard pressed buttons
        pos=pygame.mouse.get_pos() # mouse shift
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_l:
                    if (self.mouseLock == True):
                        self.mouseLock = False
                        pygame.mouse.set_visible(True)
                    elif(self.mouseLock == False):
                        self.mouseLock = True
                        pygame.mouse.set_visible(False)
            if(self.mouseLock==True):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==4:
                        self.GUI.rotateCursorClockwise(1,10)
                    elif event.button==5:
                        self.GUI.rotateCursorAnticlockwise(1,10)
                xdist = (1280/2)-pos[0]
                ydist = (1024/2)-pos[1]
                pygame.mouse.set_pos([self.winWidth/2,self.winHeight/2])
                
                self.GUI.moveCursor(1,-xdist,ydist)
                virtualpos = self.GUI.getCursorPos(1)
                if (virtualpos[0]<0):
                    self.GUI.setCursorX(1,0)
                elif(virtualpos[0]>self.winWidth):
                    self.GUI.setCursorX(1,self.winWidth)
                if(virtualpos[1]<0):
                    self.GUI.setCursorY(1,0)
                elif(virtualpos[1]>self.winHeight):
                    self.GUI.setCursorY(1,self.winHeight)
    
    def checkSetupGUI(self):
        self.getInput()
        GUIRead = self.GUI
        cursors = GUIRead.getCursors(0)
        position = GUIRead.getCursorPos(cursors[0])
        self.x = position[0]
        self.y = position[1]
        self.rotation = GUIRead.getCursorRotation(cursors[0])
		
    def resize(self, (width, height)):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winWidth, 0, self.winHeight)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def init(self):
        # set some basic OpenGL settings and control variables
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_BLEND)
		
        self.mouse_texture = Texture("cursor.png")
        self.cross_texture = Texture("cursorcross.png")
		
        self.demandedFps = 30.0
        self.done = False
		
        self.x, self.y = 0.0 , 0.0
        self.rotation = 0
		
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
        glPushMatrix()
		
        glTranslatef(self.x, self.y, 0.0)
        glRotatef(-self.rotation,0.0,0.0,1.0)

        glColor4f(1.0, 1.0, 1.0, 1.0)
		
        glBindTexture(GL_TEXTURE_2D, self.mouse_texture.texID)

        glBegin(GL_QUADS)
		
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, 0)
		
        glTexCoord2f(1.0, 1.0)
        glVertex2f(29, 0)
		
        glTexCoord2f(1.0, 0.0)
        glVertex2f(29, -46)
		
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, -46)
		
        glEnd()
        
        glBindTexture(GL_TEXTURE_2D, self.cross_texture.texID)

        glBegin(GL_QUADS)
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(-20, 20)
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f(20, 20)
        
        glTexCoord2f(1.0, 0.0)
        glVertex2f(20, -20)
        
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-20, -20)
        
        glEnd()
		
        glPopMatrix()
		
    def display(self):
        video_flags = OPENGL | DOUBLEBUF
		
        pygame.init()
        pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.set_mode((self.winWidth, self.winHeight), video_flags)
		
        pygame.display.set_caption("Display")
		
        self.resize((self.winWidth, self.winHeight))
        self.init()

		
        clock = pygame.time.Clock()
        while 1:
            event = pygame.event.poll()
            if event.type == QUIT or self.done:
                pygame.quit () 
                break
			
            self.checkSetupGUI()
            self.draw()
			
            pygame.display.flip()
			
			# limit fps
            clock.tick(self.demandedFps)
	
    def __init__(self):
        self.GUI = GUI()
        thread = Thread(target=self.display, args=())
        thread.start()
			
# TODO
# Check if locking is needed (I don't think API calls can be processed in parallel anyway)
