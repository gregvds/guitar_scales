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

class fretZeroNoteItem(QGraphicsPolygonItem):
    def __init__(self, parenta=None, noteOnNeck=False, embeddingWidget=None):
        super().__init__(parenta)
        self.setAcceptHoverEvents(True)
        self.note = ''
        self.angle = ''
        self.colour = ''
        self.embeddingWidget = embeddingWidget
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []

    def hoverEnterEvent(self, event):
        #print("Mouse entered the ellipse")
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        self.relatedNotesOnNeck = self.embeddingWidget.identifiedNotes[self.note]
        for note in self.relatedNotesOnNeck:
            #print("Note on neck diagram attribute:")
            #print("Note note: %s"%note[0].note)
            #print("i, j: %s, %s"%(note[2], note[3]))
            self.relatedNotesOnNeckOriginalColours.append(note[0].brush().color())
            #print("self.note: %s" % self.note)
            #print("notesOnCircle:")
            if hasattr(self.embeddingWidget, 'mainWindowInstance'):
                #print(self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle)
                refDegreeIndex = self.embeddingWidget.mainWindowInstance.degreesFrames[0].currentDegree-1
                semitoneAdjustement = scales[self.embeddingWidget.mainWindowInstance.scaleName][refDegreeIndex]
                note2 = (self.note)%12
                color = self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle[note2][0][2]
            else:
                color = self.colour
            note[0].setBrush(color)

    def hoverLeaveEvent(self, event):
        #print("Mouse left the ellipse")
        for (note, originalColour) in zip(self.relatedNotesOnNeck, self.relatedNotesOnNeckOriginalColours):
            note[0].setBrush(originalColour)
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []


class NoteItem(QGraphicsEllipseItem):
    def __init__(self, parenta=None, noteOnNeck=False, embeddingWidget=None):
        super().__init__(parenta)
        self.setAcceptHoverEvents(True)
        self.note = ''
        self.angle = ''
        self.colour = ''
        self.embeddingWidget = embeddingWidget
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []

    def hoverEnterEvent(self, event):
        # Function to execute when mouse enters the ellipse
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        self.relatedNotesOnNeck = self.embeddingWidget.identifiedNotes[self.note]
        for note in self.relatedNotesOnNeck:
            #print("Note on neck diagram attribute:")
            #print("Note note: %s"%note[0].note)
            #print("i, j: %s, %s"%(note[2], note[3]))
            self.relatedNotesOnNeckOriginalColours.append(note[0].brush().color())
            #print("self.note: %s" % self.note)
            #print("notesOnCircle:")
            if hasattr(self.embeddingWidget, 'mainWindowInstance'):
                #print(self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle)
                refDegreeIndex = self.embeddingWidget.mainWindowInstance.degreesFrames[0].currentDegree-1
                semitoneAdjustement = scales[self.embeddingWidget.mainWindowInstance.scaleName][refDegreeIndex]
                note2 = (self.note)%12
                color = self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle[note2][0][2]
            else:
                color = self.colour
            note[0].setBrush(color)

    def hoverLeaveEvent(self, event):
        # Function to execute when mouse leaves the ellipse
        for (note, originalColour) in zip(self.relatedNotesOnNeck, self.relatedNotesOnNeckOriginalColours):
            note[0].setBrush(originalColour)
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []


class TriangleNoteItem(QGraphicsPolygonItem):
    def __init__(self, parenta=None, noteOnNeck=False, embeddingWidget=None):
        super().__init__(parenta)
        self.setAcceptHoverEvents(True)
        self.note = ''
        self.angle = ''
        self.colour = ''
        self.embeddingWidget = embeddingWidget
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []

    def hoverEnterEvent(self, event):
        #print("Mouse entered the ellipse")
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        #print("Note attributes:\n    note: %s\n    angle: %s\n    colour: %s" % (self.note, self.angle, self.colour))
        self.relatedNotesOnNeck = self.embeddingWidget.identifiedNotes[self.note]
        for note in self.relatedNotesOnNeck:
            #print("Note on neck diagram attribute:")
            #print("Note note: %s"%note[0].note)
            #print("i, j: %s, %s"%(note[2], note[3]))
            self.relatedNotesOnNeckOriginalColours.append(note[0].brush().color())
            #print("self.note: %s" % self.note)
            #print("notesOnCircle:")
            if hasattr(self.embeddingWidget, 'mainWindowInstance'):
                #print(self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle)
                refDegreeIndex = self.embeddingWidget.mainWindowInstance.degreesFrames[0].currentDegree-1
                semitoneAdjustement = scales[self.embeddingWidget.mainWindowInstance.scaleName][refDegreeIndex]
                note2 = (self.note)%12
                color = self.embeddingWidget.mainWindowInstance.degreesFrames[0].notesOnCircle[note2][0][2]
            else:
                color = self.colour
            note[0].setBrush(color)

    def hoverLeaveEvent(self, event):
        #print("Mouse left the ellipse")
        for (note, originalColour) in zip(self.relatedNotesOnNeck, self.relatedNotesOnNeckOriginalColours):
            note[0].setBrush(originalColour)
        self.relatedNotesOnNeck = []
        self.relatedNotesOnNeckOriginalColours = []


# -----------------------------------------------------------------------------
