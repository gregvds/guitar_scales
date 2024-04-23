# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/04/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen

class NoBroderEllipseItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the pen to transparent color (no border)
        self.setPen(QPen(Qt.transparent))

class NoBroderRectItem(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the pen to transparent color (no border)
        self.setPen(QPen(Qt.transparent))

def hex_to_qcolor(hex_color):
    # Remove '#' from the beginning of the hexadecimal string if present
    hex_color = hex_color.lstrip('#')

    # Convert hexadecimal color code to RGB values
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    # Create a QColor object with the RGB values
    qcolor = QColor(red, green, blue)

    return qcolor

strandbergPen = QPen(hex_to_qcolor("#1A120B"))
strandbergPen.setWidth(2)

inlaysGeneralParameters = {
"black_dot": {
    'type': NoBroderEllipseItem,
    'color': Qt.black,
    'size_x': 20,
    'size_y': 20,
    'delta_x': 0.5,
    'delta_y': 0.0},
"white_dot": {
    'type': NoBroderEllipseItem,
    'color': hex_to_qcolor("#FAF8F1"),
    'size_x': 25,
    'size_y': 25,
    'delta_x': 0.5,
    'delta_y': 0.0},
".strandberg＊": {
    'type': QGraphicsEllipseItem,
    'color': hex_to_qcolor("#E5E5CB"),
    'pen': strandbergPen,
    'size_x': 9,
    'size_y': 9,
    'delta_x': 0.5,
    'delta_y': 0.8},
"Celeste": {
    'type': NoBroderRectItem,
    'color': hex_to_qcolor("#E3CAA5"),
    'size_x': 7,
    'size_y': 40,
    'delta_x': 0.5,
    'delta_y': 0.8},
"Millimetric": {
    'type': NoBroderRectItem,
    'color': Qt.black,
    'size_x': 2,
    'size_y': 45,
    'delta_x': 0.5,
    'delta_y': 0.76},
}

sideInlaysRoundSize = 8
sideInlaysDeltaY = 1.3

sideInlaysGeneralParameters = {
"black_dot": {
    'type': NoBroderEllipseItem,
    'color': Qt.black,
    'size_x': sideInlaysRoundSize,
    'size_y': sideInlaysRoundSize,
    'delta_x': 0.5,
    'delta_y': sideInlaysDeltaY},
"white_dot": {
    'type': NoBroderEllipseItem,
    'color': Qt.white,
    'size_x': sideInlaysRoundSize,
    'size_y': sideInlaysRoundSize,
    'delta_x': 0.5,
    'delta_y': sideInlaysDeltaY},
".strandberg＊": {
    'type': QGraphicsEllipseItem,
    'color': Qt.white,
    'pen': strandbergPen,
    'size_x': 9,
    'size_y': 9,
    'delta_x': 0.5,
    'delta_y': sideInlaysDeltaY},
"Celeste": {
    'type': NoBroderRectItem,
    'color': QColor(234, 202, 164),
    'size_x': 7,
    'size_y': 12,
    'delta_x': 0.5,
    'delta_y': sideInlaysDeltaY-.1},
"Millimetric": {
    'type': NoBroderRectItem,
    'color': Qt.black,
    'size_x': 2,
    'size_y': 12,
    'delta_x': 0.5,
    'delta_y': sideInlaysDeltaY-.1},
}

inlaymarkings = {
2: 1,
4: 1,
6: 1,
8: 1,
11: 2,
14: 1,
16: 1,
18: 1,
20: 1,
23: 2
}

# based on the generic inlay of each type, we generate all the inlays for every
# position on the neck
inlays = {}
sideInlays = {}
for inlayType in inlaysGeneralParameters.keys():
    inlays[inlayType] = {}
    sideInlays[inlayType] = {}
    for inlaymarking in inlaymarkings.keys():
        inlays[inlayType][inlaymarking] = []
        sideInlays[inlayType][inlaymarking] = []
        for i in range(inlaymarkings[inlaymarking]):
            inlays[inlayType][inlaymarking].append({})
            sideInlays[inlayType][inlaymarking].append({})
            for param in inlaysGeneralParameters[inlayType].keys():
                inlays[inlayType][inlaymarking][i][param] = inlaysGeneralParameters[inlayType][param]
                sideInlays[inlayType][inlaymarking][i][param] = sideInlaysGeneralParameters[inlayType][param]

# and according to each type, we tune the positions and or size of certain inlays
inlays["black_dot"][11][0]['delta_y'] = 0.75
inlays["black_dot"][11][1]['delta_y'] = -0.75
inlays["black_dot"][23][0]['delta_y'] = 0.75
inlays["black_dot"][23][1]['delta_y'] = -0.75

inlays["white_dot"][11][0]['delta_y'] = 0.75
inlays["white_dot"][11][1]['delta_y'] = -0.75
inlays["white_dot"][23][0]['delta_y'] = 0.75
inlays["white_dot"][23][1]['delta_y'] = -0.75

inlays[".strandberg＊"][11][1]['delta_y'] = inlays[".strandberg＊"][11][1]['delta_y']-0.4
inlays[".strandberg＊"][14][0]['delta_y'] = -inlays[".strandberg＊"][14][0]['delta_y']
inlays[".strandberg＊"][16][0]['delta_y'] = -inlays[".strandberg＊"][16][0]['delta_y']
inlays[".strandberg＊"][18][0]['delta_y'] = -inlays[".strandberg＊"][18][0]['delta_y']
inlays[".strandberg＊"][20][0]['delta_y'] = -inlays[".strandberg＊"][20][0]['delta_y']
inlays[".strandberg＊"][23][0]['delta_y'] = -inlays[".strandberg＊"][23][0]['delta_y']
inlays[".strandberg＊"][23][1]['delta_y'] = -(inlays[".strandberg＊"][23][1]['delta_y']-0.4)

inlays["Celeste"][11][0]['size_y'] = inlays["Celeste"][11][0]['size_y']*1.7
inlays["Celeste"][11][1]['size_y'] = inlays["Celeste"][11][1]['size_y']*1.7
inlays["Celeste"][11][0]['delta_y'] = inlays["Celeste"][11][0]['delta_y']-0.18
inlays["Celeste"][11][1]['delta_y'] = -(inlays["Celeste"][11][1]['delta_y']-0.18)
inlays["Celeste"][23][1]['delta_y'] = -inlays["Celeste"][23][1]['delta_y']

inlays["Millimetric"][11][0]['delta_x'] -= 0.17
inlays["Millimetric"][11][1]['delta_x'] += 0.17
inlays["Millimetric"][23][0]['delta_x'] -= 0.17
inlays["Millimetric"][23][1]['delta_x'] += 0.17

inlays["None"]= {}

# and according to each type, we tune the positions and or size of certain sideInlays
sideInlays["black_dot"][11][0]['delta_x'] -= 0.17
sideInlays["black_dot"][11][1]['delta_x'] += 0.17
sideInlays["black_dot"][23][0]['delta_x'] -= 0.17
sideInlays["black_dot"][23][1]['delta_x'] += 0.17

sideInlays["white_dot"][11][0]['delta_x'] -= 0.17
sideInlays["white_dot"][11][1]['delta_x'] += 0.17
sideInlays["white_dot"][23][0]['delta_x'] -= 0.17
sideInlays["white_dot"][23][1]['delta_x'] += 0.17

sideInlays[".strandberg＊"][11][0]['delta_x'] -= 0.17
sideInlays[".strandberg＊"][11][1]['delta_x'] += 0.17
sideInlays[".strandberg＊"][23][0]['delta_x'] -= 0.17
sideInlays[".strandberg＊"][23][1]['delta_x'] += 0.17

sideInlays["Millimetric"][11][0]['delta_x'] -= 0.17
sideInlays["Millimetric"][11][1]['delta_x'] += 0.17
sideInlays["Millimetric"][23][0]['delta_x'] -= 0.17
sideInlays["Millimetric"][23][1]['delta_x'] += 0.17

sideInlays["None"]= {}


customColours = {
    "moss":   ("#C8B272","#A88B4C","#A0A584","#697153","#43362A","#C8B272"),
    "lichen": ("#B79A59","#826C37","#54442F","#DBCEAF","#C4AA52","#B79A59"),
    "sage":   ("#657359","#9AA582","#8B775F","#D7C9BE","#F1E4DB","#657359"),
    "mojave": ("#153448","#3C5B6F","#948979","#DFD0B8","#153448"),
    "marsice": ("#ED7D31","#6C5F5B","#4F4A45","#F6F1EE","#ED7D31"),
    "saltlake": ("#FFF6F4","#FFA41B","#F86F03","#525FE1","#FFF6F4"),
    "moschen": ("#FEE8B0","#9CA777","#7C9070","#F97B22","#FEE8B0"),
    "Lichss": ("#F58634","#FFCC29","#81B214","#206A5D","#F58634"),
    "Destorm": ("#FFB037","#FFE268","#364547","#2F5D62","#FFB037"),
    "Cotterra": ("#CC7351","#E08F62","#DED7B1","#9DAB86","#CC7351")}
