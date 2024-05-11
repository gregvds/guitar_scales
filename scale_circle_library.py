# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsEllipseItem
from catalogs import scales

# -----------------------------------------------------------------------------

class GenericNoteItem:
    def __init__(self, noteOnNeck=False, embeddingWidget=None):
        self.note = ''
        self.angle = ''
        self.colour = ''
        self.embeddingWidget = embeddingWidget
        #self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []
        self.continuouslyColoured = False

    def hoverEnterEvent(self, event):
        # Function to execute when mouse enters the ellipse
        #self.relatedNotesOnNeck = self.embeddingWidget.identifiedNotes[self.note]
        if hasattr(self.embeddingWidget, "mainWindowInstance"):
            referenceVFrame = self.embeddingWidget.mainWindowInstance.degreesFrames[0]
            colourCorrection = self.embeddingWidget.scale[referenceVFrame.currentDegree-1]-self.embeddingWidget.scale[self.embeddingWidget.modeIndex]
        else:
            colourCorrection = 0
        for note in self.embeddingWidget.identifiedNotes[self.note]:
            # If notes should be back to normal when leaving
            if self.continuouslyColoured is False:
                note[0].originalColour = note[0].brush().color()
                #self.relatedNotesOnNeckOriginalColours.append(note[0].brush().color())
            if hasattr(self.embeddingWidget, 'mainWindowInstance'):
                note2 = (self.note - colourCorrection)%12
                color = referenceVFrame.notesOnCircle[note2][0][2]
            else:
                color = self.colour
            note[0].setBrush(color)
            #note[0].continuouslyColoured = bool(self.continuouslyColoured)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self.continuouslyColoured is False:
            for note in self.embeddingWidget.identifiedNotes[self.note]:
                note[0].setBrush(note[0].originalColour)
                #note[0].continuouslyColoured = False
            #self.relatedNotesOnNeck = []
            self.relatedNotesOnNeckOriginalColours = []
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


# -----------------------------------------------------------------------------
