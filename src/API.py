from GUI import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from threading import Thread
from math import *
from straightcoons import coonsCalc
import FTGL
import time
import numpy
import glob
import os
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from buffers import *

from ctypes import *

#Texture loading class from http://www.jason.gd/str/pokaz/pygame_pyopengl_2d
class Texture():
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

#A class which is used to parse API messages and call the relevant actions
class apiMessageParser:
    __slots__ = ['GUI','meshBuffer','renderOrder', 'elementBuffer', 'winWidth', 'winHeight']
    
    mouseLock = False
    elementBuffer = {}
    textureBuffer = {}
    looping = True
    
    fonts = {"Times New Roman" : "FreeSerif",
         "Free Serif" : "FreeSerif",
         "Arial" : "arial",
         "Free Mono" : "FreeMono",
         "Courier New": "FreeMono",
         "Arial" : "FreeSans",
         "Free Sans" : "FreeSans"
         }
    
    #Creates a new surface for projection as requested by the API call
    def newSurface(self, pieces):
        surfaceNo = self.GUI.newSurface(pieces[1], pieces[2], pieces[3])
        return {'surfaceNo' : surfaceNo}
    
    #Creates a new surface for projection with an ID as requested by the API Call
    def newSurfaceWithID(self, peices):
        surfaceNo = self.GUI.newSurfaceWithID(pieces[2], pieces[3], pieces[4], pieces[1])
        return {'surfaceNo' : surfaceNo}
        
    #Creates a new cursor on the desired surface as requested by the API call
    def newCursor(self, pieces):
        cursorNo = self.GUI.newCursor(pieces[1], pieces[2], pieces[3])
        return {"cursorNo" : cursorNo}
    
    #Creates a new cursor with an ID on the desired surface as requested by the API call
    def newCursorWithID(self, pieces):
        cursorNo = self.GUI.newCursorWithID(pieces[1], pieces[2], pieces[3], pieces[4])
        return {"cursorNo" : cursorNo}
        
    #Creates a new window on the desired surface as requested by the API call
    def newWindow(self, pieces):
        windowNo = self.GUI.newWindow(pieces[7], pieces[8], pieces[9], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"windowNo" : windowNo}
    
    #Creates a new window with an ID on the desired surface as requested by the API call
    def newWindowWithID(self, pieces):
        windowNo = self.GUI.newWindowWithID(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"windowNo" : windowNo}
        
    #Creates a new circle on the desired window as requested by the API call
    def newCircle(self, pieces):
        elementNo = self.GUI.newCircle(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
    
    #Creates a new circle with an ID on the desired window as requested by the API call
    def newCircleWithID(self, pieces):
        print str(pieces)
        print "sending = " + pieces[8] + "," + pieces[9] + "," + pieces[10] + "," + pieces[1] + "," + pieces[2] + "," + pieces[3] + "," + pieces[4] + "," + pieces[5] + "," + pieces[6] + "," + pieces[7] + "," + pieces[8]
        elementNo = self.GUI.newCircleWithID(pieces[9], pieces[10], pieces[11], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])
        return {"elementNo" : elementNo}
        
    #Creates a new line on the desired window as requested by the API call
    def newLine(self, pieces):
        elementNo = self.GUI.newLine(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
    
    #Creates a new line with an ID in the desired window as requested by the API call
    def newLineWithID(self, pieces):
        elementNo = self.GUI.newLineWithID(pieces[9], pieces[10], pieces[11], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])
        return {"elementNo" : elementNo}
        
    #Creates the starting point of a new line strip on the desired window as requested by the API call
    def newLineStrip(self, pieces):
        elementNo = self.GUI.newLineStrip(pieces[6], pieces[7], pieces[8], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5])
        return {"elementNo" : elementNo}
    
    #Creates the starting point of a new line strip with an ID on the desired window as requested by the API call
    def newLineStripWithID(self, pieces):
        elementNo = self.GUI.newLineStripWithID(pieces[7], pieces[8], pieces[9], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"elementNo" : elementNo}
        
    #Creates the starting point of a new polygon on the desired window as requested by the API call
    def newPolygon(self, pieces):
        elementNo = self.GUI.newPolygon(pieces[6], pieces[7], pieces[8], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5])
        return {"elementNo" : elementNo}
    
    #Creates the starting point of a new polygon with an ID on the desired window as requested by the API call
    def newPolygonWithID(self, pieces):
        elementNo = self.GUI.newPolygonWithID(pieces[7], pieces[8], pieces[9], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"elementNo" : elementNo}
    
    #Creates a new rectangle on the desired window as requested by the API call
    def newRectangle(self,pieces):
        elementNo = self.GUI.newRectangle(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
    
    #Creates a new rectangle with an ID on the desired window as requested by the API call
    def newRectangleWithID(self,pieces):
        elementNo = self.GUI.newRectangleWithID(pieces[9], pieces[10], pieces[11], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])
        return {"elementNo" : elementNo}
    
    #Creates a new textured rectangle on the desired window as requested by the API call
    def newTexRectangle(self,pieces):
        elementNo = self.GUI.newTexRectangle(pieces[7], pieces[8], pieces[9], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6])
        return {"elementNo" : elementNo}
    
    #Creates a new textured rectangle with an ID on the desired window as requested by the API call
    def newTexRectangleWithID(self,pieces):
        elementNo = self.GUI.newTexRectangleWithID(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
            
    #Creates a new block of text on the desired window as requested by the API call
    def newText(self, pieces):
        elementNo = self.GUI.newText(pieces[8], pieces[9], pieces[10], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7])
        return {"elementNo" : elementNo}
    
    #Creates a new block of text with an ID on the desired window as requested by the API call
    def newTextWithID(self, pieces):
        elementNo = self.GUI.newTextWithID(pieces[9], pieces[10], pieces[11], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])
        return {"elementNo" : elementNo}
    
    #Subscribes the current user to a surface
    def subscribeToSurface(self, pieces):
        self.GUI.subscribeToSurface(pieces[3] + "," + pieces[4], pieces[1])
        return {}
    
    #Gets the ID of a surface
    def getSurfaceID(self, pieces):
        ID = self.GUI.getSurfaceID(pieces[1])
        return {"ID" : ID}
    
    #Sets the ID of a surface
    def setSurfaceID(self, pieces):
        self.GUI.setSurfaceID(pieces[1],pieces[2])
        return {}
    
    #Gets the owner of a surface
    def getSurfaceOwner(self, pieces):
        owner = self.GUI.getSurfaceOwner(pieces[1])
        return {"owner" : owner}
    
    #Gets the details of the creator application of a surface
    def getSurfaceAppDetails(self, pieces):
        app = self.GUI.getSurfaceAppDetails(pieces[1])
        return {"app" : app[0], "instance" : app[1]}
    
    #Returns all surfaces with the desired ID
    def getSurfacesByID(self, pieces):
        found = self.GUI.getSurfacesByID(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    #Returns all surfaces with the desired owner
    def getSurfacesByOwner(self, pieces):
        found = self.GUI.getSurfacesByOwner(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    #Returns all surfaces with the desired app name
    def getSurfacesByAppName(self, pieces):
        found = self.GUI.getSurfacesByAppName(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    #Returns all surfaces with the desired application details
    def getSurfacesByAppDetails(self, pieces):
        found = self.GUI.getSurfacesByAppDetails(pieces[1], pieces[2])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    #Registers the application as the admin for the surface
    def becomeSurfaceAdmin(self, pieces):
        test = self.GUI.becomeSurfaceAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
        
    #Deregisters the current user as admin for the surface
    def stopBeingSurfaceAdmin(self, pieces):
        test = self.GUI.stopBeingSurfaceAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
        
    #Sets the edge points for a surface
    def setSurfaceEdges(self, pieces):
        self.GUI.setSurfacePoints(pieces[1],pieces[2],pieces[3],pieces[4],pieces[5])
        return {}
        
    #Removes all the known edge points from a surface so it is no longer shown.
    def undefineSurface(self, pieces):
        self.GUI.undefineSurface(pieces[1])
        return {}
    
    def saveDefinedSurfaces(self, pieces):
        self.GUI.saveDefinedSurfaces(pieces[1])
        return {}
    
    def loadDefinedSurfaces(self, pieces):
        count = self.GUI.loadDefinedSurfaces(pieces[1])
        return {"count" : count[0], "layouts" : count[1]}
    
    def getSavedLayouts(self, pieces):
        layouts = glob.glob('*.lyt')
        dict = {}
        dict["count"] = len(layouts)
        for x in range(0,len(layouts)):
            dict[x] = layouts[x].split(".")[0]
        return dict
    
    def deleteLayout(self, pieces):
        os.remove(pieces[1] + ".lyt")
    
    def rotateSurfaceTo0(self, pieces):
        self.GUI.rotateSurfaceTo0(pieces[1])
        return {}
    
    def rotateSurfaceTo90(self, pieces):
        self.GUI.rotateSurfaceTo90(pieces[1])
        return {}
    
    def rotateSurfaceTo180(self, pieces):
        self.GUI.rotateSurfaceTo180(pieces[1])
        return {}
    
    def rotateSurfaceTo270(self, pieces):
        self.GUI.rotateSurfaceTo270(pieces[1])
        return {}
    
    def mirrorSurface(self, pieces):
        self.GUI.mirrorSurface(pieces[1])
        return {}
    
    def connectSurfaces(self, pieces):
        self.GUI.connectSurfaces(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def disconnectSurfaces(self, pieces):
        self.GUI.disconnectSurfaces(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}

    def subscribeToWindow(self, pieces):
        self.GUI.subscribeToWindow(pieces[3] + "," + pieces[4], pieces[1])
        return {}
    
    def getWindowID(self, pieces):
        ID = self.GUI.getWindowID(pieces[1])
        return {"ID" : ID}
    
    def setWindowID(self, pieces):
        self.GUI.setWindowID(pieces[1],pieces[2])
        return {}
    
    def getWindowOwner(self, pieces):
        owner = self.GUI.getWindowOwner(pieces[1])
        return {"owner" : owner}
    
    def getWindowAppDetails(self, pieces):
        app = self.GUI.getWindowAppDetails(pieces[1])
        return {"app" : app[0], "instance" : app[1]}
    
    def getWindowsByID(self, pieces):
        found = self.GUI.getWindowsByID(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getWindowsByOwner(self, pieces):
        found = self.GUI.getWindowsByOwner(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getWindowsByAppName(self, pieces):
        found = self.GUI.getWindowsByAppName(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getWindowsByAppDetails(self, pieces):
        found = self.GUI.getWindowsByAppDetails(pieces[1], pieces[2])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def becomeWindowAdmin(self, pieces):
        test = self.GUI.becomeWindowAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
        
    def stopBeingWindowAdmin(self, pieces):
        test = self.GUI.stopBeingWindowAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
    
    def subscribeToElement(self, pieces):
        self.GUI.subscribeToElement(pieces[3] + "," + pieces[4], pieces[1])
        return {}
    
    def getElementID(self, pieces):
        ID = self.GUI.getElementID(pieces[1])
        return {"ID" : ID}
    
    def setElementID(self, pieces):
        self.GUI.setElementID(pieces[1],pieces[2])
        return {}
    
    def getElementOwner(self, pieces):
        owner = self.GUI.getElementOwner(pieces[1])
        return {"owner" : owner}
    
    def getElementAppDetails(self, pieces):
        app = self.GUI.getElementAppDetails(pieces[1])
        return {"app" : app[0], "instance" : app[1]}
    
    def getElementsByID(self, pieces):
        found = self.GUI.getElementsByID(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getElementsByOwner(self, pieces):
        found = self.GUI.getElementsByOwner(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getElementsByAppName(self, pieces):
        found = self.GUI.getElementsByAppName(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getElementsByAppDetails(self, pieces):
        found = self.GUI.getElementsByAppDetails(pieces[1], pieces[2])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def getElementsOnWindow(self, pieces):
        found = self.GUI.getElements(pieces[1])
        dict = {}
        dict["count"] = len(found)
        for x in range(0,len(found)):
            dict[x] = found[x]
        return dict
    
    def becomeElementAdmin(self, pieces):
        test = self.GUI.becomeElementAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
        
    def stopBeingElementAdmin(self, pieces):
        test = self.GUI.stopBeingElementAdmin(pieces[1], pieces[3], pieces[4])
        if(test==True):
            return {}
        else:
            return {"error" : 7}
        
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
        name = self.GUI.setCirclePos(pieces[1], pieces[2], pieces[3])
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
    
    def getCircleSides(self, pieces):
        sides = self.GUI.getCircleSides(pieces[1])
        return {"sides" : sides}
    
    def setCircleSides(self, pieces):
        self.GUI.setCircleSides(pieces[1], pieces[2])
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
    
    def getLineWidth(self, pieces):
        width = self.GUI.getLineWidth(pieces[1])
        return {"width" : width}
    
    def setLineWidth(self, pieces):
        self.GUI.setLineWidth(pieces[1], pieces[2])
        
    def addLineStripPoint(self, pieces):
        self.GUI.addLineStripPoint(pieces[1], pieces[2], pieces[3])
        return {}
    
    def addLineStripPointAt(self, pieces):
        self.GUI.addLineStripPointAt(pieces[1], pieces[2], pieces[3], pieces[4])
        return {}
        
    def getLineStripPoint(self, pieces):
        loc = self.GUI.getLineStripPoint(pieces[1], pieces[2])
        return {"x" : loc[0], "y" : loc[1]}
        
    def moveLineStripPoint(self, pieces):
        self.GUI.moveLineStripPoint(int(pieces[1]), int(pieces[2]), float(pieces[3]), float(pieces[4]))    
        return {}    
        
    def getLineStripColor(self, pieces):
        color = self.GUI.getLineStripColor(pieces[1])
        return {"color" : color}
        
    def setLineStripColor(self, pieces):
        self.GUI.setLineStripColor(pieces[1], pieces[2])
        return {}
    
    def getLineStripWidth(self, pieces):
        width = self.GUI.getLineStripWidth(pieces[1])
        return {"width" : width}
    
    def setLineStripWidth(self, pieces):
        self.GUI.setLineStripWidth(pieces[1], pieces[2])
        
    def getLineStripPointCount(self, pieces):
        count = self.GUI.getLineStripPointsCount(pieces[1])
        return {"count" : count}
    
    def setLineStripContent(self, pieces):
        self.GUI.setLineStripContent(pieces[1], pieces[2])
        return {}
        
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
    
    def setRectangleTopLeft(self, pieces):
        count = self.GUI.setRectangleTopLeft(pieces[1], pieces[2], pieces[3])
        return {}
    
    def getRectangleTopLeft(self, pieces):
        loc = self.GUI.getRectangleTopLeft(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getRectangleTopRight(self, pieces):
        loc = self.GUI.getRectangleTopRight(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getRectangleBottomRight(self, pieces):
        loc = self.GUI.getRectangleBottomRight(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getRectangleBottomLeft(self, pieces):
        loc = self.GUI.getRectangleBottomLeft(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def setRectangleWidth(self, pieces):
        self.GUI.setRectangleWidth(pieces[1], pieces[2])
        return {}
        
    def getRectangleWidth(self, pieces):
        width = self.GUI.getRectangleWidth(pieces[1])
        return {'width' : width}
    
    def setRectangleHeight(self, pieces):
        self.GUI.setRectangleHeight(pieces[1], pieces[2])
        return {}
        
    def getRectangleHeight(self, pieces):
        width = self.GUI.getRectangleHeight(pieces[1])
        return {'width' : width}

    def getRectangleFillColor(self, pieces):
        color = self.GUI.getRectangleFillColor(pieces[1])
        return {'color' : color}
    
    def setRectangleFillColor(self, pieces):
        self.GUI.setRectangleFillColor(pieces[1], pieces[2])
        return {}
    
    def getRectangleLineColor(self, pieces):
        color = self.GUI.getRectangleLineColor(pieces[1])
        return {'color' : color}
    
    def setRectangleLineColor(self, pieces):
        self.GUI.setRectangleLineColor(pieces[1], pieces[2])
        return {}
    
    def setTexRectangleTopLeft(self, pieces):
        count = self.GUI.setTexRectangleTopLeft(pieces[1], pieces[2], pieces[3])
        return {}
    
    def getTexRectangleTopLeft(self, pieces):
        loc = self.GUI.getTexRectangleTopLeft(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getTexRectangleTopRight(self, pieces):
        loc = self.GUI.getTexRectangleTopRight(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getTexRectangleBottomRight(self, pieces):
        loc = self.GUI.getTexRectangleBottomRight(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def getTexRectangleBottomLeft(self, pieces):
        loc = self.GUI.getTexRectangleBottomLeft(pieces[1])
        return {'x' : loc[0], 'y' : loc[1]}
    
    def setTexRectangleTexture(self, pieces):
        self.GUI.setTexRectangleTexture(pieces[1],pieces[2])
    
    def getTexRectangleTexture(self, pieces):
        tex = self.GUI.getTexRectangleTexture(pieces[1])
        return {'texture' : tex}
    
    def setTexRectangleWidth(self, pieces):
        self.GUI.setTexRectangleWidth(pieces[1], pieces[2])
        return {}
        
    def getTexRectangleWidth(self, pieces):
        width = self.GUI.getTexRectangleWidth(pieces[1])
        return {'width' : width}
    
    def setTexRectangleHeight(self, pieces):
        self.GUI.setTexRectangleHeight(pieces[1], pieces[2])
        return {}
        
    def getTexRectangleHeight(self, pieces):
        width = self.GUI.getTexRectangleHeight(pieces[1])
        return {'width' : width}

    def setText(self, pieces):
        self.GUI.setText(pieces[1], pieces[2])
        return {}
        
    def getText(self, pieces):
        text = self.GUI.getText(pieces[1])
        return {'text' : text}
        
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
    
    def hideSetupSurface(self,pieces):
        self.GUI.hideSetupSurface()
        return {}
        
    def showSetupSurface(self,pieces):
        self.GUI.showSetupSurface()
        return {}
        
    def getSetupSurfaceVisibility(self,pieces):
        visible = self.GUI.getSetupSurfaceVisibilty()
        return {"visible" : visible}
    
    def getClickedElements(self,pieces):
        elements = self.GUI.getClickedElements(pieces[1],pieces[2],pieces[3])
        dict = {}
        dict["count"] = len(elements)
        for x in range(0,len(elements)):
            dict[str(x)]=elements[x]
        return dict
    
    def removeElement(self, pieces):
        self.GUI.removeElement(pieces[1], pieces[2])
        return {}
    
    #A dict used so that the program can check which function to call for each API command, and to tell the program how many arguments should be expected
    messages = {'new_surface' : (newSurface, 0),  # No parameters
            'new_surface_with_ID' : (newSurfaceWithID, 1),
            'new_cursor' : (newCursor, 3),  # [1]=SurfaceNo  [2]=x  [3]=y
            'new_cursor_with_ID' : (newCursorWithID, 4), # [1]=ID [2]=SurfaceNo  [3]=x  [4]=y
            'new_window' : (newWindow, 6),  # [1]=SurfaceNo  [2]=x  [3]=y  [4]=width  [5]=height  [6]=name
            'new_window_with_ID' : (newWindowWithID, 7),
            'new_circle' : (newCircle, 7),  # [1]=WindowNo  [2]=x  [3]=y  [4]=Radius  [5]=LineColor  [6]=FillColor
            'new_circle_with_ID' : (newCircleWithID, 8),
            'new_line' : (newLine, 7),  # [1]=WindowNo  [2]=xStart  [3]=yStart  [4]=xEnd  [5]=yEnd  [6]=Color
            'new_line_with_ID' : (newLineWithID, 8),
            'new_line_strip' : (newLineStrip, 5),  # [1]=WindowNo  [2]=x  [3]=y  [4]=Color
            'new_line_strip_with_ID' : (newLineStripWithID, 6),
            'new_polygon' : (newPolygon, 5),  # [1]=WindowNo  [2]=x  [3]=y  [4]=LineColor  [5]=FillColor
            'new_polygon_with_ID' : (newPolygonWithID, 6),
            'new_rectangle' : (newRectangle,7),
            'new_rectangle_with_ID' : (newRectangleWithID, 8),
            'new_texrectangle' : (newTexRectangle,6),
            'new_texrectangle_with_ID' : (newTexRectangleWithID, 7),
            'new_text' : (newText, 7),  # [1]=WindowNo  [2]=text  [3]=x  [4]=y  [5]=PointSize  [6]=Font  [7]=Color
            'new_text_with_ID' : (newTextWithID, 8),
            'subscribe_to_surface' : (subscribeToSurface, 1),
            'get_surface_ID' : (getSurfaceID, 1),
            'set_surface_ID' : (setSurfaceID, 2),
            'get_surface_owner' : (getSurfaceOwner, 1),
            'get_surface_app_details' : (getSurfaceAppDetails, 1),
            'get_surfaces_by_ID' : (getSurfacesByID, 1),
            'get_surfaces_by_owner' : (getSurfacesByOwner, 1),
            'get_surfaces_by_app_name' : (getSurfacesByAppName, 1),
            'get_surfaces_by_app_details' : (getSurfacesByAppDetails, 2),
            'become_surface_admin' : (becomeSurfaceAdmin, 1),
            'stop_being_surface_admin' : (stopBeingSurfaceAdmin, 1),
            'set_surface_edges' : (setSurfaceEdges, 5),
            'undefine_surface' : (undefineSurface, 1),
            'save_defined_surfaces' : (saveDefinedSurfaces, 1),
            'load_defined_surfaces' : (loadDefinedSurfaces, 1),
            'get_saved_layouts' : (getSavedLayouts, 0),
            'delete_layout' : (deleteLayout, 1),
            'rotate_surface_to_0' : (rotateSurfaceTo0, 1),
            'rotate_surface_to_90' : (rotateSurfaceTo90, 1),
            'rotate_surface_to_180' : (rotateSurfaceTo180, 1),
            'rotate_surface_to_270' : (rotateSurfaceTo270, 1),
            'mirror_surface' : (mirrorSurface, 1),
            'connect_surfaces' : (connectSurfaces, 4),
            'disconnect_surfaces' : (disconnectSurfaces, 4),
            'subscribe_to_window' : (subscribeToWindow, 1),
            'get_window_ID' : (getWindowID, 1),
            'set_window_ID' : (setWindowID, 2),
            'get_window_owner' : (getWindowOwner, 1),
            'get_window_app_details' : (getWindowAppDetails, 1),
            'get_windows_by_ID' : (getWindowsByID, 1),
            'get_windows_by_owner' : (getWindowsByOwner, 1),
            'get_windows_by_app_name' : (getWindowsByAppName, 1),
            'get_windows_by_app_details' : (getWindowsByAppDetails, 2),
            'become_window_admin' : (becomeWindowAdmin, 1),
            'stop_being_window_admin' : (stopBeingWindowAdmin, 1),
            'subscribe_to_element' : (subscribeToElement, 1),
            'get_element_ID' : (getElementID, 1),
            'set_element_ID' : (setElementID, 2),
            'get_element_owner' : (getElementOwner, 1),
            'get_element_app_details' : (getElementAppDetails, 1),
            'get_elements_by_ID' : (getElementsByID, 1),
            'get_elements_by_owner' : (getElementsByOwner, 1),
            'get_elements_by_app_name' : (getElementsByAppName, 1),
            'get_elements_by_app_details' : (getElementsByAppDetails, 2),
            'get_elements_on_window' : (getElementsOnWindow, 1),
            'become_element_admin' : (becomeElementAdmin, 1),
            'stop_being_element_admin' : (stopBeingElementAdmin, 1),
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
            'relocate_circle' : (relocateCircle, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'get_circle_pos' : (getCirclePosition, 1),  # [1]=ElementNo
            'get_element_type' : (getElementType, 1),  # [1]=ElementNo
            'set_circle_line_color' : (setCircleLineColor, 2),  # [1]=ElementNo  [2]=Color
            'set_circle_fill_color' : (setCircleFillColor, 2),  # [1]=ElementNo  [2]=Color
            'get_circle_line_color' : (getCircleLineColor, 1),  # [1]=ElementNo
            'get_circle_fill_color' : (getCircleFillColor, 1),  # [1]=ElementNo
            'set_circle_radius' : (setCircleRadius, 2),  # [1]=ElementNo  [2]=Radius
            'get_circle_radius' : (getCircleRadius, 1),  # [1]=ElementNo
            'set_circle_sides' : (setCircleSides, 2),
            'get_circle_sides' : (getCircleSides, 1),
            'get_line_start' : (getLineStart, 1),  # [1]=ElementNo
            'get_line_end' : (getLineEnd, 1),  # [1]=ElementNo
            'relocate_line_start' : (setLineStart, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'relocate_line_end' : (setLineEnd, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'set_line_color' : (setLineColor, 2),  # [1]=ElementNo  [2]=Color
            'get_line_color' : (getLineColor, 1),  # [1]=ElementNo
            'set_line_width' : (setLineWidth, 2),
            'get_line_width' : (getLineWidth, 1),
            'add_line_strip_point' : (addLineStripPoint, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'add_line_strip_point_at' : (addLineStripPointAt, 4), # [1]=ElementNo [2]=x [3]=y [4]=index
            'get_line_strip_point' : (getLineStripPoint, 2),  # [1]=ElementNo  [2]=PointNo
            'relocate_line_strip_point' : (moveLineStripPoint, 4),  # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
            'get_line_strip_color' : (getLineStripColor, 1),  # [1]=ElementNo
            'set_line_strip_color' : (setLineStripColor, 2),  # [1]=ElementNo  [2]=Color
            'get_line_strip_width' : (getLineStripWidth, 1),
            'set_line_strip_width' : (getLineStripWidth, 2),
            'get_line_strip_point_count' : (getLineStripPointCount, 1),  # [1]=ElementNo
            'set_line_strip_content' : (setLineStripContent, 2),
            'add_polygon_point' : (addPolygonPoint, 3),  # [1]=ElementNo  [2]=x  [3]=y
            'get_polygon_point' : (getPolygonPoint, 2),  # [1]=ElementNo  [2]=PointNo
            'relocate_polygon_point' : (movePolygonPoint, 4),  # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y
            'get_polygon_fill_color' : (getPolygonFillColor, 1),  # [1]=ElementNo
            'set_polygon_fill_color' : (setPolygonFillColor, 2),  # [1]=ElementNo  [2]=Color
            'get_polygon_line_color' : (getPolygonLineColor, 1),  # [1]=ElementNo
            'set_polygon_line_color' : (setPolygonLineColor, 2),  # [1]=ElementNo  [2]=Color
            'get_polygon_point_count' : (getPolygonPointCount, 1),  # [1]=ElementNo
            'set_rectangle_top_left' : (setRectangleTopLeft, 3),
            'get_rectangle_top_left' : (getRectangleTopLeft,1),
            'get_rectangle_top_right' : (getRectangleTopRight,1),
            'get_rectangle_bottom_right' : (getRectangleBottomRight,1),
            'get_rectangle_bottom_left' : (getRectangleBottomLeft,1),
            'set_rectangle_width' : (setRectangleWidth,2),
            'get_rectangle_width' : (getRectangleWidth,1),
            'set_rectangle_height' : (setRectangleHeight,2),
            'get_rectangle_height' : (getRectangleHeight,1),
            'get_rectangle_fill_color' : (getRectangleFillColor,1),
            'set_rectangle_fill_color' : (setRectangleFillColor,2),
            'get_rectangle_line_color' : (getRectangleLineColor,1),
            'set_rectangle_line_color' : (setRectangleLineColor,2),
            'set_texrectangle_top_left' : (setTexRectangleTopLeft, 3),
            'get_texrectangle_top_left' : (getTexRectangleTopLeft,1),
            'get_texrectangle_top_right' : (getTexRectangleTopRight,1),
            'get_texrectangle_bottom_right' : (getTexRectangleBottomRight,1),
            'get_texrectangle_bottom_left' : (getTexRectangleBottomLeft,1),
            'set_texrectangle_texture' : (setTexRectangleTexture,2),
            'get_texrectangle_texture' : (getTexRectangleTexture,1),
            'set_texrectangle_width' : (setTexRectangleWidth,2),
            'get_texrectangle_width' : (getTexRectangleWidth,1),
            'set_texrectangle_height' : (setTexRectangleHeight,2),
            'get_texrectangle_height' : (getTexRectangleHeight,1),
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
            'check_element_visibility' : (checkElementVisibility, 1),  # [1]=ElementNo
            'hide_setup_surface' : (hideSetupSurface,0),
            'show_setup_surface' : (showSetupSurface,0),
            'get_setup_surface_visibility' : (getSetupSurfaceVisibility,0),
            'get_clicked_elements' : (getClickedElements,3),
            'remove_element' : (removeElement,2)
    }
    
    #Takes a recieved API message and processes it
    def processMessage(self, msg):
        if(msg=="quit"):
            self.looping = False
        pieces = msg.split(',') #Splits the message up into sections
        data = None #Creates an empty variable to hold the message reply
        try:
            if(len(pieces) - 4 == self.messages[pieces[0]][1]):
                data = self.messages[str(pieces[0])][0](self, pieces)
            else:
                data = {"error" : 2, "1" : str(len(pieces) - 1), "2" : str(self.messages[pieces[0]][1])}
        except KeyError, e:
            data = {"error" : 1}
        return data
    
    #Draws a cursor at the requested location and rotated as required
    def drawCursor(self,x,y,rotation,cross):
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glTranslatef(x, y, 0.0) #Translates the drawing area so that the cross is drawn in the correct place
        glRotatef(-rotation,0.0,0.0,1.0) #Rotates the drawing area so that the cross is drawn with the correct rotation

        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        glBindTexture(GL_TEXTURE_2D, self.mouse_texture.texID) #Selects the cursor texture to be used

        glBegin(GL_QUADS)
        
        #Creates the top left vertex and attaches the top left of the texture
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, 0)
        
        #Creates the top right vertex and attaches the top right of the texture
        glTexCoord2f(1.0, 1.0)
        glVertex2f(29, 0)
        
        #Creates the bottom right vertex and attaches the bottom right of the texture
        glTexCoord2f(1.0, 0.0)
        glVertex2f(29, -46)
        
        #Creates the bottom left vertex and attaches the bottom left of the texture
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, -46)
        
        glEnd() #Finalises the quad so that it is displayed
        
        if (cross==True):
            glBindTexture(GL_TEXTURE_2D, self.cross_texture.texID) #Selects the cross texture to be used
    
            glBegin(GL_QUADS)
            
            #Creates the top left vertex and attaches the top left of the texture
            glTexCoord2f(0.0, 1.0)
            glVertex2f(-20, 20)
            
            #Creates the top right vertex and attaches the top right of the texture
            glTexCoord2f(1.0, 1.0)
            glVertex2f(20, 20)
            
            #Creates the bottom right vertex and attaches the bottom right of the texture
            glTexCoord2f(1.0, 0.0)
            glVertex2f(20, -20)
            
            #Creates the bottom left vertex and attaches the bottom left of the texture
            glTexCoord2f(0.0, 0.0)
            glVertex2f(-20, -20)
            
            glEnd() #Finalises the quad so that it is displayed
        
        glPopMatrix()
        
    #Draws a cross at the desired location. This mainly exists for testing of the display code
    def drawCross(self,x,y):
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glTranslatef(x, y, 0.0) #Translates the drawing area so that the cross is drawn in the correct place

        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        glBindTexture(GL_TEXTURE_2D, self.cross_texture.texID) #Sets the cross texture to be used

        glBegin(GL_QUADS)
        
        #Creates the top left vertex and attaches the top left of the texture
        glTexCoord2f(0.0, 1.0)
        glVertex2f(-20, 20)
        
        #Creates the top right vertex and attaches the top right of the texture
        glTexCoord2f(1.0, 1.0)
        glVertex2f(20, 20)
        
        #Creates the bottom right vertex and attaches the bottom right of the texture
        glTexCoord2f(1.0, 0.0)
        glVertex2f(20, -20)
        
        #Creates the bottom left vertex and attaches the bottom left of the texture
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-20, -20)
        
        glEnd() #Finalises the quad so that it is displayed
        
        glPopMatrix()
        
    def createTexture(self,width,height,surfaceNo):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0,width,0,height)
        glMatrixMode(GL_MODELVIEW)
        rendertarget = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, rendertarget);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
                     GL_UNSIGNED_INT, None)
        fbo = c_uint(1)
        glGenFramebuffers(1)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT,
                                  GL_TEXTURE_2D, rendertarget, 0)
        glPushAttrib(GL_VIEWPORT_BIT)
        glViewport(0, 0, width, height)
        
        self.renderSurfaceTex(surfaceNo)
        
        glPopAttrib()
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        glEnable(GL_TEXTURE_2D)
        self.resize((self.winWidth, self.winHeight))#glViewport(0,0,self.winWidth,self.winHeight)
        return (rendertarget,fbo)
    
    def renderSurfaceTex(self, surfaceNo):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        windows = self.GUI.getWindows(surfaceNo) #Gathers the list of windows on the surface
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        for x in range(0,len(windows)):
            self.renderWindowContents(windows[x], self.GUI)
        cursors = self.GUI.getCursors(surfaceNo) #Gathers the list of cursors on the setup surface
        '''test = self.GUI.testForConnection(surfaceNo,"left")
        if (test[1] != "None"):
            self.drawPartialCursors(test[0],test[1],surfaceNo,"left")
        test = self.GUI.testForConnection(surfaceNo,"right")
        if (test[1] != "None"):
            self.drawPartialCursors(test[0],test[1],surfaceNo,"right")
        test = self.GUI.testForConnection(surfaceNo,"top")
        if (test[1] != "None"):
            self.drawPartialCursors(test[0],test[1],surfaceNo,"top")
        test = self.GUI.testForConnection(surfaceNo,"bottom")
        if (test[1] != "None"):
            self.drawPartialCursors(test[0],test[1],surfaceNo,"bottom")'''
        
        #Loops through all the cursors on the setup surface
        for z in range(0,len(cursors)):
            position = self.GUI.getCursorPos(cursors[z]) #Gets the position of the current cursor
            rotation = self.GUI.getCursorRotation(cursors[z]) #Gets the rotation of the current cursor
            self.drawCursor(position[0],position[1],rotation,False) #Draws the cursor at the correct position with the correct rotation
            
    '''def drawPartialCursors(self, fromSurf, inSide, toSurf, outSide):
        cursors = self.GUI.getCursors(fromSurf)
        for z in range(0,len(cursors)):
            position = self.GUI.getCursorPos(cursors[z])
            rotation = self.GUI.getCursorRotation(cursors[z])
            self.drawCursor(position[0],position[1],rotation,False)'''
        
    def drawMesh(self, surfaceNo, rotation, mirrored):
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        (rendertarget,fbo) = self.createTexture(512,512,surfaceNo)
        
        glBindTexture(GL_TEXTURE_2D, rendertarget)
        self.meshBuffer[str(surfaceNo)][0].bind_vertexes(2, GL_FLOAT)
        
        tb = None
        if(rotation==0):
            if(mirrored):
                tb = VertexBuffer(self.numpy_tex_0_m, GL_STATIC_DRAW)
            else:
                tb = VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW)
        elif(rotation==1):
            if(mirrored):
                tb = VertexBuffer(self.numpy_tex_90_m, GL_STATIC_DRAW)
            else:
                tb = VertexBuffer(self.numpy_tex_90, GL_STATIC_DRAW)
        elif(rotation==2):
            if(mirrored):
                tb = VertexBuffer(self.numpy_tex_180_m, GL_STATIC_DRAW)
            else:
                tb = VertexBuffer(self.numpy_tex_180, GL_STATIC_DRAW)
        elif(rotation==3):
            if(mirrored):
                tb = VertexBuffer(self.numpy_tex_270_m, GL_STATIC_DRAW)
            else:
                tb = VertexBuffer(self.numpy_tex_270, GL_STATIC_DRAW)
        tb.bind_texcoords(2, GL_FLOAT)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glDrawElementsui(GL_TRIANGLE_STRIP, self.renderOrder)
        
        glDisable(GL_TEXTURE_2D)
        self.meshBuffer[str(surfaceNo)][0].bind_vertexes(2, GL_FLOAT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glLineWidth(3)
        glDrawElementsui(GL_LINE_STRIP, self.left)
        glDrawElementsui(GL_LINE_STRIP, self.right)
        glDrawElementsui(GL_LINE_STRIP, self.top)
        glDrawElementsui(GL_LINE_STRIP, self.bottom)
            
        glPopMatrix()
        
        glDeleteTextures(rendertarget)
        glDeleteFramebuffers(1, fbo)
        
    def drawText(self,x,y,text,elementNo,colors):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glTranslatef(x, y, 0.0)
                
        glColor4f(float(colors[0]), float(colors[1]), float(colors[2]), float(colors[3]))
        
        self.elementBuffer[elementNo].Render(text)
        
        glPopMatrix()
    
    #When passed a list of coordinates uses them to draw a line strip
    def drawLineStrip(self,elementNo,width,color,count):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glColor4f(float(color[0]), float(color[1]), float(color[2]), float(color[3])) #Sets the drawing color to white (THIS WILL BE CHANGED)
        glLineWidth(float(width))
        
        self.elementBuffer[elementNo][0].bind_vertexes(2,GL_FLOAT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawElementsui(GL_LINE_STRIP, range(0, count))
        
        glPopMatrix()
        
    def drawPolygon(self,elementNo,color,count):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glColor4f(float(color[0]), float(color[1]), float(color[2]), float(color[3]))
        #glLineWidth(5.0)
        
        self.elementBuffer[elementNo][0].bind_vertexes(2,GL_FLOAT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawElementsui(GL_POLYGON, range(0, count))
        
        glPopMatrix()
        
    def drawTexturedPolygon(self,elementNo,count):
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glColor4f(1, 1, 1, 1)

        glBindTexture(GL_TEXTURE_2D, self.textureBuffer[elementNo].texID)
        
        self.elementBuffer[elementNo][0].bind_vertexes(2,GL_FLOAT)
        self.elementBuffer[elementNo][1].bind_texcoords(2, GL_FLOAT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glDrawElementsui(GL_POLYGON, range(0, count))
        
        glPopMatrix()
        
    def renderWindowContents(self, windowNo, GUIRead):
        elements = GUIRead.getVisibleElements(int(windowNo)) #Gathers the list of elements in the window
        #Loops through the elements in the window
        for z in range(0,len(elements)):
            type = GUIRead.getEleType(elements[z]) #Gets the type of the current element
            
            if(type=="circle"): #Runs if the current element is a circle
                upToDate = GUIRead.upToDateCircle(elements[z])
                color = GUIRead.getCircleFill(elements[z])
                colors = color.split(":")
                sides = GUIRead.getCircleSides(elements[z])
                if(upToDate==False):
                    rad = GUIRead.getCircleRad(elements[z])
                    cirPos = GUIRead.getCirclePos(elements[z])
                    points = []
                    for i in range(sides):
                        cosine = float(rad) * cos(i*2*pi/sides)
                        sine = float(rad) * sin(i*2*pi/sides)
                        points.append([cosine+float(cirPos[0]),sine+float(cirPos[1])])
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),sides)
            elif(type=="lineStrip"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateLineStrip(elements[z])
                noPoints = GUIRead.getLineStripPointsCount(elements[z]) #Gets the number of points in the line strip
                
                #Runs if there is more than one point in the line strip (otherwise the line strip wont be shown)
                if(noPoints>1):
                    color = GUIRead.getLineStripColor(elements[z])
                    noPoints = GUIRead.getLineStripPointsCount(elements[z])
                    if(upToDate==False):
                        strip = [] #Creates an empty list to hold the line strip points
                        #Loops through the points in the line strip
                        for point in range(0,noPoints):
                            pos = GUIRead.getLineStripPoint(elements[z],point) #Gets the position of the current point
                            drawPos = [pos[0], pos[1]] #Converts the position of the point based on the window location
                            strip.append(drawPos) #Adds the calculated position to the point list
                        numpy_verts = numpy.array(strip, dtype=numpy.float32)
                        self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                    self.drawLineStrip(elements[z],GUIRead.getLineStripWidth(elements[z]),(colors[0],colors[1],colors[2],colors[3]),GUIRead.getLineStripPointsCount(elements[z])) #Draws a strip based on the point list
            elif(type=="polygon"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDatePolygon(elements[z])
                noPoints = GUIRead.getPolygonPointsCount(elements[z])
                if(noPoints>2):
                    color = GUIRead.getPolygonFillColor(elements[z])
                    colors = color.split(":")
                    if(upToDate==False):
                        points = []
                        for point in range(0,noPoints):
                            pos = GUIRead.getPolygonPoint(elements[z],point)
                            drawPos = [pos[0], pos[1]]
                            points.append(drawPos)
                        numpy_verts = numpy.array(points, dtype=numpy.float32)
                        self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                    self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),noPoints)
            elif(type=="rectangle"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateRectangle(elements[z])
                color = GUIRead.getRectangleFillColor(elements[z])
                colors = color.split(":")
                if(upToDate==False):
                    points = []
                    temp = GUIRead.getRectangleTopLeft(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleTopRight(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleBottomRight(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleBottomLeft(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),4)
            elif(type=="line"):
                upToDate = GUIRead.upToDateLineStrip(elements[z])
                color = GUIRead.getLineColor(elements[z])
                colors = color.split(":")
                if(upToDate==False):
                    points = [] #Creates an empty list to hold the line points
                    start = GUIRead.getLineStart(elements[z])
                    end = GUIRead.getLineEnd(elements[z])
                    points.append([start[0],start[1]])
                    points.append([end[0],end[1]])
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawLineStrip(elements[z],GUIRead.getLineWidth(elements[z]),(colors[0],colors[1],colors[2],colors[3]),2) #Draws a line based on the points
            elif(type=="text"):
                upToDate = GUIRead.upToDateText(elements[z])
                color = GUIRead.getTextColor(elements[z])
                colors = color.split(":")
                pos=GUIRead.getTextPos(elements[z])
                text=GUIRead.getText(elements[z])
                if(upToDate==False):
                    font=GUIRead.getFont(elements[z])
                    size=GUIRead.getPtSize(elements[z])
                    
                    if(self.fonts.has_key(font)):
                        font = self.fonts[font]
                    
                    self.elementBuffer[elements[z]] = FTGL.PolygonFont(font + ".ttf")
                    self.elementBuffer[elements[z]].FaceSize(size)
                    self.elementBuffer[elements[z]].UseDisplayList(True)
                self.drawText(pos[0], pos[1], text, elements[z],(colors[0],colors[1],colors[2],colors[3]))
            elif(type=="texRectangle"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateTexRectangle(elements[z])
                if(upToDate==False):
                    texture = GUIRead.getTexRectangleTexture(elements[z])
                    self.textureBuffer[elements[z]] = Texture(texture)
                    texCoors = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]
                    points = []
                    temp = GUIRead.getTexRectangleTopLeft(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleTopRight(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleBottomRight(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleBottomLeft(elements[z])
                    drawPos = [temp[0],temp[1]]
                    points.append(drawPos)
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    numpy_tex = numpy.array(texCoors, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(numpy_tex, GL_STATIC_DRAW))
                self.drawTexturedPolygon(elements[z], 4)
        glColor4f(1,1,1,1)
        
    #Processes the GUI data for the desired window and calls functions to draw the elements contained within it
    def displayWindow(self, windowNo, GUIRead):
        winPos = GUIRead.getWindowPos(windowNo) #Fetches the position of the upper left corner of the window
        width = GUIRead.getWindowWidth(windowNo) #Fetches the width of the window
        height = GUIRead.getWindowHeight(windowNo) #Fetches the height of the window
        elements = GUIRead.getVisibleElements(int(windowNo)) #Gathers the list of elements in the window
        
        #Loops through the elements in the window
        for z in range(0,len(elements)):
            type = GUIRead.getEleType(elements[z]) #Gets the type of the current element
            
            if(type=="circle"): #Runs if the current element is a circle
                upToDate = GUIRead.upToDateCircle(elements[z])
                color = GUIRead.getCircleFill(elements[z])
                colors = color.split(":")
                sides = GUIRead.getCircleSides(elements[z])
                if(upToDate==False):
                    rad = GUIRead.getCircleRad(elements[z])
                    cirPos = GUIRead.getCirclePos(elements[z])
                    points = []
                    for i in range(sides):
                        cosine = float(rad) * cos(i*2*pi/sides)
                        sine = float(rad) * sin(i*2*pi/sides)
                        points.append([cosine+float(cirPos[0])+float(winPos[0]),sine+float(cirPos[1])+float(winPos[1])-height])
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),sides)
            elif(type=="lineStrip"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateLineStrip(elements[z])
                noPoints = GUIRead.getLineStripPointsCount(elements[z]) #Gets the number of points in the line strip
                
                #Runs if there is more than one point in the line strip (otherwise the line strip wont be shown)
                if(noPoints>1):
                    color = GUIRead.getLineStripColor(elements[z])
                    colors = color.split(":")
                    if(upToDate==False):
                        strip = []
                        #Loops through the points in the line strip
                        for point in range(0,noPoints):
                            pos = GUIRead.getLineStripPoint(elements[z],point) #Gets the position of the current point
                            drawPos = [winPos[0] + pos[0], winPos[1] - height + pos[1]] #Converts the position of the point based on the window location
                            strip.append(drawPos)
                        numpy_verts = numpy.array(strip, dtype=numpy.float32)
                        self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                    self.drawLineStrip(elements[z],GUIRead.getLineStripWidth(elements[z]),(colors[0],colors[1],colors[2],colors[3]),GUIRead.getLineStripPointsCount(elements[z])) #Draws a strip based on the point list
            elif(type=="polygon"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDatePolygon(elements[z])
                noPoints = GUIRead.getPolygonPointsCount(elements[z])
                if(noPoints>2):
                    color = GUIRead.getPolygonFillColor(elements[z])
                    colors = color.split(":")
                    if(upToDate==False):
                        points = []
                        for point in range(0,noPoints):
                            pos = GUIRead.getPolygonPoint(elements[z],point)
                            drawPos = [pos[0]+winPos[0], pos[1] + winPos[1] - height]
                            points.append(drawPos)
                        numpy_verts = numpy.array(points, dtype=numpy.float32)
                        self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                    self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),noPoints)
            elif(type=="rectangle"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateRectangle(elements[z])
                color = GUIRead.getRectangleFillColor(elements[z])
                colors = color.split(":")
                if(upToDate==False):
                    points = []
                    temp = GUIRead.getRectangleTopLeft(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleTopRight(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleBottomRight(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getRectangleBottomLeft(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawPolygon(elements[z], (colors[0],colors[1],colors[2],colors[3]),4)
            elif(type=="line"):
                upToDate = GUIRead.upToDateLineStrip(elements[z])
                color = GUIRead.getLineColor(elements[z])
                colors = color.split(":")
                if(upToDate==False):
                    points = [] #Creates an empty list to hold the line points
                    start = GUIRead.getLineStart(elements[z])
                    end = GUIRead.getLineEnd(elements[z])
                    points.append([float(start[0])+winPos[0],float(start[1])+winPos[1]-height])
                    points.append([float(end[0])+winPos[0],float(end[1])+winPos[1]-height])
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                self.drawLineStrip(elements[z],GUIRead.getLineWidth(elements[z]),(colors[0],colors[1],colors[2],colors[3]),2) #Draws a line based on the points
            elif(type=="text"):
                upToDate = GUIRead.upToDateText(elements[z])
                color = GUIRead.getTextColor(elements[z])
                colors = color.split(":")
                text=GUIRead.getText(elements[z])
                pos=GUIRead.getTextPos(elements[z])
                if(upToDate==False):
                    font=GUIRead.getFont(elements[z])
                    size=GUIRead.getPtSize(elements[z])
                    
                    if(self.fonts.has_key(font)):
                        font = self.fonts[font]
                    
                    self.elementBuffer[elements[z]] = FTGL.PolygonFont(font + ".ttf")
                    self.elementBuffer[elements[z]].FaceSize(size)
                    self.elementBuffer[elements[z]].UseDisplayList(True)
                self.drawText(pos[0], pos[1], text, elements[z],(colors[0],colors[1],colors[2],colors[3]))
            elif(type=="texRectangle"): #Runs if the current element is a line strip
                upToDate = GUIRead.upToDateTexRectangle(elements[z])
                if(upToDate==False):
                    texture = GUIRead.getTexRectangleTexture(elements[z])
                    self.textureBuffer[elements[z]] = Texture(texture)
                    texCoors = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]
                    points = []
                    temp = GUIRead.getTexRectangleTopLeft(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleTopRight(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleBottomRight(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    temp = GUIRead.getTexRectangleBottomLeft(elements[z])
                    drawPos = [temp[0] + winPos[0],temp[1] + winPos[1] - height]
                    points.append(drawPos)
                    numpy_verts = numpy.array(points, dtype=numpy.float32)
                    numpy_tex = numpy.array(texCoors, dtype=numpy.float32)
                    self.elementBuffer[elements[z]] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(numpy_tex, GL_STATIC_DRAW))
                self.drawTexturedPolygon(elements[z], 4)
                
    #Checks the setuo GUI and displays any required windows and cursors on it by calling the relevant functions
    def checkSetupGUI(self):
        
        #Runs if the setup surface is meant to be visible
        if(self.GUI.getSetupSurfaceVisibilty()==True):
            GUIRead = self.GUI # Makes a copy of the GUI so that changes during rendering don't cause problems

            windows = GUIRead.getWindows(0) #Gathers the list of windows on the setup surface

            #print str(len(windows))
            
            #Loops through all the windows on the setup surface
            for z in range(0,len(windows)):
                self.displayWindow(windows[z],GUIRead) #Renders the current window in the list
            
            cursors = GUIRead.getCursors(0) #Gathers the list of cursors on the setup surface
            
            #Loops through all the cursors on the setup surface
            for z in range(0,len(cursors)):
                position = GUIRead.getCursorPos(cursors[z]) #Gets the position of the current cursor
                rotation = GUIRead.getCursorRotation(cursors[z]) #Gets the rotation of the current cursor
                self.drawCursor(position[0],position[1],rotation,True) #Draws the cursor at the correct position with the correct rotation
	
    #Resizes the window to the desired width and height
    def resize(self, (width, height)):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0, width, height, 0, 0, 1)
        gluOrtho2D(0, self.winWidth, 0, self.winHeight)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    #Prepares the opengl code 
    def init(self):
        # set some basic OpenGL settings and control variables
        #glShadeModel(GL_SMOOTH)
        parser = SafeConfigParser()
        parser.read("config.ini")
        temp = parser.getint('surfaces','showMeshLines')
        if(temp==0):
            self.showMeshLines = False
        else:
            self.showMeshLines = True
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glEnable(GL_ALPHA_TEST)
		
        #Loads the cursor and cross textures into memory
        self.mouse_texture = Texture("cursor.png")
        self.cross_texture = Texture("cursorcross.png")
		
        self.demandedFps = 30.0 #Indicates the number of desired frames per second
        
        self.meshBuffer = {}
        
        self.renderOrder = []
        lTOr = True
        for y in range(0,self.pps-1):
            if(lTOr == True):
                for x in range(0,self.pps):
                    self.renderOrder.append(self.pps*y + x)
                    self.renderOrder.append(self.pps*(y+1) + x)
                lTOr = False
            else:
                for x in range(0,self.pps):
                    self.renderOrder.append(self.pps*y + self.pps-1-x)
                    self.renderOrder.append(self.pps*(y+1) + self.pps-1-x)
                lTOr = True
        tex = []
        
        self.meshLines=[]
        revFlag = False
        columns = []
        self.top = []
        self.bottom = []
        for x in range(0,self.pps):
            for y in range(0,self.pps):
                if (revFlag == False):
                    columns.append(x+self.pps*y)
                    if(x==0):
                        self.top.append(x+self.pps*y)
                    elif(x==self.pps-1):
                        self.bottom.append(x+self.pps*y)
                else:
                    columns.append(x+self.pps*(self.pps-1-y))
                    if(x==self.pps-1):
                        self.bottom.append(x+self.pps*(self.pps-1-y))
            if revFlag==False:
                revFlag=True
            else:
                revFlag=False
        self.meshLines.append(columns)
        revFlag = False
        rows = []
        self.left = []
        self.right = []
        for y in range(0,self.pps):
            for x in range(0,self.pps):
                if (revFlag == False):
                    rows.append(x+self.pps*y)
                    if(y==0):
                        self.left.append(x+self.pps*y)
                    elif(y==self.pps-1):
                        self.right.append(x+self.pps*y)
                else:
                    rows.append(self.pps-1-x+self.pps*y)
                    if(y==self.pps-1):
                        self.right.append(self.pps-1-x+self.pps*y)
            if revFlag==False:
                revFlag=True
            else:
                revFlag=False
        self.meshLines.append(rows)
                
        for y in list(reversed(range(0,self.pps))):
            for x in range(0,self.pps):
                tex.append([(1.0/(self.pps-1))*x,(1.0/(self.pps-1))*y])
        self.numpy_tex_0 = numpy.array(tex, dtype=numpy.float32)
        tex = list(reversed(tex))
        self.numpy_tex_180 = numpy.array(tex, dtype=numpy.float32)

        tex=[]
        for x in range(0,self.pps):
            for y in range(0,self.pps):
                tex.append([(1.0/(self.pps-1))*x,(1.0/(self.pps-1))*y])
        self.numpy_tex_90 = numpy.array(tex, dtype=numpy.float32)
        tex = list(reversed(tex))
        self.numpy_tex_270 = numpy.array(tex, dtype=numpy.float32)

        tex=[]
        for x in list(reversed(range(0,self.pps))):
            for y in range(0,self.pps):
                tex.append([(1.0/(self.pps-1))*x,(1.0/(self.pps-1))*y])
        self.numpy_tex_90_m = numpy.array(tex, dtype=numpy.float32)
        tex = list(reversed(tex))
        self.numpy_tex_270_m = numpy.array(tex, dtype=numpy.float32)
		
        tex=[]
        for y in list(reversed(range(0,self.pps))):
            for x in list(reversed(range(0,self.pps))):
                tex.append([(1.0/(self.pps-1))*x,(1.0/(self.pps-1))*y])
        self.numpy_tex_0_m = numpy.array(tex, dtype=numpy.float32)
        tex = list(reversed(tex))
        self.numpy_tex_180_m = numpy.array(tex, dtype=numpy.float32)
    
    #Starts the pygame window and runs the rendering loop
    def display(self):
        video_flags = OPENGL | DOUBLEBUF
		
        pygame.init()
        pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.set_mode((self.winWidth, self.winHeight), video_flags)
		
        pygame.display.set_caption("Display") #Sets the window name
		
        self.resize((self.winWidth, self.winHeight)) #Resizes winding
        self.init() #Initialises OpenGL
		
        clock = pygame.time.Clock() #Creates a clock to enable FPS control
        
        #The rendering loop
        while self.looping:
            event = pygame.event.poll() # Polls for events
            
            #If a quit event has been received the program is closed
            if event.type == QUIT:
                pygame.quit () 
                break
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            surfaceList = self.GUI.getDefinedSurfaces()
            if(len(surfaceList)>0):
                for z in range(0,len(surfaceList)):
                    if(self.GUI.checkSurfaceRenderUpdate(z+1)):   
                        mesh = self.GUI.getSurfacePoints(z+1)
                        
                        verts = []
                        tex = []
                        for y in range(0,self.pps):
                            for x in range(0,self.pps):
                                meshloc = mesh[str(x) + "," + str(y)]
                                verts.append([meshloc[0],meshloc[1]])
                        numpy_verts = numpy.array(verts, dtype=numpy.float32)
                        self.meshBuffer[str(z+1)] = (VertexBuffer(numpy_verts, GL_STATIC_DRAW),VertexBuffer(self.numpy_tex_0, GL_STATIC_DRAW))
                    rot = self.GUI.getSurfaceRotation(z+1)
                    mir = self.GUI.getSurfaceMirrored(z+1)
                    self.drawMesh(z+1,rot,mir)
                    if(self.showMeshLines==True):
                        for x in range(0,len(self.meshLines)):
                            self.meshBuffer[str(z+1)][0].bind_vertexes(2, GL_FLOAT)
                            glEnableClientState(GL_VERTEX_ARRAY)
                            glColor4f(0,1,1,1)
                            glLineWidth(1)
                            glDrawElementsui(GL_LINE_STRIP, self.meshLines[x])
                    
            self.checkSetupGUI() #The setup GUI is rendered if it is meant to be visible
			
            pygame.display.flip() #Displays the display surface on the screen
            
            time.sleep(1.0/self.demandedFps)
			
            #clock.tick(self.demandedFps) #Sets the maximum FPS allowed
        time.sleep(0.1)
        pygame.quit()
	
    #Creates a GUI object and starts a thread to display its contents
    def __init__(self):
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.pps = parser.getint('surfaces','curveResolution')
        self.winWidth = parser.getint('surfaces', 'windowWidth')
        self.winHeight = parser.getint('surfaces', 'windowHeight')
        self.GUI = GUI() #Creates the GUI
        thread = Thread(target=self.display, args=()) #Creates the display thread
        thread.start() #Starts the display thread