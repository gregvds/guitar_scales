# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/
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

notes = {
"C" : 0,
"C♯": 1,
"D" : 2,
"D♯": 3,
"E" : 4,
"F" : 5,
"F♯": 6,
"G" : 7,
"G♯": 8,
"A" : 9,
"A♯": 10,
"B" : 11
}

scales = {
"Natural"                   : [0, 2, 4, 5, 7, 9, 11],
"Harmonic"                  : [0, 2, 3, 5, 7, 8, 11],
"Melodic"                   : [0, 2, 3, 5, 7, 9, 11],
"Pentatonic"                : [0, 3, 5, 7, 10],
"Whole tone"                : [0, 2, 4, 6, 8, 10],
"Prometheus = Mystic chord" : [0, 2, 4, 6, 9, 10],
"Peiraiotikos"              : [0, 1, 4, 6, 7, 9, 11],
"Gypsy"                     : [0, 1, 4, 5, 7, 8, 11],
"Enigmatic"                 : [0, 1, 4, 6, 8, 10, 11],
"Neapolitan major"          : [0, 1, 3, 5, 7, 9, 11],
"Neapolitan minor"          : [0, 1, 3, 5, 7, 8, 11]
}

modes = {
(0, 3, 5, 7, 10)        : "Minor pentatonic",
(0, 2, 4, 7, 9)         : "Major pentatonic",
(0, 2, 5, 7, 10)        : "Egyptian",
(0, 3, 5, 8, 10)        : "Quan Ming",
(0, 2, 5, 7, 9)         : "Ritusen",
(0, 2, 4, 5, 7, 9, 11)  : "Ionian (major)",
(0, 2, 3, 5, 7, 9, 10)  : "Dorian",
(0, 1, 3, 5, 7, 8, 10)  : "Phrygian",
(0, 2, 4, 6, 7, 9, 11)  : "Lydian",
(0, 2, 4, 5, 7, 9, 10)  : "Mixolydian",
(0, 2, 3, 5, 7, 8, 10)  : "Aeolian (minor)",
(0, 1, 3, 5, 6, 8, 10)  : "Locrian",
(0, 2, 3, 5, 7, 8, 11)  : "Harmonic minor",
(0, 1, 3, 5, 6, 9, 10)  : "Locrian ♮13",
(0, 2, 4, 5, 8, 9, 11)  : "Ionian ♯5",
(0, 2, 3, 6, 7, 9, 10)  : "Romanian minor",
(0, 1, 4, 5, 7, 8, 10)  : "Phrygian dominant",
(0, 3, 4, 6, 7, 9, 11)  : "Lydian ♯9",
(0, 1, 3, 4, 6, 8, 9)   : "Superlocrian 𝄫7",
(0, 2, 3, 5, 7, 9, 11)  : "Melodic minor",
(0, 1, 3, 5, 7, 9, 10)  : "Dorian ♭9",
(0, 2, 4, 6, 8, 9, 11)  : "Lydian ♯5",
(0, 2, 4, 6, 7, 9, 10)  : "Bartók",
(0, 2, 4, 5, 7, 8, 10)  : "Mixolydian ♭13",
(0, 2, 3, 5, 6, 8, 10)  : "Aeolian ♭5",
(0, 1, 3, 4, 6, 8, 10)  : "Ravel",
(0, 1, 4, 6, 7, 9, 11)  : "Peiraiotikos",
(0, 3, 5, 6, 8, 10, 11) : "Mixolydian “♭1”",
(0, 2, 3, 5, 7, 8, 9)   : "Mela Jhankaradhvani",
(0, 1, 3, 5, 6, 7, 10)  : "Locrian 𝄫6",
(0, 2, 4, 5, 6, 9, 11)  : "Ionian ♭5",
(0, 2, 3, 4, 7, 9, 10)  : "Banshikicho",
(0, 1, 2, 5, 7, 8, 10)  : "Mela Ratnangi",
(0, 1, 4, 6, 8, 10, 11) : "Enigmatic",
(0, 3, 5, 7, 9, 10, 11) : "II Enigmatic",
(0, 2, 4, 6, 7, 8, 9)   : "Raga Kuntala",
(0, 2, 4, 5, 6, 7, 10)  : "IV Enigmatic",
(0, 2, 3, 4, 5, 8, 10)  : "V Enigmatic",
(0, 1, 2, 3, 6, 8, 10)  : "VI Enigmatic",
(0, 1, 2, 5, 7, 9, 11)  : "Mela Manativa",
(0, 1, 4, 5, 7, 8, 11)  : "Gypsy",
(0, 3, 4, 6, 7, 10, 11) : "Rasikapriya",
(0, 1, 3, 4, 7, 8, 9)   : "III Gypsy",
(0, 2, 3, 6, 7, 8, 11)  : "Hungarian minor",
(0, 1, 4, 5, 6, 9, 10)  : "Oriental",
(0, 3, 4, 5, 8, 9, 11)  : "VI Gypsy",
(0, 1, 2, 5, 6, 8, 9)   : "VII Gypsy",
(0, 1, 3, 5, 7, 9, 11)  : "Neapolitan major",
(0, 2, 4, 6, 8, 10, 11) : "Leading whole tone",
(0, 2, 4, 6, 8, 9, 10)  : "Synthetic mixture ♯5",
(0, 2, 4, 6, 7, 8, 10)  : "Minor lydian",
(0, 2, 4, 5, 6, 8, 10)  : "V Neapolitan major",
(0, 2, 3, 4, 6, 8, 10)  : "VI Neapolitan major",
(0, 1, 2, 4, 6, 8, 10)  : "VII Neapolitan major",
(0, 1, 3, 5, 7, 8, 11)  : "Neapolitan minor",
(0, 2, 4, 6, 7, 10, 11) : "Mela Citrambari",
(0, 2, 4, 5, 8, 9, 10)  : "Mixolydian ♯5",
(0, 2, 3, 6, 7, 8, 10)  : "Raga Camara",
(0, 1, 4, 5, 6, 8, 10)  : "Major locrian",
(0, 3, 4, 5, 7, 9, 11)  : "Mela Sulini",
(0, 1, 2, 4, 6, 8, 9)   : "Dorian “♯1”",
(0, 2, 4, 6, 8, 10)     : "Whole tone",
(0, 2, 4, 6, 9, 10)     : "Prometheus",
(0, 2, 4, 7, 8, 10)     : "II Prometheus",
(0, 2, 5, 6, 8, 10)     : "III Prometheus",
(0, 3, 4, 6, 8, 10)     : "IV Prometheus",
(0, 1, 3, 5, 7, 9)      : "V Prometheus",
(0, 2, 4, 6, 8, 11)     : "Eskimo Alaska point Hope"}

alterations = {-2: "𝄫",
               -1: "♭",
               0 : "",
               1 : "♯",
               2 : "♮"}

chords = {
(0, 7): {"name": "Powerchord", "notation": "5"},
(0, 8): {"name": "Augmented fifth", "notation": "♯5"},
(0, 6): {"name": "Diminished fifth", "notation": "♭5"},
(0, 4, 7): {"name": "Major", "notation": "M"},
(0, 3, 7): {"name": "Minor", "notation": "m"},
(0, 2, 7): {"name": "Suspended", "notation": "sus2"},
(0, 5, 7): {"name": "Suspended", "notation": "sus4"},
(0, 4, 8): {"name": "Augmented", "notation": "Aug"},
(0, 3, 6): {"name": "Diminished", "notation": "dim"},
(0, 4, 7, 10): {"name": "Dominant 7th", "notation": "7"},
(0, 3, 7, 10): {"name": "Minor 7th", "notation": "m7"},
(0, 5, 7, 10): {"name": "Suspended tetrad", "notation": "7sus"},
(0, 4, 7, 11): {"name": "Major 7th", "notation": "7maj"},
(0, 3, 7, 11): {"name": "Minor major 7th", "notation": "m7maj"},
(0, 4, 8, 11): {"name": "Augmented major 7th", "notation": "7maj♯5"},
(0, 4, 8, 10): {"name": "Augmented 7th", "notation": "7♯5"},
(0, 4, 6, 10): {"name": "Dominant 7th flat 5", "notation": "7♭5"},
(0, 3, 6, 10): {"name": "Half diminished", "notation": "m7♭5"},
(0, 3, 6, 9): {"name": "Diminished 7th", "notation": "dim7"},
(0, 4, 7, 9): {"name": "Major 6", "notation": "6"},
(0, 3, 7, 9): {"name": "Minor 6", "notation": "m6"}
}

tunings = {
"Standard 6 \tEADGBE"    : (0, 5, 10, 15, 19, 24),
"Drop D 6 \tDADGBE"      : (0, 7, 12, 17, 21, 26),
"open 6 \tDGDGBD"        : (0, 5, 12, 17, 21, 24),
"Standard 7 \tBEADGBE"   : (0, 5, 10, 15, 20, 24, 29),
"Drop A 7 \tAEADGBE"     : (0, 7, 12, 17, 22, 26, 31),
"Standard 8 \tF♯BEADGBE" : (0, 5, 10, 15, 20, 25, 29, 34),
"A-Tuning 8 \tADGCFADG"  : (0, 5, 10, 15, 20, 24, 29, 34),
"Drop E 8 \tEBEADGBE"    : (0, 7, 12, 17, 22, 27, 31, 36),
"Drop D 8 \tDADGCFAD"    : (0, 7, 12, 17, 22, 27, 31, 36)
}

stringGaugeFromNumberOfString = {
6 : "standard 6",
7 : ".strandberg＊ 7",
8 : ".standberg＊ 8"
}

semitonesToConsiderByNumberOfStrings = {
6: 24,
7: 24,
8: 36
}

stringSets = {
"standard 6"      : (10, 13, 17, 26, 36, 46),
".strandberg＊ 7" : (9.5, 13, 16, 24, 34, 46, 64),
".standberg＊ 8"  : (9, 12, 15, 22, 30, 42, 56, 84)
}

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



degrees = ("I", "II", "III", "IV", "V", "VI", "VII")

degreeArrangements = (
(1,),
(2,),
(3,),
(4,),
(5,),
(6,),
(7,),
(1,2,3),
(1, 5, 6, 4),
(2, 4, 1, 5),
(1, 3, 6, 5),
(1, 2, 6, 5),
(1, 5, 4),
(1, 5, 2, 5),
(4, 1, 5, 6),
(1, 6, 1, 4),
(4, 1, 7, 6),
(1, 5, 5),
(1,2,3,4,5,6,7))
