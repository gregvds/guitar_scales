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


strandbergPen = QPen(Qt.black)
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
    'color': Qt.white,
    'size_x': 25,
    'size_y': 25,
    'delta_x': 0.5,
    'delta_y': 0.0},
".strandberg＊": {
    'type': QGraphicsEllipseItem,
    'color': Qt.white,
    'pen': strandbergPen,
    'size_x': 9,
    'size_y': 9,
    'delta_x': 0.5,
    'delta_y': 0.8},
"Celeste": {
    'type': NoBroderRectItem,
    'color': QColor(234, 202, 164),
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
