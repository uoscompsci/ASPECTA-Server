from ConfigParser import SafeConfigParser
from kivy.core.window import Window
from GUI import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.graphics import Rectangle, Color, Ellipse, Line, Fbo
from kivy.core.image import Image
from kivy.properties import ObjectProperty
from kivy.base import EventLoop
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty, Property
from kivy.vector import Vector
from random import random
import socket
from collections import deque
import select
import ujson as json
import base64
from threading import Thread
from time import sleep
import sys
import glob
import os
import FTGL

class CircleWidget(Widget):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)
    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)


class TexRectangleWidget(Widget):
    texture = ObjectProperty(None, allownone=True)
    def __init__(self, **kwargs):
        super(TexRectangleWidget, self).__init__(**kwargs)

class RectangleWidget(Widget):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)
    def __init__(self, **kwargs):
        super(RectangleWidget, self).__init__(**kwargs)

class LineWidget(Widget):
    pos1 = ListProperty(0)
    pos2 = ListProperty(0)
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)
    def __init__(self, **kwargs):
        super(LineWidget, self).__init__(**kwargs)


class renderSurface(FloatLayout):
    server_started=False
    queue = deque([])
    sock2usr = {}
    app2sock = {}
    sock2app = {}
    loop = True
    GUI = None
    meshBuffer = None
    renderOrder = None
    elementBuffer = None
    winWidth = None
    winHeight = None
    canvases = {}
    elements = {}
    cursors = {}
    fonts = {"Times New Roman": "FreeSerif",
             "Free Serif": "FreeSerif",
             "Free Mono": "FreeMono",
             "Courier New": "FreeMono",
             "Arial": "FreeSans",
             "Free Sans": "FreeSans"
             }

    def __init__(self, **kwargs):
        super(renderSurface, self).__init__(**kwargs)
        self.server_init()
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.pps = parser.getint('surfaces', 'curveResolution')
        self.winWidth = parser.getint('display', 'HorizontalRes')
        self.winHeight = parser.getint('display', 'VerticalRes')
        self.fullscreen = parser.getint('display', 'fullscreen')
        self.GUI = GUI(self.winWidth, self.winHeight)  # Creates the GUI

    # Creates a new surface for projection as requested by the API call
    def newSurface(self, pieces):
        surfaceNo = self.GUI.newSurface(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'])
        return {'surfaceNo': surfaceNo}

    # Creates a new surface for projection with an ID as requested by the API Call
    def newSurfaceWithID(self, pieces):
        surfaceNo = self.GUI.newSurfaceWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'])
        return {'surfaceNo': surfaceNo}

    # Creates a new cursor on the desired surface as requested by the API call
    def newCursor(self, pieces):
        cursorNo = self.GUI.newCursor(pieces['surfaceNo'], pieces['x'], pieces['y'], pieces['coorSys'])
        x,y = int(float(pieces['x'])), int(float(pieces['y']))
        with self.canvas:
            Color(1, 1, 1, 1)
            self.tex = Image.load("icons/dcursor.png").texture
            self.cursors[cursorNo] = Rectangle(pos=(x,y-94/2),size=(59/2,94/2),texture=self.tex)
        return {"cursorNo": cursorNo}

    # Creates a new cursor with an ID on the desired surface as requested by the API call
    def newCursorWithID(self, pieces):
        cursorNo = self.GUI.newCursorWithID(pieces['ID'], pieces['surfaceNo'], pieces['x'], pieces['y'],
                                            pieces['coorSys'])
        return {"cursorNo": cursorNo}

    # Creates a new canvas on the desired surface as requested by the API call
    def newCanvas(self, pieces):
        canvasNo = self.GUI.newCanvas(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['surfaceNo'],
                                      pieces['x'], pieces['y'], pieces['width'], pieces['height'], pieces['coorSys'],
                                      pieces['name'])
        width, height = int(pieces['width']), int(pieces['height'])
        return {"canvasNo": canvasNo}

    # Creates a new canvas with an ID on the desired surface as requested by the API call
    def newCanvasWithID(self, pieces):
        canvasNo = self.GUI.newCanvasWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                            pieces['surfaceNo'], pieces['x'], pieces['y'], pieces['width'],
                                            pieces['height'], pieces['coorSys'], pieces['name'])
        return {"canvasNo": canvasNo}

    # Creates a new circle on the desired canvas as requested by the API call
    def newCircle(self, pieces):
        elementNo = self.GUI.newCircle(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                       pieces['x'], pieces['y'], pieces['radius'], pieces['coorSys'],
                                       pieces['lineColor'], pieces['lineWidth'], pieces['fillColor'], pieces['sides'])
        x,y,radius = int(float(pieces['x'])), int(float(pieces['y'])), int(float(pieces['radius']))
        colors = pieces['fillColor'].split(":")
        r,g,b,a = float(colors[0]), float(colors[1]), float(colors[2]), float(colors[3])
        circ = CircleWidget(pos=(x,y),size=(radius,radius), r=r, g=g, b=b, a=a)
        self.add_widget(circ)
        self.elements[elementNo] = circ
        return {"elementNo": elementNo}

    # Creates a new circle with an ID on the desired canvas as requested by the API call
    def newCircleWithID(self, pieces):
        elementNo = self.GUI.newCircleWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                             pieces['canvasNo'], pieces['x'], pieces['y'], pieces['radius'],
                                             pieces['coorSys'], pieces['lineColor'], pieces['lineWidth'],
                                             pieces['fillColor'], pieces['sides'])
        return {"elementNo": elementNo}

    # Creates a new line on the desired canvas as requested by the API call
    def newLine(self, pieces):
        elementNo = self.GUI.newLine(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                     pieces['xStart'], pieces['yStart'], pieces['xEnd'], pieces['yEnd'],
                                     pieces['coorSys'], pieces['color'], pieces['width'])
        xstart,ystart,xend,yend,width = int(long(pieces['xStart'])),int(long(pieces['yStart'])),int(long(pieces['xEnd'])),int(long(pieces['yEnd'])),int(long(pieces['width']))
        colors = pieces['color'].split(":")
        r,g,b,a = float(colors[0]), float(colors[1]), float(colors[2]), float(colors[3])
        line = LineWidget(pos1=(xstart,ystart), pos2=(xend,yend), width=width, r=r, g=g, b=b, a=a)
        self.add_widget(line)
        self.elements[elementNo] = line
        return {"elementNo": elementNo}

    # Creates a new line with an ID in the desired canvas as requested by the API call
    def newLineWithID(self, pieces):
        elementNo = self.GUI.newLineWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                           pieces['canvasNo'], pieces['xStart'], pieces['yStart'], pieces['xEnd'],
                                           pieces['yEnd'], pieces['coorSys'], pieces['color'], pieces['width'])
        return {"elementNo": elementNo}

    # Creates the starting point of a new line strip on the desired canvas as requested by the API call
    def newLineStrip(self, pieces):
        elementNo = self.GUI.newLineStrip(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                          pieces['x'], pieces['y'], pieces['coorSys'], pieces['color'], pieces['width'])
        return {"elementNo": elementNo}

    # Creates the starting point of a new line strip with an ID on the desired canvas as requested by the API call
    def newLineStripWithID(self, pieces):
        elementNo = self.GUI.newLineStripWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                                pieces['canvasNo'], pieces['x'], pieces['y'], pieces['coorSys'],
                                                pieces['color'], pieces['width'])
        return {"elementNo": elementNo}

    # Creates the starting point of a new polygon on the desired canvas as requested by the API call
    def newPolygon(self, pieces):
        elementNo = self.GUI.newPolygon(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                        pieces['x'], pieces['y'], pieces['coorSys'], pieces['lineColor'],
                                        pieces['lineWidth'], pieces['fillColor'])
        return {"elementNo": elementNo}

    # Creates the starting point of a new polygon with an ID on the desired canvas as requested by the API call
    def newPolygonWithID(self, pieces):
        elementNo = self.GUI.newPolygonWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                              pieces['canvasNo'], pieces['x'], pieces['y'], pieces['coorSys'],
                                              pieces['lineColor'], pieces['lineWidth'], pieces['fillColor'])
        return {"elementNo": elementNo}

    # Creates a new rectangle on the desired canvas as requested by the API call
    def newRectangle(self, pieces):
        elementNo = self.GUI.newRectangle(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                          pieces['x'], pieces['y'], pieces['width'], pieces['height'],
                                          pieces['coorSys'], pieces['lineColor'], pieces['lineWidth'],
                                          pieces['fillColor'])
        x,y,width,height = int(float(pieces['x'])), int(float(pieces['y'])), int(float(pieces['width'])), int(float(pieces['height']))
        colors = pieces['fillColor'].split(":")
        r,g,b,a = float(colors[0]), float(colors[1]), float(colors[2]), float(colors[3])
        rect = RectangleWidget(pos=(x,y),size=(width,height), r=r, g=g, b=b, a=a)
        self.add_widget(rect)
        self.elements[elementNo] = rect
        return {"elementNo": elementNo}

    # Creates a new rectangle with an ID on the desired canvas as requested by the API call
    def newRectangleWithID(self, pieces):
        elementNo = self.GUI.newRectangleWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                                pieces['canvasNo'], pieces['x'], pieces['y'], pieces['width'],
                                                pieces['height'], pieces['coorSys'], pieces['lineColor'],
                                                pieces['lineWidth'], pieces['fillColor'])
        return {"elementNo": elementNo}

    # Creates a new textured rectangle on the desired canvas as requested by the API call
    def newTexRectangle(self, pieces):
        elementNo = self.GUI.newTexRectangle(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'],
                                             pieces['canvasNo'], pieces['x'], pieces['y'], pieces['width'],
                                             pieces['height'], pieces['coorSys'], pieces['imageID'])
        x,y,width,height = int(float(pieces['x'])), int(float(pieces['y'])), int(float(pieces['width'])), int(float(pieces['height']))
        texturefile = glob.glob('images/' + str(pieces['imageID']) + "*")
        texrect = TexRectangleWidget(pos=(x,y),size=(width,height), texture=Image.load(texturefile[0]).texture)
        self.add_widget(texrect)
        self.elements[elementNo] = texrect
        return {"elementNo": elementNo}

    # Creates a new textured rectangle with an ID on the desired canvas as requested by the API call
    def newTexRectangleWithID(self, pieces):
        elementNo = self.GUI.newTexRectangleWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'],
                                                   pieces['ID'], pieces['canvasNo'], pieces['x'], pieces['y'],
                                                   pieces['width'], pieces['height'], pieces['coorSys'],
                                                   pieces['imageID'])
        return {"elementNo": elementNo}

    # Creates a new block of text on the desired canvas as requested by the API call
    def newText(self, pieces):
        elementNo = self.GUI.newText(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['canvasNo'],
                                     pieces['text'], pieces['x'], pieces['y'], pieces['coorSys'], pieces['ptSize'],
                                     pieces['font'], pieces['color'])
        return {"elementNo": elementNo}

    # Creates a new block of text with an ID on the desired canvas as requested by the API call
    def newTextWithID(self, pieces):
        elementNo = self.GUI.newTextWithID(pieces['IDuser'], pieces['IDapp'], pieces['IDinstance'], pieces['ID'],
                                           pieces['canvasNo'], pieces['text'], pieces['x'], pieces['y'],
                                           pieces['coorSys'], pieces['ptSize'], pieces['font'], pieces['color'])
        return {"elementNo": elementNo}

    # Subscribes the current user to a surface
    def subscribeToSurface(self, pieces):
        self.GUI.subscribeToSurface(pieces['IDapp'] + "," + pieces['IDinstance'], pieces['surfaceNo'])
        return {}

    # Gets the ID of a surface
    def getSurfaceID(self, pieces):
        ID = self.GUI.getSurfaceID(pieces['surfaceNo'])
        return {"ID": ID}

    # Sets the ID of a surface
    def setSurfaceID(self, pieces):
        self.GUI.setSurfaceID(pieces['surfaceNo'], pieces['ID'])
        return {}

    # Gets the owner of a surface
    def getSurfaceOwner(self, pieces):
        owner = self.GUI.getSurfaceOwner(pieces['surfaceNo'])
        return {"owner": owner}

    # Gets the details of the creator application of a surface
    def getSurfaceAppDetails(self, pieces):
        app = self.GUI.getSurfaceAppDetails(pieces['surfaceNo'])
        return {"app": app[0], "instance": app[1]}

    # Returns all surfaces with the desired ID
    def getSurfacesByID(self, pieces):
        found = self.GUI.getSurfacesByID(pieces['ID'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    # Returns all surfaces with the desired owner
    def getSurfacesByOwner(self, pieces):
        found = self.GUI.getSurfacesByOwner(pieces['owner'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    # Returns all surfaces with the desired app name
    def getSurfacesByAppName(self, pieces):
        found = self.GUI.getSurfacesByAppName(pieces['name'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    # Returns all surfaces with the desired application details
    def getSurfacesByAppDetails(self, pieces):
        found = self.GUI.getSurfacesByAppDetails(pieces['name'], pieces['number'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    # Registers the application as the admin for the surface
    def becomeSurfaceAdmin(self, pieces):
        test = self.GUI.becomeSurfaceAdmin(pieces['surfaceNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    # Deregisters the current user as admin for the surface
    def stopBeingSurfaceAdmin(self, pieces):
        test = self.GUI.stopBeingSurfaceAdmin(pieces['surfaceNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    # Sets the edge points for a surface
    def setSurfaceEdges(self, pieces):
        self.GUI.setSurfacePoints(pieces['surfaceNo'], pieces['topString'], pieces['bottomString'],
                                  pieces['leftString'], pieces['rightString'])
        return {}

    # Removes all the known edge points from a surface so it is no longer shown.
    def undefineSurface(self, pieces):
        self.GUI.undefineSurface(pieces['surfaceNo'])
        return {}

    def saveDefinedSurfaces(self, pieces):
        self.GUI.saveDefinedSurfaces(pieces['fileName'])
        return {}

    def loadDefinedSurfaces(self, pieces):
        count = self.GUI.loadDefinedSurfaces(pieces['fileName'])
        return {"count": count[0], "layouts": count[1], "connections": count[2], "realSizes": count[3]}

    def getSavedLayouts(self, pieces):
        layouts = glob.glob('layouts/*.lyt')
        dict = {}
        dict["count"] = len(layouts)
        for x in range(0, len(layouts)):
            dict[x] = layouts[x].split(".")[0].split("/")[1]
        return dict

    def getSavedImages(self, pieces):
        images = glob.glob('images/*')
        dict = {}
        dict["count"] = len(images)
        for x in range(0, len(images)):
            dict[x] = images[x].split("/")[1]
        return dict

        # def setUploadName(self, pieces):
        # self.fts.setFileName(pieces['fileName'])
        # ftsthread = Thread(target=self.fts.awaitConnection, args=())
        # ftsthread.start()

    def getSurfacePixelWidth(self, pieces):
        width = self.GUI.getSurfacePixelWidth(pieces['surfaceNo'])
        return {"width": width}

    def getSurfacePixelHeight(self, pieces):
        height = self.GUI.getSurfacePixelHeight(pieces['surfaceNo'])
        return {"height": height}

    def setSurfacePixelWidth(self, pieces):
        self.GUI.setSurfacePixelWidth(pieces['surfaceNo'], pieces['width'])
        return {}

    def setSurfacePixelHeight(self, pieces):
        self.GUI.setSurfacePixelHeight(pieces['surfaceNo'], pieces['height'])
        return {}

    def getSurfaceRealWidth(self, pieces):
        width = self.GUI.getSurfaceRealWidth(pieces['surfaceNo'])
        return {"width": width}

    def getSurfaceRealHeight(self, pieces):
        height = self.GUI.getSurfaceRealHeight(pieces['surfaceNo'])
        return {"height": height}

    def setSurfaceRealWidth(self, pieces):
        self.GUI.setSurfaceRealWidth(pieces['surfaceNo'], pieces['width'])
        return {}

    def setSurfaceRealHeight(self, pieces):
        self.GUI.setSurfaceRealHeight(pieces['surfaceNo'], pieces['height'])
        return {}

    def clearSurface(self, pieces):
        self.GUI.clearSurface(pieces['surfaceNo'])
        return {}

    def deleteLayout(self, pieces):
        os.remove("layouts/" + pieces[1] + ".lyt")
        return {}

    def deleteImage(self, pieces):
        os.remove("images/" + pieces[1])
        return {}

    def rotateSurfaceTo0(self, pieces):
        self.GUI.rotateSurfaceTo0(pieces['surfaceNo'])
        return {}

    def rotateSurfaceTo90(self, pieces):
        self.GUI.rotateSurfaceTo90(pieces['surfaceNo'])
        return {}

    def rotateSurfaceTo180(self, pieces):
        self.GUI.rotateSurfaceTo180(pieces['surfaceNo'])
        return {}

    def rotateSurfaceTo270(self, pieces):
        self.GUI.rotateSurfaceTo270(pieces['surfaceNo'])
        return {}

    def mirrorSurface(self, pieces):
        self.GUI.mirrorSurface(pieces['surfaceNo'])
        return {}

    def connectSurfaces(self, pieces):
        self.GUI.connectSurfaces(pieces['surfaceNo1'], pieces['side1'], pieces['surfaceNo2'], pieces['side2'])
        return {}

    def disconnectSurfaces(self, pieces):
        self.GUI.disconnectSurfaces(pieces['surfaceNo1'], pieces['side1'], pieces['surfaceNo2'], pieces['side2'])
        return {}

    def subscribeToCanvas(self, pieces):
        self.GUI.subscribeToCanvas(pieces['IDapp'] + "," + pieces['IDinstance'], pieces['canvasNo'])
        return {}

    def getCanvasID(self, pieces):
        ID = self.GUI.getCanvasID(pieces['canvasNo'])
        return {"ID": ID}

    def setCanvasID(self, pieces):
        self.GUI.setCanvasID(pieces['canvasNo'], pieces['ID'])
        return {}

    def getCanvasOwner(self, pieces):
        owner = self.GUI.getCanvasOwner(pieces['canvasNo'])
        return {"owner": owner}

    def getCanvasAppDetails(self, pieces):
        app = self.GUI.getCanvasAppDetails(pieces['canvasNo'])
        return {"app": app[0], "instance": app[1]}

    def getCanvasesByID(self, pieces):
        found = self.GUI.getCanvasesByID(pieces['ID'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getCanvasesByOwner(self, pieces):
        found = self.GUI.getCanvasesByOwner(pieces['owner'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getCanvasesByAppName(self, pieces):
        found = self.GUI.getCanvasesByAppName(pieces['name'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getCanvasesByAppDetails(self, pieces):
        found = self.GUI.getCanvasesByAppDetails(pieces['name'], pieces['number'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def becomeCanvasAdmin(self, pieces):
        test = self.GUI.becomeCanvasAdmin(pieces['canvasNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    def stopBeingCanvasAdmin(self, pieces):
        test = self.GUI.stopBeingCanvasAdmin(pieces['canvasNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    def subscribeToElement(self, pieces):
        self.GUI.subscribeToElement(pieces['IDapp'] + "," + pieces['IDinstance'], pieces['elementNo'])
        return {}

    def getElementID(self, pieces):
        ID = self.GUI.getElementID(pieces['elementNo'])
        return {"ID": ID}

    def setElementID(self, pieces):
        self.GUI.setElementID(pieces['elementNo'], pieces['ID'])
        return {}

    def getElementOwner(self, pieces):
        owner = self.GUI.getElementOwner(pieces['elementNo'])
        return {"owner": owner}

    def getElementAppDetails(self, pieces):
        app = self.GUI.getElementAppDetails(pieces['elementNo'])
        return {"app": app[0], "instance": app[1]}

    def getElementsByID(self, pieces):
        found = self.GUI.getElementsByID(pieces['ID'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getElementsByOwner(self, pieces):
        found = self.GUI.getElementsByOwner(pieces['owner'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getElementsByAppName(self, pieces):
        found = self.GUI.getElementsByAppName(pieces['name'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getElementsByAppDetails(self, pieces):
        found = self.GUI.getElementsByAppDetails(pieces['name'], pieces['number'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def getElementsOnCanvas(self, pieces):
        found = self.GUI.getElements(pieces['canvasNo'])
        dict = {}
        dict["count"] = len(found)
        for x in range(0, len(found)):
            dict[x] = found[x]
        return dict

    def becomeElementAdmin(self, pieces):
        test = self.GUI.becomeElementAdmin(pieces['elementNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    def stopBeingElementAdmin(self, pieces):
        test = self.GUI.stopBeingElementAdmin(pieces['elementNo'], pieces['IDapp'], pieces['IDinstance'])
        if (test == True):
            return {}
        else:
            return {"error": 7}

    def moveCursor(self, pieces):
        self.GUI.moveCursor(pieces['cursorNo'], pieces['xDist'], pieces['yDist'])
        return {}

    def testMoveCursor(self, pieces):
        loc = self.GUI.testMoveCursor(pieces['cursorNo'], pieces['xDist'], pieces['yDist'])
        return {'x': loc[0], 'y': loc[1]}

    def relocateCursor(self, pieces):
        self.GUI.setCursorPos(pieces['cursorNo'], pieces['x'], pieces['y'], pieces['coorSys'], pieces['surfaceNo'])
        return {}

    def getCursorPosition(self, pieces):
        loc = self.GUI.getCursorPos(pieces['cursorNo'])
        return {"x": loc[0], "y": loc[1]}

    def rotateCursorClockwise(self, pieces):
        self.GUI.rotateCursorClockwise(pieces['cursorNo'], pieces['degrees'])
        return {}

    def rotateCursorAnticlockwise(self, pieces):
        self.GUI.rotateCursorAnticlockwise(pieces['cursorNo'], pieces['degrees'])
        return {}

    def getCursorRotation(self, pieces):
        rot = self.GUI.getCursorRotation(pieces['cursorNo'])
        return {"rotation": rot}

    def getCursorMode(self, pieces):
        mode = self.GUI.getCursorMode(pieces['cursorNo'])
        return {"mode": mode}

    def setCursorDefaultMode(self, pieces):
        self.GUI.setCursorDefaultMode(pieces['cursorNo'])
        return {}

    def setCursorWallMode(self, pieces):
        self.GUI.setCursorWallMode(pieces['cursorNo'])
        return {}

    def setCursorBlockMode(self, pieces):
        self.GUI.setCursorBlockMode(pieces['cursorNo'])
        return {}

    def setCursorScreenMode(self, pieces):
        self.GUI.setCursorScreenMode(pieces['cursorNo'])
        return {}

    def showCursor(self, pieces):
        self.GUI.showCursor(pieces['cursorNo'])
        return {}

    def hideCursor(self, pieces):
        self.GUI.hideCursor(pieces['cursorNo'])
        return {}

    def isCursorVisible(self, pieces):
        visibility = self.GUI.isCursorVisible(pieces['cursorNo'])
        return {"visibility": visibility}

    def moveCanvas(self, pieces):
        self.GUI.moveCanvas(pieces['canvasNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def relocateCanvas(self, pieces):
        self.GUI.setCanvasPos(pieces['canvasNo'], pieces['x'], pieces['y'], pieces['coorSys'], pieces['surfaceNo'])
        return {}

    def setCanvasWidth(self, pieces):
        self.GUI.setCanvasWidth(pieces['canvasNo'], pieces['width'], pieces['coorSys'])
        return {}

    def setCanvasHeight(self, pieces):
        self.GUI.setCanvasHeight(pieces['canvasNo'], pieces['height'], pieces['coorSys'])
        return {}

    def getCanvasPosition(self, pieces):
        loc = self.GUI.getCanvasPos(pieces['canvasNo'])
        return {"x": loc[0], "y": loc[1]}

    def getCanvasWidth(self, pieces):
        width = self.GUI.getCanvasWidth(pieces['canvasNo'])
        return {"width": width}

    def getCanvasHeight(self, pieces):
        height = self.GUI.getCanvasHeight(pieces['canvasNo'])
        return {"height": height}

    def stretchCanvasDown(self, pieces):
        self.GUI.stretchCanvasDown(pieces['canvasNo'], pieces['distance'], pieces['coorSys'])
        return {}

    def stretchCanvasUp(self, pieces):
        self.GUI.stretchCanvasUp(pieces['canvasNo'], pieces['distance'], pieces['coorSys'])
        return {}

    def stretchCanvasLeft(self, pieces):
        self.GUI.stretchCanvasLeft(pieces['canvasNo'], pieces['distance'], pieces['coorSys'])
        return {}

    def stretchCanvasRight(self, pieces):
        self.GUI.stretchCanvasRight(pieces['canvasNo'], pieces['distance'], pieces['coorSys'])
        return {}

    def setCanvasName(self, pieces):
        self.GUI.setCanvasName(pieces['canvasNo'], pieces['name'])
        return {}

    def getCanvasName(self, pieces):
        name = self.GUI.getCanvasName(pieces['canvasNo'])
        return {"name": name}

    def relocateCircle(self, pieces):
        name = self.GUI.setCirclePos(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'],
                                     pieces['canvasNo'])
        x,y = int(pieces['x']), int(pieces['y'])
        print str(self.elements[pieces['elementNo']].pos)
        self.elements[pieces['elementNo']].pos = (x,y)
        return {}

    def getCirclePosition(self, pieces):
        loc = self.GUI.getCirclePos(pieces['elementNo'])
        return {"x": loc[0], "y": loc[1]}

    def getElementType(self, pieces):
        type = self.GUI.getEleType(pieces['elementNo'])
        return {"type": type}

    def setCircleLineColor(self, pieces):
        self.GUI.setCircleLine(pieces['elementNo'], pieces['color'])
        return {}

    def setCircleLineWidth(self, pieces):
        self.GUI.setCircleLineWidth(pieces['elementNo'], pieces['width'])
        return {}

    def setCircleFillColor(self, pieces):
        self.GUI.setCircleFill(pieces['elementNo'], pieces['color'])
        return {}

    def getCircleLineColor(self, pieces):
        color = self.GUI.getCircleLine(pieces['elementNo'])
        return {"color": color}

    def getCircleLineWidth(self, pieces):
        width = self.GUI.getCircleLineWidth(pieces['elementNo'])
        return {"width": width}

    def getCircleFillColor(self, pieces):
        color = self.GUI.getCircleFill(pieces['elementNo'])
        return {"color": color}

    def getCircleRadius(self, pieces):
        radius = self.GUI.getCircleRad(pieces['elementNo'])
        return {"radius": radius}

    def setCircleRadius(self, pieces):
        self.GUI.setCircleRad(pieces['elementNo'], pieces['radius'], pieces['coorSys'])
        return {}

    def getCircleSides(self, pieces):
        sides = self.GUI.getCircleSides(pieces['elementNo'])
        return {"sides": sides}

    def setCircleSides(self, pieces):
        self.GUI.setCircleSides(pieces['elementNo'], pieces['sides'])
        return {}

    def shiftLine(self, pieces):
        self.GUI.shiftLine(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def relocateLine(self, pieces):
        self.GUI.relocateLine(pieces['elementNo'], pieces['refPoint'], pieces['x'], pieces['y'], pieces['coorSys'],
                              pieces['canvasNo'])
        return {}

    def getLineStart(self, pieces):
        loc = self.GUI.getLineStart(pieces['elementNo'])
        return {"x": loc[0], "y": loc[1]}

    def getLineEnd(self, pieces):
        loc = self.GUI.getLineEnd(pieces['elementNo'])
        return {"x": loc[0], "y": loc[1]}

    def setLineStart(self, pieces):
        self.GUI.setLineStart(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'])
        return {}

    def setLineEnd(self, pieces):
        self.GUI.setLineEnd(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'])
        return {}

    def setLineColor(self, pieces):
        self.GUI.setLineColor(pieces['elementNo'], pieces['color'])
        return {}

    def getLineColor(self, pieces):
        color = self.GUI.getLineColor(pieces['elementNo'])
        return {"color": color}

    def getLineWidth(self, pieces):
        width = self.GUI.getLineWidth(pieces['elementNo'])
        return {"width": width}

    def setLineWidth(self, pieces):
        self.GUI.setLineWidth(pieces['elementNo'], pieces['width'])

    def shiftLineStrip(self, pieces):
        self.GUI.shiftLineStrip(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def relocateLineStrip(self, pieces):
        self.GUI.relocateLineStrip(pieces['elementNo'], pieces['refPoint'], pieces['x'], pieces['y'], pieces['coorSys'],
                                   pieces['canvasNo'])
        return {}

    def addLineStripPoint(self, pieces):
        self.GUI.addLineStripPoint(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'])
        return {}

    def addLineStripPointAt(self, pieces):
        self.GUI.addLineStripPointAt(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'], pieces['index'])
        return {}

    def getLineStripPoint(self, pieces):
        loc = self.GUI.getLineStripPoint(pieces['elementNo'], pieces['index'])
        return {"x": loc[0], "y": loc[1]}

    def moveLineStripPoint(self, pieces):
        self.GUI.moveLineStripPoint(int(pieces['elementNo']), int(pieces['pointNo']), float(pieces['x']),
                                    float(pieces['y']), pieces['coorSys'])
        return {}

    def getLineStripColor(self, pieces):
        color = self.GUI.getLineStripColor(pieces['elementNo'])
        return {"color": color}

    def setLineStripColor(self, pieces):
        self.GUI.setLineStripColor(pieces['elementNo'], pieces['color'])
        return {}

    def getLineStripWidth(self, pieces):
        width = self.GUI.getLineStripWidth(pieces['elementNo'])
        return {"width": width}

    def setLineStripWidth(self, pieces):
        self.GUI.setLineStripWidth(pieces['elementNo'], pieces['width'])

    def getLineStripPointCount(self, pieces):
        count = self.GUI.getLineStripPointsCount(pieces['elementNo'])
        return {"count": count}

    def setLineStripContent(self, pieces):
        self.GUI.setLineStripContent(pieces['elementNo'], pieces['content'])
        return {}

    def shiftPolygon(self, pieces):
        self.GUI.shiftPolygon(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def relocatePolygon(self, pieces):
        self.GUI.relocatePolygon(pieces['elementNo'], pieces['refPoint'], pieces['x'], pieces['y'], pieces['coorSys'],
                                 pieces['canvasNo'])
        return {}

    def addPolygonPoint(self, pieces):
        self.GUI.addPolygonPoint(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'])
        return {}

    def getPolygonPoint(self, pieces):
        loc = self.GUI.getPolygonPoint(pieces['elementNo'], pieces['index'])
        return {"x": loc[0], "y": loc[1]}

    def movePolygonPoint(self, pieces):
        self.GUI.movePolygonPoint(pieces['elementNo'], pieces['index'], pieces['x'], pieces['y'], pieces['coorSys'])
        return {}

    def getPolygonFillColor(self, pieces):
        color = self.GUI.getPolygonFillColor(pieces['elementNo'])
        return {"color": color}

    def setPolygonFillColor(self, pieces):
        self.GUI.setPolygonFillColor(pieces['elementNo'], pieces['color'])
        return {}

    def getPolygonLineColor(self, pieces):
        color = self.GUI.getPolygonLineColor(pieces['elementNo'])
        return {"color": color}

    def getPolygonLineWidth(self, pieces):
        width = self.GUI.getPolygonLineWidth(pieces['elementNo'])
        return {"width": width}

    def setPolygonLineColor(self, pieces):
        self.GUI.setPolygonLineColor(pieces['elementNo'], pieces['color'])
        return {}

    def setPolygonLineWidth(self, pieces):
        self.GUI.setPolygonLineWidth(pieces['elementNo'], pieces['width'])
        return {}

    def getPolygonPointCount(self, pieces):
        count = self.GUI.getPolygonPointsCount(pieces['elementNo'])
        return {"count": count}

    def shiftRectangle(self, pieces):
        self.GUI.shiftRectangle(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def setRectangleTopLeft(self, pieces):
        count = self.GUI.setRectangleTopLeft(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'],
                                             pieces['canvasNo'])
        return {}

    def getRectangleTopLeft(self, pieces):
        loc = self.GUI.getRectangleTopLeft(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getRectangleTopRight(self, pieces):
        loc = self.GUI.getRectangleTopRight(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getRectangleBottomRight(self, pieces):
        loc = self.GUI.getRectangleBottomRight(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getRectangleBottomLeft(self, pieces):
        loc = self.GUI.getRectangleBottomLeft(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def setRectangleWidth(self, pieces):
        self.GUI.setRectangleWidth(pieces['elementNo'], pieces['width'], pieces['coorSys'])
        return {}

    def getRectangleWidth(self, pieces):
        width = self.GUI.getRectangleWidth(pieces['elementNo'])
        return {'width': width}

    def setRectangleHeight(self, pieces):
        self.GUI.setRectangleHeight(pieces['elementNo'], pieces['height'], pieces['coorSys'])
        return {}

    def getRectangleHeight(self, pieces):
        height = self.GUI.getRectangleHeight(pieces['elementNo'])
        return {'height': height}

    def getRectangleFillColor(self, pieces):
        color = self.GUI.getRectangleFillColor(pieces['elementNo'])
        return {'color': color}

    def setRectangleFillColor(self, pieces):
        self.GUI.setRectangleFillColor(pieces['elementNo'], pieces['color'])
        return {}

    def getRectangleLineColor(self, pieces):
        color = self.GUI.getRectangleLineColor(pieces['elementNo'])
        return {'color': color}

    def getRectangleLineWidth(self, pieces):
        width = self.GUI.getRectangleLineWidth(pieces['elementNo'])
        return {'width': width}

    def setRectangleLineColor(self, pieces):
        self.GUI.setRectangleLineColor(pieces['elementNo'], pieces['color'])
        return {}

    def setRectangleLineWidth(self, pieces):
        self.GUI.setRectangleLineWidth(pieces['elementNo'], pieces['width'])

    def shiftTexRectangle(self, pieces):
        print "HIYA!"
        self.GUI.shiftTexRectangle(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        xdist,ydist = int(pieces['xDist']), int(pieces['yDist'])
        print str(self.elements[pieces['elementNo']].pos)
        orig = self.elements[pieces['elementNo']].pos
        self.elements[pieces['elementNo']].pos = (orig[0]+xdist,orig[1]+ydist)
        return {}

    def setTexRectangleTopLeft(self, pieces):
        count = self.GUI.setTexRectangleTopLeft(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'],
                                                pieces['canvasNo'])
        return {}

    def getTexRectangleTopLeft(self, pieces):
        loc = self.GUI.getTexRectangleTopLeft(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getTexRectangleTopRight(self, pieces):
        loc = self.GUI.getTexRectangleTopRight(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getTexRectangleBottomRight(self, pieces):
        loc = self.GUI.getTexRectangleBottomRight(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def getTexRectangleBottomLeft(self, pieces):
        loc = self.GUI.getTexRectangleBottomLeft(pieces['elementNo'])
        return {'x': loc[0], 'y': loc[1]}

    def setTexRectangleTexture(self, pieces):
        self.GUI.setTexRectangleTexture(pieces['elementNo'], pieces['imageID'])

    def getTexRectangleTexture(self, pieces):
        tex = self.GUI.getTexRectangleTexture(pieces['elementNo'])
        return {'texture': tex}

    def setTexRectangleWidth(self, pieces):
        self.GUI.setTexRectangleWidth(pieces['elementNo'], pieces['width'], pieces['coorSys'])
        return {}

    def getTexRectangleWidth(self, pieces):
        width = self.GUI.getTexRectangleWidth(pieces['elementNo'])
        return {'width': width}

    def setTexRectangleHeight(self, pieces):
        self.GUI.setTexRectangleHeight(pieces['elementNo'], pieces['height'], pieces['coorSys'])
        return {}

    def getTexRectangleHeight(self, pieces):
        width = self.GUI.getTexRectangleHeight(pieces['elementNo'])
        return {'width': width}

    def setText(self, pieces):
        self.GUI.setText(pieces['elementNo'], pieces['text'])
        return {}

    def getText(self, pieces):
        text = self.GUI.getText(pieces['elementNo'])
        return {'text': text}

    def shiftText(self, pieces):
        self.GUI.shiftText(pieces['elementNo'], pieces['xDist'], pieces['yDist'], pieces['coorSys'])
        return {}

    def setTextPos(self, pieces):
        self.GUI.setTextPos(pieces['elementNo'], pieces['x'], pieces['y'], pieces['coorSys'], pieces['canvasNo'])
        return {}

    def getTextPos(self, pieces):
        loc = self.GUI.getTextPos(pieces['elementNo'])
        return {"x": loc[0], "y": loc[1]}

    def getTextWidth(self, pieces):
        font = self.fonts[pieces['font']]
        text = FTGL.PolygonFont("fonts/" + font + ".ttf")
        text.FaceSize(int(pieces['pt']))
        width = text.Advance(pieces['text'].encode('utf8'))
        return {"width": int(width)}

    def getTextHeight(self, pieces):
        font = self.fonts[pieces['font']]
        text = FTGL.PolygonFont("fonts/" + font + ".ttf")
        text.FaceSize(int(pieces['pt']))
        box = text.BBox(pieces['text'].encode('utf8'))
        height = box[4] - box[1]
        return {"height": int(height)}

    def getTextLineHeight(self, pieces):
        font = self.fonts[pieces['font']]
        text = FTGL.PolygonFont("fonts/" + font + ".ttf")
        text.FaceSize(int(pieces['pt']))
        height = text.line_height
        return {"height": int(height)}

    def getTextDescenderHeight(self, pieces):
        font = self.fonts[pieces['font']]
        text = FTGL.PolygonFont("fonts/" + font + ".ttf")
        text.FaceSize(int(pieces['pt']))
        height = text.descender
        return {"height": int(-height)}

    def setPointSize(self, pieces):
        self.GUI.setPtSize(pieces['elementNo'], pieces['pt'])
        return {}

    def getPointSize(self, pieces):
        size = self.GUI.getPtSize(pieces['elementNo'])
        return {"size": size}

    def getTextFont(self, pieces):
        font = self.GUI.getFont(pieces['elementNo'])
        return {"font": font}

    def setTextFont(self, pieces):
        self.GUI.setFont(pieces['elementNo'], pieces['font'])
        return {}

    def getTextColor(self, pieces):
        color = self.GUI.getTextColor(pieces['elementNo'])
        return {"color": color}

    def setTextColor(self, pieces):
        self.GUI.setTextColor(pieces['elementNo'], pieces['color'])
        return {}

    def showElement(self, pieces):
        self.GUI.showElement(pieces['elementNo'])
        return {}

    def hideElement(self, pieces):
        self.GUI.hideElement(pieces['elementNo'])
        return {}

    def checkElementVisibility(self, pieces):
        visible = self.GUI.checkElementVisibility(pieces['elementNo'])
        return {"visible": visible}

    def hideSetupSurface(self, pieces):
        self.GUI.hideSetupSurface()
        return {}

    def showSetupSurface(self, pieces):
        self.GUI.showSetupSurface()
        return {}

    def getSetupSurfaceVisibility(self, pieces):
        visible = self.GUI.getSetupSurfaceVisibilty()
        return {"visible": visible}

    def getClickedElements(self, pieces):
        elements = self.GUI.getClickedElements(pieces['surfaceNo'], pieces['x'], pieces['y'])
        dict = {}
        dict["count"] = len(elements)
        for x in range(0, len(elements)):
            dict[str(x)] = elements[x]
        return dict

    def removeElement(self, pieces):
        self.GUI.removeElement(pieces['elementNo'], pieces['canvasNo'])
        return {}

    # A dict used so that the program can check which function to call for each API command, and to tell the program how many arguments should be expected
    messages = {'new_surface': (newSurface, 0),  # No parameters
                'new_surface_with_ID': (newSurfaceWithID, 1),
                'new_cursor': (newCursor, 4),  # [1]=SurfaceNo  [2]=x  [3]=y
                'new_cursor_with_ID': (newCursorWithID, 5),  # [1]=ID [2]=SurfaceNo  [3]=x  [4]=y
                'new_canvas': (newCanvas, 7),  # [1]=SurfaceNo  [2]=x  [3]=y  [4]=width  [5]=height  [6]=name
                'new_canvas_with_ID': (newCanvasWithID, 8),
                'new_circle': (newCircle, 9),  # [1]=CanvasNo  [2]=x  [3]=y  [4]=Radius  [5]=LineColor  [6]=FillColor
                'new_circle_with_ID': (newCircleWithID, 10),
                'new_line': (newLine, 8),  # [1]=CanvasNo  [2]=xStart  [3]=yStart  [4]=xEnd  [5]=yEnd  [6]=Color
                'new_line_with_ID': (newLineWithID, 9),
                'new_line_strip': (newLineStrip, 6),  # [1]=CanvasNo  [2]=x  [3]=y  [4]=Color
                'new_line_strip_with_ID': (newLineStripWithID, 7),
                'new_polygon': (newPolygon, 7),  # [1]=CanvasNo  [2]=x  [3]=y  [4]=LineColor  [5]=FillColor
                'new_polygon_with_ID': (newPolygonWithID, 8),
                'new_rectangle': (newRectangle, 9),
                'new_rectangle_with_ID': (newRectangleWithID, 10),
                'new_texrectangle': (newTexRectangle, 9),
                'new_texrectangle_with_ID': (newTexRectangleWithID, 10),
                'new_text': (newText, 8),  # [1]=CanvasNo  [2]=text  [3]=x  [4]=y  [5]=PointSize  [6]=Font  [7]=Color
                'new_text_with_ID': (newTextWithID, 9),
                'subscribe_to_surface': (subscribeToSurface, 1),
                'get_surface_ID': (getSurfaceID, 1),
                'set_surface_ID': (setSurfaceID, 2),
                'get_surface_owner': (getSurfaceOwner, 1),
                'get_surface_app_details': (getSurfaceAppDetails, 1),
                'get_surfaces_by_ID': (getSurfacesByID, 1),
                'get_surfaces_by_owner': (getSurfacesByOwner, 1),
                'get_surfaces_by_app_name': (getSurfacesByAppName, 1),
                'get_surfaces_by_app_details': (getSurfacesByAppDetails, 2),
                'become_surface_admin': (becomeSurfaceAdmin, 1),
                'stop_being_surface_admin': (stopBeingSurfaceAdmin, 1),
                'set_surface_edges': (setSurfaceEdges, 5),
                'undefine_surface': (undefineSurface, 1),
                'save_defined_surfaces': (saveDefinedSurfaces, 1),
                'load_defined_surfaces': (loadDefinedSurfaces, 1),
                'get_saved_layouts': (getSavedLayouts, 0),
                'get_saved_images': (getSavedImages, 0),
                'get_surface_pixel_width': (getSurfacePixelWidth, 1),
                'get_surface_pixel_height': (getSurfacePixelHeight, 1),
                'set_surface_pixel_width': (setSurfacePixelWidth, 2),
                'set_surface_pixel_height': (setSurfacePixelHeight, 2),
                'get_surface_real_width': (getSurfaceRealWidth, 1),
                'get_surface_real_height': (getSurfaceRealHeight, 1),
                'set_surface_real_width': (setSurfaceRealWidth, 2),
                'set_surface_real_height': (setSurfaceRealHeight, 2),
                'clear_surface': (clearSurface, 1),
                'delete_layout': (deleteLayout, 1),
                'delete_image': (deleteImage, 1),
                'rotate_surface_to_0': (rotateSurfaceTo0, 1),
                'rotate_surface_to_90': (rotateSurfaceTo90, 1),
                'rotate_surface_to_180': (rotateSurfaceTo180, 1),
                'rotate_surface_to_270': (rotateSurfaceTo270, 1),
                'mirror_surface': (mirrorSurface, 1),
                'connect_surfaces': (connectSurfaces, 4),
                'disconnect_surfaces': (disconnectSurfaces, 4),
                'subscribe_to_canvas': (subscribeToCanvas, 1),
                'get_canvas_ID': (getCanvasID, 1),
                'set_canvas_ID': (setCanvasID, 2),
                'get_canvas_owner': (getCanvasOwner, 1),
                'get_canvas_app_details': (getCanvasAppDetails, 1),
                'get_canvases_by_ID': (getCanvasesByID, 1),
                'get_canvases_by_owner': (getCanvasesByOwner, 1),
                'get_canvases_by_app_name': (getCanvasesByAppName, 1),
                'get_canvases_by_app_details': (getCanvasesByAppDetails, 2),
                'become_canvas_admin': (becomeCanvasAdmin, 1),
                'stop_being_canvas_admin': (stopBeingCanvasAdmin, 1),
                'subscribe_to_element': (subscribeToElement, 1),
                'get_element_ID': (getElementID, 1),
                'set_element_ID': (setElementID, 2),
                'get_element_owner': (getElementOwner, 1),
                'get_element_app_details': (getElementAppDetails, 1),
                'get_elements_by_ID': (getElementsByID, 1),
                'get_elements_by_owner': (getElementsByOwner, 1),
                'get_elements_by_app_name': (getElementsByAppName, 1),
                'get_elements_by_app_details': (getElementsByAppDetails, 2),
                'get_elements_on_canvas': (getElementsOnCanvas, 1),
                'become_element_admin': (becomeElementAdmin, 1),
                'stop_being_element_admin': (stopBeingElementAdmin, 1),
                'move_cursor': (moveCursor, 3),  # [1]=CursorNo  [2]=xDistance  [3]=yDistance
                'test_move_cursor': (testMoveCursor, 3),  # [1]=CursorNo  [2]=xDistance  [3]=yDistance
                'relocate_cursor': (relocateCursor, 5),  # [1]=CursorNo  [2]=x  [3]=y  [4]=Surface
                'get_cursor_pos': (getCursorPosition, 1),  # [1]=CursorNo
                'rotate_cursor_clockwise': (rotateCursorClockwise, 2),  # [1]=CursorNo [2]=Degrees
                'rotate_cursor_anticlockwise': (rotateCursorAnticlockwise, 2),  # [1]=CursorNo [2]=Degrees
                'get_cursor_rotation': (getCursorRotation, 1),  # [1]=CursorNo
                'get_cursor_mode': (getCursorMode, 1),
                'set_cursor_default_mode': (setCursorDefaultMode, 1),
                'set_cursor_wall_mode': (setCursorWallMode, 1),
                'set_cursor_block_mode': (setCursorBlockMode, 1),
                'set_cursor_screen_mode': (setCursorScreenMode, 1),
                'show_cursor': (showCursor, 1),
                'hide_cursor': (hideCursor, 1),
                'is_cursor_visible': (isCursorVisible, 1),
                'move_canvas': (moveCanvas, 4),  # [1]=CanvasNo  [2]=xDistance  [3]=yDistance  [4]=coorSys
                'relocate_canvas': (relocateCanvas, 5),  # [1]=CanvasNo  [2]=x  [3]=y  [4]=coorSys  [5]=Surface
                'set_canvas_width': (setCanvasWidth, 3),  # [1]=CanvasNo  [2]=Width  [3]=coorSys
                'set_canvas_height': (setCanvasHeight, 3),  # [1]=CanvasNo  [2]=Height  [3]=coorSys
                'get_canvas_pos': (getCanvasPosition, 1),  # [1]=CanvasNo
                'get_canvas_width': (getCanvasWidth, 1),  # [1]=CanvasNo
                'get_canvas_height': (getCanvasHeight, 1),  # [1]=CanvasNo
                'stretch_canvas_down': (stretchCanvasDown, 3),  # [1]=CanvasNo  [2]=Distance  [3]=coorSys
                'stretch_canvas_up': (stretchCanvasUp, 3),  # [1]=CanvasNo  [2]=Distance  [3]=coorSys
                'stretch_canvas_left': (stretchCanvasLeft, 2),  # [1]=CanvasNo  [2]=Distance  [3]=coorSys
                'stretch_canvas_right': (stretchCanvasRight, 2),  # [1]=CanvasNo  [2]=Distance  [3]=coorSys
                'set_canvas_name': (setCanvasName, 2),  # [1]=CanvasNo  [2]=Name
                'get_canvas_name': (getCanvasName, 1),  # [1]=CanvasNo
                'relocate_circle': (relocateCircle, 5),  # [1]=ElementNo  [2]=x  [3]=y [4]=coorSys [5]=canvasNo
                'get_circle_pos': (getCirclePosition, 1),  # [1]=ElementNo
                'get_element_type': (getElementType, 1),  # [1]=ElementNo
                'set_circle_line_color': (setCircleLineColor, 2),  # [1]=ElementNo  [2]=Color
                'set_circle_line_width': (setCircleLineWidth, 2),  # [1]=ElementNo  [2]=Width
                'set_circle_fill_color': (setCircleFillColor, 2),  # [1]=ElementNo  [2]=Color
                'get_circle_line_color': (getCircleLineColor, 1),  # [1]=ElementNo
                'get_circle_line_width': (getCircleLineWidth, 1),  # [1]=ElementNo
                'get_circle_fill_color': (getCircleFillColor, 1),  # [1]=ElementNo
                'set_circle_radius': (setCircleRadius, 3),  # [1]=ElementNo  [2]=Radius  [3]=coorSys
                'get_circle_radius': (getCircleRadius, 1),  # [1]=ElementNo
                'set_circle_sides': (setCircleSides, 2),
                'get_circle_sides': (getCircleSides, 1),
                'shift_line': (shiftLine, 4),
                'relocate_line': (relocateLine, 6),
                'get_line_start': (getLineStart, 1),  # [1]=ElementNo
                'get_line_end': (getLineEnd, 1),  # [1]=ElementNo
                'relocate_line_start': (setLineStart, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=coorSys
                'relocate_line_end': (setLineEnd, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=coorSys
                'set_line_color': (setLineColor, 2),  # [1]=ElementNo  [2]=Color
                'get_line_color': (getLineColor, 1),  # [1]=ElementNo
                'set_line_width': (setLineWidth, 2),
                'get_line_width': (getLineWidth, 1),
                'shift_line_strip': (shiftLineStrip, 4),
                'relocate_line_strip': (relocateLineStrip, 6),
                'add_line_strip_point': (addLineStripPoint, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=coorSys
                'add_line_strip_point_at': (addLineStripPointAt, 5),  # [1]=ElementNo [2]=x [3]=y [4]=coorSys [5]=index
                'get_line_strip_point': (getLineStripPoint, 2),  # [1]=ElementNo  [2]=PointNo
                'relocate_line_strip_point': (moveLineStripPoint, 5),
                # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y [5]=coorSys
                'get_line_strip_color': (getLineStripColor, 1),  # [1]=ElementNo
                'set_line_strip_color': (setLineStripColor, 2),  # [1]=ElementNo  [2]=Color
                'get_line_strip_width': (getLineStripWidth, 1),
                'set_line_strip_width': (getLineStripWidth, 2),
                'get_line_strip_point_count': (getLineStripPointCount, 1),  # [1]=ElementNo
                'set_line_strip_content': (setLineStripContent, 2),
                'shift_polygon': (shiftPolygon, 4),
                'relocate_polygon': (relocatePolygon, 6),
                'add_polygon_point': (addPolygonPoint, 4),  # [1]=ElementNo  [2]=x  [3]=y  [4]=coorSys
                'get_polygon_point': (getPolygonPoint, 2),  # [1]=ElementNo  [2]=PointNo
                'relocate_polygon_point': (movePolygonPoint, 5),
                # [1]=ElementNo  [2]=PointNo  [3]=x  [4]=y  [5]=coorSys
                'get_polygon_fill_color': (getPolygonFillColor, 1),  # [1]=ElementNo
                'set_polygon_fill_color': (setPolygonFillColor, 2),  # [1]=ElementNo  [2]=Color
                'get_polygon_line_color': (getPolygonLineColor, 1),  # [1]=ElementNo
                'get_polygon_line_width': (getPolygonLineWidth, 1),  # [1]=ElementNo
                'set_polygon_line_color': (setPolygonLineColor, 2),  # [1]=ElementNo  [2]=Color
                'set_polygon_line_width': (setPolygonLineWidth, 2),  # [1]=ElementNo  [2]=Width
                'get_polygon_point_count': (getPolygonPointCount, 1),  # [1]=ElementNo
                'shift_rectangle': (shiftRectangle, 4),
                'set_rectangle_top_left': (setRectangleTopLeft, 5),
                'get_rectangle_top_left': (getRectangleTopLeft, 1),
                'get_rectangle_top_right': (getRectangleTopRight, 1),
                'get_rectangle_bottom_right': (getRectangleBottomRight, 1),
                'get_rectangle_bottom_left': (getRectangleBottomLeft, 1),
                'set_rectangle_width': (setRectangleWidth, 3),
                'get_rectangle_width': (getRectangleWidth, 1),
                'set_rectangle_height': (setRectangleHeight, 3),
                'get_rectangle_height': (getRectangleHeight, 1),
                'get_rectangle_fill_color': (getRectangleFillColor, 1),
                'set_rectangle_fill_color': (setRectangleFillColor, 2),
                'get_rectangle_line_color': (getRectangleLineColor, 1),
                'get_rectangle_line_width': (getRectangleLineWidth, 1),
                'set_rectangle_line_color': (setRectangleLineColor, 2),
                'set_rectangle_line_width': (setRectangleLineWidth, 2),
                'shift_texrectangle': (shiftRectangle, 4),
                'set_texrectangle_top_left': (setTexRectangleTopLeft, 5),
                'get_texrectangle_top_left': (getTexRectangleTopLeft, 1),
                'get_texrectangle_top_right': (getTexRectangleTopRight, 1),
                'get_texrectangle_bottom_right': (getTexRectangleBottomRight, 1),
                'get_texrectangle_bottom_left': (getTexRectangleBottomLeft, 1),
                'set_texrectangle_texture': (setTexRectangleTexture, 4),
                'get_texrectangle_texture': (getTexRectangleTexture, 1),
                'set_texrectangle_width': (setTexRectangleWidth, 3),
                'get_texrectangle_width': (getTexRectangleWidth, 1),
                'set_texrectangle_height': (setTexRectangleHeight, 3),
                'get_texrectangle_height': (getTexRectangleHeight, 1),
                'set_text': (setText, 2),  # [1]=ElementNo  [2]=String
                'get_text': (getText, 1),  # [1]=ElementNo
                'shift_text': (shiftText, 4),
                'relocate_text': (setTextPos, 5),  # [1]=ElementNo  [2]=x  [3]=y  [4]=coorSys  [5]=CanvasNo
                'get_text_pos': (getTextPos, 1),  # [1]=ElementNo
                'get_text_width': (getTextWidth, 3),  # [1]=text  [2]=font  [3]=pt
                'get_text_height': (getTextHeight, 3),  # [1]=text  [2]=font  [3]=pt
                'get_text_line_height': (getTextLineHeight, 2),  # [1]=font  [2]=pt
                'get_text_descender_height': (getTextDescenderHeight, 2),  # [1]=font  [2]=pt
                'set_text_point_size': (setPointSize, 2),  # [1]=ElementNo  [2]=pt
                'get_text_point_size': (getPointSize, 1),  # [1]=ElementNo
                'get_text_font': (getTextFont, 1),  # [1]=ElementNo
                'set_text_font': (setTextFont, 2),  # [1]=ElementNo  [2]=Font
                'set_text_color': (setTextColor, 2),  # [1]=ElementNo  [2]=Color
                'get_text_color': (getTextColor, 1),  # [1]=ElementNo
                'show_element': (showElement, 1),  # [1]=ElementNo
                'hide_element': (hideElement, 1),  # [1]=ElementNo
                'check_element_visibility': (checkElementVisibility, 1),  # [1]=ElementNo
                'hide_setup_surface': (hideSetupSurface, 0),
                'show_setup_surface': (showSetupSurface, 0),
                'get_setup_surface_visibility': (getSetupSurfaceVisibility, 0),
                'get_clicked_elements': (getClickedElements, 3),
                'remove_element': (removeElement, 2)
                }

    # Takes a recieved API message and processes it
    def processMessage(self, msg):
        if (msg == "quit"):
            self.looping = False
        data = None  # Creates an empty variable to hold the message reply
        try:
            if (len(msg) - 4 == self.messages[msg['call']][1]):
                data = self.messages[str(msg['call'])][0](self, msg)
            else:
                data = {"error": 2, "1": str(len(msg) - 1), "2": str(self.messages[msg['call']][1])}
        except KeyError, e:
            data = {"error": 1}
        return data

    # Sends a reply to the client that the last message was received from
    def reply (self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket == sock :
                try :
                    jsonmessage = json.dumps(message)
                    socket.send(jsonmessage)
                except :
                    socket.close()
                    self.CONNECTION_LIST.remove(socket)

    def server_init(self):
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.RECV_BUFFER = parser.getint('connection','RecieveBuffer')
        PORT = parser.getint('connection','port')
        HOST = parser.get('connection','host')

        self.CONNECTION_LIST = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # why is this not working?
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(10)

        self.CONNECTION_LIST.append(self.server_socket)

        print "API server started on port " + str(PORT)

        loop = True

        self.server_started = True
        thread = Thread(target = self.server)
        thread.start()
        self.counter = 0

    def update(self, dt):
        while(len(self.queue)!=0):
            qitem = self.queue.pop()
            appsplit = self.sock2app[qitem[0]].split(',')
            temp = qitem[1]
            temp['IDuser'] = self.sock2usr[qitem[0]]
            temp['IDapp'] = appsplit[0]
            temp['IDinstance'] = appsplit[1]
            if(temp['call'] == "set_rectangle_texture" or temp['call'] == "new_texrectangle" or temp['call'] == "new_texrectangle_with_ID"):
                g = open("images/" + str(self.counter) + "." + str(temp['extension']), "w")
                g.write(base64.decodestring(str(temp['textureData'])))
                g.close()
                temp['imageID'] = self.counter
                self.counter += 1
            #qitem = (qitem[0], json.dumps(temp))
            self.reply(qitem[0], self.processMessage(temp))

    def server(self):
        while(True):
            sleep(0.001)
            try:
                read_sockets = select.select(self.CONNECTION_LIST,[],[])[0] #Wait until ready for IO
                # Loop through all the read sockets
                for sock in read_sockets:
                    if sock == self.server_socket: #If a new client is connecting add it to the connection list
                        sockfd, addr = self.server_socket.accept()
                        self.CONNECTION_LIST.append(sockfd)
                        print "Client (%s, %s) connected" % addr
                    else:
                        try: #Try to receive data and process it
                            recieved = int(sock.recv(10))
                            data = ""
                            while (recieved>0):
                                temp = sock.recv(self.RECV_BUFFER)
                                data += temp
                                recieved -= len(temp)
                            dataJSON = json.loads(data)
                            if data:
                                if(dataJSON['call'] == 'quit'): #If the received data is a quit command close the socket and exit
                                    print '\033[1;31mShutting down server\033[1;m'
                                    self.processMessage(data)
                                    loop=False
                                elif(dataJSON['call'] == 'login'):
                                    if(self.sock2usr.has_key(sock)==False):
                                        self.sock2usr[sock] = dataJSON['username']
                                        self.reply(sock,str({}))
                                    else:
                                        self.reply(sock,str({'error' : 4}))
                                elif(dataJSON['call'] == 'setapp'):
                                    if(self.sock2app.has_key(sock)):
                                        self.reply(sock,str({'error' : 5}))
                                    else:
                                        count = 0
                                        added = False
                                        while(added==False):
                                            if(self.app2sock.has_key(dataJSON['appname'] + "," + str(count))==False):
                                                self.app2sock[dataJSON['appname'] + "," + str(count)] = sock
                                                self.sock2app[sock] = dataJSON['appname'] + "," + str(count)
                                                self.reply(sock,str({}))
                                                added = True
                                            else:
                                                count += 1
                                else: #If the message isn't a quit command puts the received API message onto the queue to be processed
                                    if(self.sock2usr.has_key(sock) and self.sock2app.has_key(sock)):
                                        self.queue.appendleft((sock,dataJSON))
                                    else:
                                        if(self.sock2usr.has_key(sock)==False):
                                            self.reply(sock,str({'error' : 3}))
                                        else:
                                            self.reply(sock,str({'error' : 6}))
                        except:
                            print "Client (%s, %s) is offline" % addr
                            sock.close()
                            self.CONNECTION_LIST.remove(sock)
                            continue
            except:
                pass

class eventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_texture')
        super(eventDispatcher, self).__init__(**kwargs)

    def on_texture(self, surface, filename, x, y, width, height):
        print "texturing"
        with surface.canvas:
            self.tex = Image.load(filename).texture
            rect = Rectangle(pos=(x,y-height),size=(width,height),texture=self.tex)


# A class which is used to parse API messages and call the relevant actions
class renderApp(App):
    def build(self):
        parent = Widget()
        EventLoop.ensure_window()
        self.dispatcher = eventDispatcher()
        self.r_surf = renderSurface()
        Clock.schedule_interval(self.r_surf.update,1.0/120.0)
        parent.add_widget(self.r_surf)
        return parent

if __name__ == "__main__":
    test = 'images/*'
    r = glob.glob(test)
    for i in r:
        os.remove(i)
    Config.set('graphics', 'width', '1024')
    Config.set('graphics', 'height', '768')
    renderApp().run()