#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, json
from API import apiMessageParser
from collections import deque
import os
import glob
import base64

app = Flask(__name__)
messageParser = None
counter = 0


class processor(object):
    @staticmethod
    def processMessage(message):
        message['IDuser'] = 'webusr'
        message['IDapp'] = 'REST'
        message['IDinstance'] = 0
        reply = messageParser.processMessage(message)
        return jsonify(reply)
    
'''@app.route('/api/login', methods=['POST'])
def login():
    if not request.json or not 'username' in request.json:
        abort(400)
    returnData = processor.processMessage("login," + request.json['username'])
    return returnData

@app.route('/api/setApp', methods=['POST'])
def setApp():
    if not request.json or not 'appName' in request.json:
        abort(400)
    returnData = processor.processMessage("setapp," + request.json['appName'])
    return returnData'''

@app.route('/api/newSurface', methods=['POST'])
def newSurface():
    call = {'call' : 'new_surface'}
    returnData = processor.processMessage(call)
    return returnData
    
@app.route('/api/newSurfaceWithID', methods=['POST'])
def newSurfaceWithID():
    if not request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_surface_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newCursor', methods=['POST'])
def newCursor():
    if not request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newCursorWithID', methods=['POST'])
def newCursorWithID():
    if not request.json or not 'ID' in request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_cursor_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newWindow', methods=['POST'])
def newWindow():
    if not request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_window'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newWindowWithID', methods=['POST'])
def newWindowWithID():
    if not request.json or not 'ID' in request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_window_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newCircle', methods=['POST'])
def newCircle():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'radius' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json or not 'sides' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_circle'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newCircleWithID', methods=['POST'])
def newCircleWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'radius' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json or not 'sides' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_circle_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newLine', methods=['POST'])
def newLine():
    if not request.json or not 'windowNo' in request.json or not 'xStart' in request.json or not 'yStart' in request.json or not 'xEnd' in request.json or not 'yEnd' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_line'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newLineWithID', methods=['POST'])
def newLineWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'xStart' in request.json or not 'yStart' in request.json or not 'xEnd' in request.json or not 'yEnd' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_line_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newLineStrip', methods=['POST'])
def newLineStrip():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_line_strip'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newLineStripWithID', methods=['POST'])
def newLineStripWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_line_strip_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newPolygon', methods=['POST'])
def newPolygon():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_polygon'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newPolygonWithID', methods=['POST'])
def newPolygonWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_polygon_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newRectangle', methods=['POST'])
def newRectangle():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_rectangle'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newRectangleWithID', methods=['POST'])
def newRectangleWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_rectangle_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newTexRectangle', methods=['POST'])
def newTexRectangle():
    global counter
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'textureData' in request.json or not 'extension' in request.json:
        print str(request.json)
        abort(400)
    g = open("images/" + str(counter) + "-rest." + str(request.json['extension']), "w")
    g.write(base64.decodestring(str(request.json['textureData'])))
    g.close()
    dict = json.loads(request.json)
    dict['call'] = 'new_texrectangle'
    dict['imageID'] = counter
    returnData = processor.processMessage(dict)
    counter += 1
    return returnData

@app.route('/api/newTexRectangleWithID', methods=['POST'])
def newTexRectangleWithID():
    global counter
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'textureData' in request.json or not 'extension' in request.json:
        abort(400)
    g = open("images/" + str(counter) + "." + str(request.json['extension']), "w")
    g.write(base64.decodestring(str(request.json['textureData'])))
    g.close()
    dict = json.loads(request.json)
    dict['call'] = 'new_line_with_ID'
    dict['imageID'] = counter
    returnData = processor.processMessage(dict)
    counter += 1
    return returnData

@app.route('/api/newText', methods=['POST'])
def newText():
    if not request.json or not 'windowNo' in request.json or not 'text' in request.json or not 'x' in request.json or not 'y' in request.json or not 'pt' in request.json or not 'font' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_text'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/newTextWithID', methods=['POST'])
def newTextWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'text' in request.json or not 'x' in request.json or not 'y' in request.json or not 'pt' in request.json or not 'font' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'new_text_with_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfaceID', methods=['GET'])
def getSurfaceID():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surface_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setSurfaceID', methods=['POST'])
def setSurfaceID():
    if not request.json or not 'surfaceNo' in request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_surface_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfaceOwner', methods=['GET'])
def getSurfaceOwner():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surface_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfaceAppDetails', methods=['GET'])
def getSurfaceAppDetails():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surface_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacesByID', methods=['GET'])
def getSurfacesByID():
    if not request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surfaces_by_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacesByOwner', methods=['GET'])
def getSurfacesByOwner():
    if not request.json or not 'owner' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surfaces_by_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacesByAppName', methods=['GET'])
def getSurfacesByAppName():
    if not request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surfaces_by_app_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacesByAppDetails', methods=['GET'])
def getSurfacesByAppDetails():
    if not request.json or not 'name' in request.json or not 'number' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surfaces_by_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setSurfaceEdges', methods=['POST'])
def setSurfaceEdges():
    if not request.json or not 'surfaceNo' in request.json or not 'topPoints' in request.json or not 'bottomPoints' in request.json or not 'leftPoints' in request.json or not 'rightPoints' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_surface_edges'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/undefineSurface', methods=['POST'])
def undefineSurface():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'undefine_surface'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/saveDefinedSurfaces', methods=['POST'])
def saveDefinedSurfaces():
    if not request.json or not 'fileName' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'save_defined_surfaces'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/loadDefinedSurfaces', methods=['POST'])
def loadDefinedSurfaces():
    if not request.json or not 'fileName' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'load_defined_surfaces'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSavedLayouts', methods=['GET'])
def getSavedLayouts():
    dict = {'call' : 'get_saved_layouts'}
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSavedImages', methods=['GET'])
def getSavedImages():
    dict = {'call' : 'get_saved_images'}
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setUploadName', methods=['POST'])
def setUploadName():
    if not request.json or not 'fileName' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_upload_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacePixelWidth', methods=['GET'])
def getSurfacePixelWidth():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surface_pixel_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSurfacePixelHeight', methods=['GET'])
def getSurfacePixelHeight():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_surface_pixel_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setSurfacePixelWidth', methods=['POST'])
def setSurfacePixelWidth():
    if not request.json or not 'surfaceNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_surface_pixel_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setSurfacePixelHeight', methods=['POST'])
def setSurfacePixelHeight():
    if not request.json or not 'surfaceNo' in request.json or not 'height' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_surface_pixel_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/clearSurface', methods=['POST'])
def clearSurface():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'clear_surface'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/deleteLayout', methods=['POST'])
def deleteLayout():
    if not request.json or not 'layoutName' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'delete_layout'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/deleteImage', methods=['POST'])
def deleteImage():
    if not request.json or not 'fileName' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'delete_image'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateSurfaceTo0', methods=['POST'])
def rotateSurfaceTo0():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_surface_to_0'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateSurfaceTo90', methods=['POST'])
def rotateSurfaceTo90():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_surface_to_90'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateSurfaceTo180', methods=['POST'])
def rotateSurfaceTo180():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_surface_to_180'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateSurfaceTo270', methods=['POST'])
def rotateSurfaceTo270():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_surface_to_270'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/mirrorSurface', methods=['POST'])
def mirrorSurface():
    if not request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'mirror_surface'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/connectSurfaces', methods=['POST'])
def connectSurfaces():
    if not request.json or not 'surfaceNo1' in request.json or not 'side1' in request.json or not 'surfaceNo2' in request.json or not 'side2' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'connect_surfaces'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/disconnectSurfaces', methods=['POST'])
def disconnectSurfaces():
    if not request.json or not 'surfaceNo1' in request.json or not 'side1' in request.json or not 'surfaceNo2' in request.json or not 'side2' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'disconnect_surfaces'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowID', methods=['GET'])
def getWindowID():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setWindowID', methods=['POST'])
def setWindowID():
    if not request.json or not 'windowNo' in request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_window_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowOwner', methods=['GET'])
def getWindowOwner():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowAppDetails', methods=['GET'])
def getWindowAppDetails():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowsByID', methods=['GET'])
def getWindowsByID():
    if not request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_windows_by_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowsByOwner', methods=['GET'])
def getWindowsByOwner():
    if not request.json or not 'owner' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_windows_by_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowsByAppName', methods=['GET'])
def getWindowsByAppName():
    if not request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_windows_by_app_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowsByAppDetails', methods=['GET'])
def getWindowsByAppDetails():
    if not request.json or not 'name' in request.json or not 'number' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_windows_by_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementID', methods=['GET'])
def getElementID():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_element_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setElementID', methods=['POST'])
def setElementID():
    if not request.json or not 'elementNo' in request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_element_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementOwner', methods=['GET'])
def getElementOwner():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_element_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementAppDetails', methods=['GET'])
def getElementAppDetails():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_element_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementsByID', methods=['GET'])
def getElementsByID():
    if not request.json or not 'ID' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_elements_by_ID'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementsByOwner', methods=['GET'])
def getElementsByOwner():
    if not request.json or not 'owner' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_elements_by_owner'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementsByAppName', methods=['GET'])
def getElementsByAppName():
    if not request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_elements_by_app_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementsByAppDetails', methods=['GET'])
def getElementsByAppDetails():
    if not request.json or not 'name' in request.json or not 'number' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_elements_by_app_details'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementsOnWindow', methods=['GET'])
def getElementsOnWindow():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_elements_on_window'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/moveCursor', methods=['POST'])
def moveCursor():
    if not request.json or not 'cursorNo' in request.json or not 'xDist' in request.json or not 'yDist' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'move_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/testMoveCursor', methods=['GET'])
def testMoveCursor():
    if not request.json or not 'cursorNo' in request.json or not 'xDist' in request.json or not 'yDist' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'test_move_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/relocateCursor', methods=['POST'])
def relocateCursor():
    if not request.json or not 'cursorNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCursorPosition', methods=['GET'])
def getCursorPosition():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_cursor_pos'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateCursorClockwise', methods=['POST'])
def rotateCursorClockwise():
    if not request.json or not 'cursorNo' in request.json or not 'degrees' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_cursor_clockwise'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/rotateCursorAnticlockwise', methods=['POST'])
def rotateCursorAnticlockwise():
    if not request.json or not 'cursorNo' in request.json or not 'degrees' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'rotate_cursor_anticlockwise'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCursorRotation', methods=['GET'])
def getCursorRotation():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_cursor_rotation'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCursorMode', methods=['GET'])
def getCursorMode():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_cursor_mode'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCursorDefaultMode', methods=['POST'])
def setCursorDefaultMode():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_cursor_default_mode'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCursorWallMode', methods=['POST'])
def setCursorWallMode():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_cursor_wall_mode'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCursorBlockMode', methods=['POST'])
def setCursorBlockMode():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_cursor_block_mode'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCursorScreenMode', methods=['POST'])
def setCursorScreenMode():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_cursor_screen_mode'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/showCursor', methods=['POST'])
def showCursor():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'show_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/hideCursor', methods=['POST'])
def hideCursor():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'hide_cursor'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/isCursorVisible', methods=['GET'])
def isCursorVisible():
    if not request.json or not 'cursorNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'is_cursor_visible'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/moveWindow', methods=['POST'])
def moveWindow():
    if not request.json or not 'windowNo' in request.json or not 'xDist' in request.json or not 'yDist' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'move_window'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/relocateWindow', methods=['POST'])
def relocateWindow():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'surfaceNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_window'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setWindowHeight', methods=['POST'])
def setWindowHeight():
    if not request.json or not 'windowNo' in request.json or not 'height' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_window_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setWindowWidth', methods=['POST'])
def setWindowWidth():
    if not request.json or not 'windowNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_window_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowPosition', methods=['GET'])
def getWindowPosition():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_pos'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowHeight', methods=['GET'])
def getWindowHeight():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowWidth', methods=['GET'])
def getWindowWidth():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/stretchWindowDown', methods=['POST'])
def stretchWindowDown():
    if not request.json or not 'windowNo' in request.json or not 'distance' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'stretch_window_down'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/stretchWindowUp', methods=['POST'])
def stretchWindowUp():
    if not request.json or not 'windowNo' in request.json or not 'distance' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'stretch_window_up'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/stretchWindowLeft', methods=['POST'])
def stretchWindowLeft():
    if not request.json or not 'windowNo' in request.json or not 'distance' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'stretch_window_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/stretchWindowRight', methods=['POST'])
def stretchWindowRight():
    if not request.json or not 'windowNo' in request.json or not 'distance' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'stretch_window_right'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setWindowName', methods=['POST'])
def setWindowName():
    if not request.json or not 'windowNo' in request.json or not 'name' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_window_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getWindowName', methods=['GET'])
def getWindowName():
    if not request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_window_name'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/relocateCircle', methods=['POST'])
def relocateCircle():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_circle'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCirclePosition', methods=['GET'])
def getCirclePosition():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_circle_pos'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getElementType', methods=['GET'])
def getElementType():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_element_type'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCircleLineColor', methods=['POST'])
def setCircleLineColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_circle_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCircleFillColor', methods=['POST'])
def setCircleFillColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_circle_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCircleLineColor', methods=['GET'])
def getCircleLineColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_circle_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCircleFillColor', methods=['GET'])
def getCircleFillColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_circle_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCircleRadius', methods=['POST'])
def setCircleRadius():
    if not request.json or not 'elementNo' in request.json or not 'radius' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_circle_radius'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCircleRadius', methods=['GET'])
def getCircleRadius():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_circle_radius'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setCircleSides', methods=['POST'])
def setCircleSides():
    if not request.json or not 'elementNo' in request.json or not 'sides' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_circle_sides'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getCircleSides', methods=['GET'])
def getCircleSides():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_circle_sides'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineStart', methods=['GET'])
def getLineStart():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_start'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineEnd', methods=['GET'])
def getLineEnd():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_end'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineStart', methods=['POST'])
def setLineStart():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_line_start'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineEnd', methods=['POST'])
def setLineEnd():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_line_end'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineColor', methods=['POST'])
def setLineColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineColor', methods=['GET'])
def getLineColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineWidth', methods=['POST'])
def setLineWidth():
    if not request.json or not 'elementNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_line_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineWidth', methods=['GET'])
def getLineWidth():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/addLineStripPoint', methods=['POST'])
def addLineStripPoint():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'add_line_strip_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/addLineStripPointAt', methods=['POST'])
def addLineStripPointAt():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'index' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'add_line_strip_point_at'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineStripPoint', methods=['GET'])
def getLineStripPoint():
    if not request.json or not 'elementNo' in request.json or not 'index' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_strip_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/moveLineStripPoint', methods=['POST'])
def moveLineStripPoint():
    if not request.json or not 'elementNo' in request.json or not 'index' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_line_strip_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineStripColor', methods=['POST'])
def setLineStripColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_line_strip_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineStripColor', methods=['GET'])
def getLineStripColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_strip_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineStripWidth', methods=['POST'])
def setLineStripWidth():
    if not request.json or not 'elementNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_line_strip_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineStripWidth', methods=['GET'])
def getLineStripWidth():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_strip_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getLineStripPointCount', methods=['GET'])
def getLineStripPointCount():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_line_strip_point_count'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setLineStripContent', methods=['POST'])
def setLineStripContent():
    if not request.json or not 'elementNo' in request.json or not 'content' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_line_strip_content'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/addPolygonPoint', methods=['POST'])
def addPolygonPoint():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'add_polygon_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getPolygonPoint', methods=['GET'])
def getPolygonPoint():
    if not request.json or not 'elementNo' in request.json or not 'index' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_polygon_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/movePolygonPoint', methods=['POST'])
def movePolygonPoint():
    if not request.json or not 'elementNo' in request.json or not 'index' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_polygon_point'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setPolygonFillColor', methods=['POST'])
def setPolygonFillColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_polygon_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getPolygonFillColor', methods=['GET'])
def getPolygonFillColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_polygon_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setPolygonLineColor', methods=['POST'])
def setPolygonLineColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_polygon_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getPolygonLineColor', methods=['GET'])
def getPolygonLineColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_polygon_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getPolygonPointCount', methods=['GET'])
def getPolygonPointCount():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_polygon_point_count'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setRectangleTopLeft', methods=['POST'])
def setRectangleTopLeft():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_top_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleTopLeft', methods=['GET'])
def getRectangleTopLeft():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_top_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleTopRight', methods=['GET'])
def getRectangleTopRight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_top_right'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleBottomRight', methods=['GET'])
def getRectangleBottomRight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_bottom_right'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleBottomLeft', methods=['GET'])
def getRectangleBottomLeft():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_bottom_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setRectangleWidth', methods=['POST'])
def setRectangleWidth():
    if not request.json or not 'elementNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleWidth', methods=['GET'])
def getRectangleWidth():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setRectangleHeight', methods=['POST'])
def setRectangleHeight():
    if not request.json or not 'elementNo' in request.json or not 'height' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleHeight', methods=['GET'])
def getRectangleHeight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setRectangleFillColor', methods=['POST'])
def setRectangleFillColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleFillColor', methods=['GET'])
def getRectangleFillColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_fill_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setRectangleLineColor', methods=['POST'])
def setRectangleLineColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getRectangleLineColor', methods=['GET'])
def getRectangleLineColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_rectangle_line_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTexRectangleTopLeft', methods=['POST'])
def setTexRectangleTopLeft():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_texrectangle_top_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleTopLeft', methods=['GET'])
def getTexRectangleTopLeft():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_top_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleTopRight', methods=['GET'])
def getTexRectangleTopRight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_top_right'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleBottomRight', methods=['GET'])
def getTexRectangleBottomRight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_bottom_right'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleBottomLeft', methods=['GET'])
def getTexRectangleBottomLeft():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_bottom_left'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTexRectangleTexture', methods=['POST'])
def setTexRectangleTexture():
    global counter
    if not request.json or not 'elementNo' in request.json or not 'textureData' in request.json or not 'extension' in request.json:
        abort(400)
    g = open("images/" + str(counter) + "." + str(request.json['extension']), "w")
    g.write(base64.decodestring(str(request.json['textureData'])))
    g.close()
    dict = json.loads(request.json)
    dict['call'] = 'set_rectangle_texture'
    dict['imageID'] = counter
    returnData = processor.processMessage(dict)
    counter += 1
    return returnData

@app.route('/api/getTexRectangleTexture', methods=['GET'])
def getTexRectangleTexture():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_texture'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTexRectangleWidth', methods=['POST'])
def setTexRectangleWidth():
    if not request.json or not 'elementNo' in request.json or not 'width' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_textrectangle_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleWidth', methods=['GET'])
def getTexRectangleWidth():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_width'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTexRectangleHeight', methods=['POST'])
def setTexRectangleHeight():
    if not request.json or not 'elementNo' in request.json or not 'height' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_texrectangle_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTexRectangleHeight', methods=['GET'])
def getTexRectangleHeight():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_texrectangle_height'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setText', methods=['POST'])
def setText():
    if not request.json or not 'elementNo' in request.json or not 'text' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_text'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getText', methods=['GET'])
def getText():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_text'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTextPosition', methods=['POST'])
def setTextPosition():
    if not request.json or not 'elementNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'relocate_text'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTextPosition', methods=['GET'])
def getTextPosition():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_text_position'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTextPointSize', methods=['POST'])
def setTextPointSize():
    if not request.json or not 'elementNo' in request.json or not 'pt' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_text_point_size'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTextPointSize', methods=['GET'])
def getTextPointSize():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_text_point_size'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTextFont', methods=['POST'])
def setTextFont():
    if not request.json or not 'elementNo' in request.json or not 'font' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_text_font'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTextFont', methods=['GET'])
def getTextFont():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_text_font'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/setTextColor', methods=['POST'])
def setTextColor():
    if not request.json or not 'elementNo' in request.json or not 'color' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'set_text_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getTextColor', methods=['GET'])
def getTextColor():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'get_text_color'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/showElement', methods=['POST'])
def showElement():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'show_element'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/hideElement', methods=['POST'])
def hideElement():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'hide_element'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/checkElementVisibility', methods=['GET'])
def checkElementVisibility():
    if not request.json or not 'elementNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'check_element_visibility'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/hideSetupSurface', methods=['POST'])
def hideSetupSurface():
    dict = json.loads(request.json)
    dict['call'] = 'hide_setup_surface'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/showSetupSurface', methods=['POST'])
def showSetupSurface():
    dict = json.loads(request.json)
    dict['call'] = 'show_setup_surface'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/getSetupSurfaceVisibility', methods=['GET'])
def getSetupSurfaceVisibility():
    dict = json.loads(request.json)
    dict['call'] = 'get_setup_surface_visibility'
    returnData = processor.processMessage(dict)
    return returnData

@app.route('/api/removeElement', methods=['POST'])
def removeElement():
    if not request.json or not 'elementNo' in request.json or not 'windowNo' in request.json:
        abort(400)
    dict = json.loads(request.json)
    dict['call'] = 'remove_element'
    returnData = processor.processMessage(dict)
    return returnData

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true': #Only run on the child server to prevent two windows and port blocking
        messageParser = apiMessageParser()
        messageParser.processMessage("login,webusr")
        messageParser.processMessage("appName,REST")
        counter = 0
        files = glob.glob('images/*')
        for f in files:
            os.remove(f)
    app.run(port=5000, debug=True, host='0.0.0.0')