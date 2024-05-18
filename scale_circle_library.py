# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsEllipseItem
from catalogs import scales, modes

# -----------------------------------------------------------------------------

class GenericNoteItem:
    def __init__(self, noteOnNeck=False, embeddingWidget=None):
        self.note = ''
        self.angle = ''
        self.colour = ''
        self.originalColour = ''
        self.embeddingWidget = embeddingWidget
        self.relatedNotesOnNeckOriginalColours = []
        self.continuouslyColoured = False

    def colourNotes(self):
        '''
        Colours momentarly all the same notes on the neck
        '''
        if hasattr(self.embeddingWidget, "mainWindowInstance"):
            referenceVFrame = self.embeddingWidget.mainWindowInstance.degreesFrames[0]
            colourCorrection = self.embeddingWidget.scale[referenceVFrame.degreeIndex]-self.embeddingWidget.scale[self.embeddingWidget.modeIndex]
        else:
            colourCorrection = 0
        for note in self.embeddingWidget.identifiedNotes[self.note]:
            color = None
            # If notes should be back to normal when leaving
            if self.continuouslyColoured is False:
                note[0].originalColour = note[0].brush().color()
                #color = note[0].brush().color()
            if hasattr(self.embeddingWidget, 'mainWindowInstance'):
                note2 = (self.note - colourCorrection)%12
                if note2 in referenceVFrame.notesOnCircle.keys():
                    color = referenceVFrame.notesOnCircle[note2][0][2]
                else:
                    color = self.colour
            else:
                color = self.colour
            if color:
                note[0].setBrush(color)

    def uncolourNotesConditionally(self):
        '''
        Stops Colouring momentarly all the same notes on the neck
        if no continuouslyColoured set by a simple click
        '''
        if self.continuouslyColoured is False:
            for note in self.embeddingWidget.identifiedNotes[self.note]:
                if hasattr(note[0], "originalColour"):
                    note[0].setBrush(note[0].originalColour)
            self.relatedNotesOnNeckOriginalColours = []

    def hoverEnterEvent(self, event):
        self.colourNotes()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.uncolourNotesConditionally()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        '''
        Toggles all the coloured notes permanently coloured or not
        '''
        for note in self.embeddingWidget.identifiedNotes[self.note]:
            if note[0].continuouslyColoured:
                note[0].continuouslyColoured = False
            else:
                note[0].continuouslyColoured = True
        super().mousePressEvent(event)

class PolgonNoteItem(GenericNoteItem, QGraphicsPolygonItem):
    def __init__(self,  parenta=None, noteOnNeck=False, embeddingWidget=None):
        GenericNoteItem.__init__(self, noteOnNeck=noteOnNeck, embeddingWidget=embeddingWidget)
        QGraphicsPolygonItem.__init__(self, parenta)
        self.setAcceptHoverEvents(True)

class RounNoteItem(GenericNoteItem, QGraphicsEllipseItem):
    def __init__(self,  parenta=None, noteOnNeck=False, embeddingWidget=None):
        GenericNoteItem.__init__(self, noteOnNeck=noteOnNeck, embeddingWidget=embeddingWidget)
        QGraphicsEllipseItem.__init__(self, parenta)
        self.setAcceptHoverEvents(True)

fretZeroNoteItem = PolgonNoteItem
NoteItem = RounNoteItem
TriangleNoteItem = PolgonNoteItem

def linkModesToScales():
    modesListByScaleDic = dict()
    for scaleName in scales.keys():
        modesListByScaleDic[scaleName] = list()
        scale =  scales[scaleName]
        scaleLength = len(scale)
        rotatedScale = scale
        for i in range(scaleLength):
            if tuple(rotatedScale) in modes.keys():
                modesListByScaleDic[scaleName].append(modes[tuple(rotatedScale)])
            rotatedScale = sorted([(inScale +(12-rotatedScale[1]))%12 for inScale in rotatedScale])
    return modesListByScaleDic

# -----------------------------------------------------------------------------
