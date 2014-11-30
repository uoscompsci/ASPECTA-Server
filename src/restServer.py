#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

class processor(object):
    @staticmethod
    def processMessage(message):
        print message
        return jsonify({})

@app.route('/api/newSurface', methods=['POST'])
def newSurface():
    returnData = processor.processMessage("new_surface")
    return returnData
    
@app.route('/api/newSurfaceWithID', methods=['POST'])
def newSurfaceWithID():
    if not request.json or not 'ID' in request.json:
        abort(400)
    returnData = processor.processMessage("new_surface," + request.json['ID'])
    return returnData

@app.route('/api/newCursor', methods=['POST'])
def newCursor():
    if not request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    returnData = processor.processMessage("new_cursor," + str(request.json['surfaceNo']) + "," + str(request.json['x']) + "," + str(request.json['y']))
    return returnData

@app.route('/api/newCursorWithID', methods=['POST'])
def newCursorWithID():
    if not request.json or not 'ID' in request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json:
        abort(400)
    returnData = processor.processMessage("new_cursor_with_ID," + str(request.json['ID']) + "," + str(request.json['surfaceNo']) + "," + str(request.json['x']) + "," + str(request.json['y']))
    return returnData

@app.route('/api/newWindow', methods=['POST'])
def newWindow():
    if not request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'name' in request.json:
        abort(400)
    returnData = processor.processMessage("new_window," + str(request.json['surfaceNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['name']))
    return returnData

@app.route('/api/newWindowWithID', methods=['POST'])
def newWindowWithID():
    if not request.json or not 'ID' in request.json or not 'surfaceNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'name' in request.json:
        abort(400)
    returnData = processor.processMessage("new_window_with_ID," + str(request.json['ID']) + "," + str(request.json['surfaceNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['name']))
    return returnData

@app.route('/api/newCircle', methods=['POST'])
def newCircle():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'radius' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_circle," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['radius']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newCircleWithID', methods=['POST'])
def newCircleWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'radius' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_circle_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['radius']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newLine', methods=['POST'])
def newLine():
    if not request.json or not 'windowNo' in request.json or not 'xStart' in request.json or not 'yStart' in request.json or not 'xEnd' in request.json or not 'yEnd' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_line," + str(request.json['windowNo']) + "," + str(request.json['xStart']) + "," + str(request.json['yStart']) + "," + str(request.json['xEnd']) + "," + str(request.json['yEnd']) + "," + str(request.json['color']))
    return returnData

@app.route('/api/newLineWithID', methods=['POST'])
def newLineWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'xStart' in request.json or not 'yStart' in request.json or not 'xEnd' in request.json or not 'yEnd' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_line_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['xStart']) + "," + str(request.json['yStart']) + "," + str(request.json['xEnd']) + "," + str(request.json['yEnd']) + "," + str(request.json['color']))
    return returnData

@app.route('/api/newLineStrip', methods=['POST'])
def newLineStrip():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_line_strip," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['color']))
    return returnData

@app.route('/api/newLineStripWithID', methods=['POST'])
def newLineStripWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_line_strip_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['color']))
    return returnData

@app.route('/api/newPolygon', methods=['POST'])
def newPolygon():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_polygon," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newPolygonWithID', methods=['POST'])
def newPolygonWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_polygon_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newRectangle', methods=['POST'])
def newRectangle():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_rectangle," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newRectangleWithID', methods=['POST'])
def newRectangleWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'linecolor' in request.json or not 'fillcolor' in request.json:
        abort(400)
    returnData = processor.processMessage("new_rectangle_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['linecolor']) + "," + str(request.json['fillcolor']))
    return returnData

@app.route('/api/newTexRectangle', methods=['POST'])
def newTexRectangle():
    if not request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'texture' in request.json:
        abort(400)
    returnData = processor.processMessage("new_texrectangle," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['texture']))
    return returnData

@app.route('/api/newTexRectangleWithID', methods=['POST'])
def newTexRectangleWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'x' in request.json or not 'y' in request.json or not 'width' in request.json or not 'height' in request.json or not 'texture' in request.json:
        abort(400)
    returnData = processor.processMessage("new_texrectangle_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['width']) + "," + str(request.json['height']) + "," + str(request.json['texture']))
    return returnData

@app.route('/api/newText', methods=['POST'])
def newText():
    if not request.json or not 'windowNo' in request.json or not 'text' in request.json or not 'x' in request.json or not 'y' in request.json or not 'pt' in request.json or not 'font' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_text," + str(request.json['windowNo']) + "," + str(request.json['text']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['pt']) + "," + str(request.json['font']) + "," + str(request.json['color']))
    return returnData

@app.route('/api/newTextWithID', methods=['POST'])
def newTextWithID():
    if not request.json or not 'ID' in request.json or not 'windowNo' in request.json or not 'text' in request.json or not 'x' in request.json or not 'y' in request.json or not 'pt' in request.json or not 'font' in request.json or not 'color' in request.json:
        abort(400)
    returnData = processor.processMessage("new_text_with_ID," + str(request.json['ID']) + "," + str(request.json['windowNo']) + "," + str(request.json['text']) + "," + str(request.json['x']) + "," + str(request.json['y']) + "," + str(request.json['pt']) + "," + str(request.json['font']) + "," + str(request.json['color']))
    return returnData

if __name__ == '__main__':
    app.run(debug=True)