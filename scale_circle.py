# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsLineItem
from PySide6.QtWidgets import QDialog, QPushButton, QRadioButton, QComboBox, QMenu, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QPointF, QRectF, QLineF, QSizeF, Slot
from PySide6.QtGui import QPolygonF, QPen, QPainter, QAction, QFont, QColor
import math
from catalogs import notes, scales, modes, alterations, tunings, stringSets, stringGaugeFromNumberOfString, chords, semitonesToConsiderByNumberOfStrings, degrees, degreeArrangements, inlays

# -----------------------------------------------------------------------------
SCALE_CIRCLE_RADIUS = 160
FRET_SPACING = 45
FRET_OVERSHOOT = 4
STRING_SPACING = 30

GRAPHICSVIEW_WIDTH = 459
GRAPHICSVIEW_HEIGHT = 366

# -----------------------------------------------------------------------------

class NeckWindow(QDialog):
    def __init__(self, mainWindowInstance):
        super().__init__()
        self.setWindowTitle("🎸 Neck general view")
        self.mainWindowInstance = mainWindowInstance

        self.once = True
        self.neckSceneRect = ''
        self.scaleName = ""
        self.rootNote = ''
        self.shownScale = list()
        self.scaleLength = 0

        self.currentTuningName = ""
        self.currentArrangement = (1,)
        self.referenceDegree = 0

        self.num_frets = 24
        self.first_root_position = -1
        self.num_strings = 0

        # Add neck_graphics_view to layout
        self.mainVBoxLayout = QVBoxLayout()
        self.topHBoxLayout = QHBoxLayout()
        self.mainVBoxLayout.addLayout(self.topHBoxLayout)

        self.neck_graphics_view = QGraphicsView()
        self.neck_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.neck_graphics_view.viewport().palette()
        palette.setColor(self.neck_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.neck_graphics_view.viewport().setPalette(palette)

        self.neck_scene = QGraphicsScene()
        self.neck_graphics_view.setScene(self.neck_scene)

        # Create a radio button to toggle showing the root notes
        self.create_show_root_button()
        #create the combobox to choose the note for the root
        self.create_root_note_combobox()
        #create the inlays combobox
        self.create_inlays_combobox()


        self.mainVBoxLayout.addWidget(self.neck_graphics_view)
        self.setLayout(self.mainVBoxLayout)

        # Groups to help manage graphic items
        self.neck_diagram_background_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group = QGraphicsItemGroup()
        self.neck_diagram_degrees_group = QGraphicsItemGroup()

        # Initialisation
        self.set_tuning(self.mainWindowInstance.currentTuningName, init=True)
        self.set_scale(self.mainWindowInstance.scaleName)

        # Enable antialiasing
        self.neck_graphics_view.setRenderHint(QPainter.Antialiasing)

# -----------------------------------------------------------------------------

    def set_tuning(self, tuning_name, init=False):
        '''
        Takes a tuning name and set it
        If not in init phase, the entire neck is redrawn
        '''
        self.currentTuningName = tuning_name
        self.currentTuning = tunings[self.currentTuningName]
        self.num_strings = len(self.currentTuning)


        # All this will be useful to draw a more realistic neck
        tuningNotesComposition = tuning_name.split('\t')[1].split()
        print(tuningNotesComposition)
        firstTuningNote = ''
        if len(tuningNotesComposition)>0 and tuningNotesComposition[0][1] == '♯':
            firstTuningNote = tuningNotesComposition[0][0]+tuningNotesComposition[0][1]
        else:
            firstTuningNote = tuningNotesComposition[0][0]
        print("\nIn set_tuning of NeckWindow, firstTuningNote: %s" % firstTuningNote)

        if not init:
            self.setRootNote()
            #self.draw_notes_on_neck()
            #self.label_degrees_on_neck()

    def set_scale(self, scale_name):
        '''

        '''
        self.scaleName = scale_name
        self.shownScale = scales[self.scaleName]
        self.scaleLength = len(self.shownScale)
        self.rootIndexInScale = 0
        self.draw_notes_on_neck()
        self.label_degrees_on_neck()

    def set_reference_degree(self, degreeIndex):
        deltaDegree = degreeIndex - self.referenceDegree
        self.move_root_index(deltaDegree)
        self.referenceDegree = degreeIndex #(0 - 6)
        self.draw_notes_on_neck()
        self.label_degrees_on_neck()

    def set_arrangement(self, arrangement):
        self.currentArrangement = arrangement
        #print("\nIn set_arrangement of NeckGeneralView, setting arrangement as ")
        #print(arrangement)
        self.label_degrees_on_neck()

    def setRootNote(self):
        # All this will be useful to draw a more realistic neck
        tuningNotesComposition = self.currentTuningName.split('\t')[1].split()
        print(tuningNotesComposition)
        firstTuningNote = ''
        if len(tuningNotesComposition)>0 and tuningNotesComposition[0][1] == '♯':
            firstTuningNote = tuningNotesComposition[0][0]+tuningNotesComposition[0][1]
        else:
            firstTuningNote = tuningNotesComposition[0][0]

        firstTuningNoteValue = notes[firstTuningNote]
        rootNoteValue = notes[self.root_note_combobox.currentText()]
        print('\nIn setRootNote: firstTuningNoteValue: %s' % firstTuningNoteValue)
        print('\nIn setRootNote: rootNoteValue: %s' % rootNoteValue)
        self.first_root_position = (rootNoteValue - firstTuningNoteValue)-1
        self.draw_notes_on_neck()
        self.label_degrees_on_neck()

# -----------------------------------------------------------------------------

    def create_show_root_button(self):
        self.show_root_radio_button = QRadioButton("Roots")
        self.show_root_radio_button.setChecked(True)
        self.show_root_radio_button.toggled.connect(self.draw_notes_on_neck)
        self.topHBoxLayout.addWidget(self.show_root_radio_button)

    def create_root_note_combobox(self):
        self.root_note_combobox = QComboBox()
        self.root_note_combobox.addItems(notes.keys())
        self.rootNote = "E"
        self.root_note_combobox.setCurrentText(self.rootNote)
        self.root_note_combobox.currentTextChanged.connect(lambda: self.setRootNote())
        #self.root_note_combobox.highlighted.connect(self.setRootNote)
        self.topHBoxLayout.addWidget(self.root_note_combobox)

    def create_inlays_combobox(self):
        self.inlays_combobox = QComboBox()
        self.inlays_combobox.addItems(inlays.keys())
        self.inlays_combobox.setCurrentText(".strandberg＊")
        self.inlays_combobox.currentTextChanged.connect(lambda: self.draw_notes_on_neck())
        #self.root_note_combobox.highlighted.connect(self.setRootNote)
        self.topHBoxLayout.addWidget(self.inlays_combobox)

    def move_root_index(self, direction):
        '''
        Unused currently. Moves the root notes
        '''
        self.rootIndexInScale = (self.rootIndexInScale+direction)%self.scaleLength

    def define_root_by_note_click(self, event):
        '''
        Not functional; unused
        '''
        print("click ok", event.scenePos())
        if event.button() == Qt.LeftButton:
            print("left click ok")
            # Check if the mouse click is inside the ellipse
            for semitone_text in self.identifiedNotes.keys():
                for note in self.identifiedNotes[semitone_text]:
                    print("that is generating a lot of trace...")
                    if note[0].contains(event.scenePos()):
                        print("Clicked on %s situated in x: %s - y: %s!"%(note[1], note[2], note[3]))

    def draw_neck_background(self, rootUndefined=True):
        '''
        Draws the strings and frets background canvas
        '''

        neck_width = FRET_SPACING * (self.num_frets + 1)
        neck_height = STRING_SPACING * (self.num_strings - 1)
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]

        self.clear_group(self.neck_diagram_background_group)

        # Draw strings
        string_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        string_darkGray_pen.setWidth(1)      # Set the pen width

        #Draw borders of neck
        fretOvershoot = FRET_OVERSHOOT+1
        top = QGraphicsLineItem(-15, -fretOvershoot, neck_width, -fretOvershoot)
        bottom = QGraphicsLineItem(-15, neck_height+fretOvershoot, neck_width, neck_height+fretOvershoot)
        string_darkGray_pen.setWidth(0.5)
        top.setPen(string_darkGray_pen)
        bottom.setPen(string_darkGray_pen)
        self.neck_diagram_background_group.addToGroup(top)
        self.neck_diagram_background_group.addToGroup(bottom)

        # Draw inlays
        self.draw_inlays(type=self.inlays_combobox.currentText()) #.strandberg＊

        for i in range(self.num_strings):
            y = i * STRING_SPACING
            line = QGraphicsLineItem(-15, y, neck_width, y)
            string_darkGray_pen.setWidth(strings_thickness[i]/10.0)
            line.setPen(string_darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

        # Draw fret 0 and nut
        fret_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        fret_darkGray_pen.setWidth(4)      # Set the pen width
        line = QGraphicsLineItem(0, -FRET_OVERSHOOT, 0, neck_height+FRET_OVERSHOOT)
        line.setPen(fret_darkGray_pen)
        self.neck_diagram_background_group.addToGroup(line)

        fret_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        fret_darkGray_pen.setWidth(10)      # Set the pen width
        line = QGraphicsLineItem(-15, -FRET_OVERSHOOT+4, -15, neck_height+FRET_OVERSHOOT-4)
        line.setPen(fret_darkGray_pen)
        self.neck_diagram_background_group.addToGroup(line)

        # Draw frets
        fret_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        fret_darkGray_pen.setWidth(3)      # Set the pen width
        for i in range(1, self.num_frets + 1):
            x = i * FRET_SPACING
            line = QGraphicsLineItem(x, -FRET_OVERSHOOT, x, neck_height+FRET_OVERSHOOT)
            line.setPen(fret_darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)


        if self.neck_diagram_background_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_background_group)

    def draw_inlays(self, type="black_dot"):
        neck_height = STRING_SPACING * (self.num_strings - 1)
        localInlays = inlays
        for i in range(0, self.num_frets):
            if i in localInlays[type].keys():
                for inlayMark in localInlays[type][i]:
                    x = (FRET_SPACING*inlayMark['delta_x']) + i * FRET_SPACING
                    y = neck_height/2 + neck_height/2*inlayMark['delta_y']
                    point = QPointF(x, y)
                    inlay = inlayMark['type'](QRectF(point - QPointF(inlayMark['size_x']/2, inlayMark['size_y']/2), QSizeF(inlayMark['size_x'], inlayMark['size_y'])))
                    inlay.setBrush(inlayMark['color'])
                    self.neck_diagram_background_group.addToGroup(inlay)

    def draw_notes_on_neck(self):
        '''
        draws all the scale notes on the entire neck
        '''
        if self.once:
            self.neckSceneRect = self.neck_scene.sceneRect()

        fret_spacing = FRET_SPACING
        string_spacing = STRING_SPACING

        neck_width = fret_spacing * (self.num_frets + 1)
        neck_height = string_spacing * (self.num_strings - 1)
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]

        self.draw_neck_background()

        self.identifiedNotes = {each: list() for each in range(12)}
        self.clear_group(self.neck_diagram_notes_group)

        # from low to high strings
        for i in range(self.num_strings):
            y = neck_height - (i * string_spacing)
            # from low to high frets
            for j in range(0, self.num_frets):
                x = (fret_spacing/2.0) + j * fret_spacing
                semitone_text = (self.currentTuning[i] + j) - self.first_root_position
                if semitone_text%12 in self.shownScale:
                    point = QPointF(x, y)
                    if self.show_root_radio_button.isChecked() and semitone_text%12 == self.shownScale[self.rootIndexInScale]:
                        triangle = QPolygonF()
                        triangle.append(QPointF(string_spacing/2.0, 0))  # Top point
                        triangle.append(QPointF(string_spacing, string_spacing))  # Bottom right point
                        triangle.append(QPointF(0, string_spacing))  # Bottom left point
                        note_point = QGraphicsPolygonItem(triangle)
                        note_point.setPos(x-string_spacing/2.0, y-string_spacing/2.0)
                    else:
                        note_point = QGraphicsEllipseItem(QRectF(point - QPointF(string_spacing/2.0, string_spacing/2.0), QSizeF(string_spacing, string_spacing)))
                    self.identifiedNotes[semitone_text%12].append([note_point, semitone_text, i, j])
                    self.neck_diagram_notes_group.addToGroup(note_point)
                    #note_point.mousePressEvent = self.define_root_by_note_click

        self.color_notes_by_default()

        if self.neck_diagram_notes_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_notes_group)

        if self.once:
            self.once = False
        else:
            self.center_neck_view()

    def label_degrees_on_neck(self):
        #if self.once:
        #    self.neckSceneRect = self.neck_scene.sceneRect()

        fret_spacing = FRET_SPACING
        string_spacing = STRING_SPACING
        neck_width = fret_spacing * (self.num_frets + 1)
        neck_height = string_spacing * (self.num_strings - 1)

        self.identifiedDegrees = {each: list() for each in range(12)}
        self.clear_group(self.neck_diagram_degrees_group)

        font = QFont()
        font.setFamily("Garamond Premier Pro")
        font.setPointSize(.95*(STRING_SPACING))
        gray_pen = QPen(Qt.gray)

        # Label for used Degrees in arrangement
        for j in range(1, self.num_frets):
            x = (fret_spacing/2.0) + j * fret_spacing
            y = neck_height + 1.5*string_spacing
            semitone_text = (self.currentTuning[0] + j) - self.first_root_position
            if (semitone_text%12 in self.shownScale) and (self.first_root_position <= j <= self.num_frets - self.first_root_position):
                point = QPointF(x, y)
                note_point = QGraphicsEllipseItem(QRectF(point - QPointF(string_spacing/2.0, string_spacing/2.0), QSizeF(string_spacing, string_spacing)))
                note_point.hide()
                self.neck_diagram_degrees_group.addToGroup(note_point)
                self.identifiedDegrees[semitone_text%12].append([note_point, semitone_text, 0, j])

                # Creation of label object for the note
                degreeLabel = degrees[(self.shownScale.index(semitone_text%12) - self.referenceDegree)%self.scaleLength]
                text_item = QGraphicsSimpleTextItem(degreeLabel)
                text_item.setFont(font)
                text_item.setPos(point - QPointF(text_item.boundingRect().width()/2.0, text_item.boundingRect().height()/2.0))
                text_item.setFlags(QGraphicsItem.ItemIgnoresTransformations)
                # We add the label object to the record of the note
                self.identifiedDegrees[semitone_text%12][-1].append(text_item)
                self.neck_diagram_degrees_group.addToGroup(text_item)


        self.color_degrees()

        if self.neck_diagram_degrees_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_degrees_group)
        self.center_neck_view()

# -----------------------------------------------------------------------------

    def clear_group(self, group):
        '''
        remove all the item from a group and remove the group from the scene
        '''
        for item in group.childItems():
            if item in self.neck_scene.items():
                self.neck_scene.removeItem(item)
            group.removeFromGroup(item)

        if group in self.neck_scene.items():
            self.neck_scene.removeItem(group)

    def color_notes_by_default(self):
        transblack = QColor(Qt.black)
        transblack.setAlpha(128)
        trans = QColor(Qt.black)
        trans.setAlpha(255)
        transblack_pen = QPen(trans)
        transblack_pen.setColor(trans)
        gray_pen = QPen(Qt.gray)
        for note in self.identifiedNotes.keys():
            for (note_point, semitone_text, string, fret) in self.identifiedNotes[note]:
                note_point.setBrush(transblack)
                note_point.setPen(transblack_pen)
                '''
                if self.first_root_position <= fret <= self.num_frets - self.first_root_position:
                    note_point.setBrush(Qt.black)
                    note_point.setPen(black_pen)
                else:
                    note_point.setBrush(Qt.gray)
                    note_point.setPen(gray_pen)

                    blur_effect = QGraphicsBlurEffect()
                    blur_radius = (self.first_root_position - fret) if (fret < self.first_root_position) else (fret - (self.num_frets - self.first_root_position))
                    blur_effect.setBlurRadius(blur_radius*10)
                    note_point.setGraphicsEffect(blur_effect)
                '''

    def color_degrees(self):
        black_pen = QPen(Qt.black)
        white_pen = QPen(Qt.white)
        degreeIncrement = 1
        for semiTone in self.identifiedDegrees.keys():
            #print("for semiTone %s" % semiTone)
            #print("with degreeIncrement %s" % degreeIncrement)
            first = True
            for (note_point, semitone_text, string, fret, text_item) in self.identifiedDegrees[semiTone]:
                #print("for note at fret %s in semiTone %s" % (fret, semiTone))
                #print("with first %s and degreeIncrement: %s" % (first, degreeIncrement))
                if first:
                    #print("/In color_degrees with degreeIncrement = %s, self.referenceDegree = %s and self.currentArrangement = " % (degreeIncrement, self.referenceDegree))
                    #print(self.currentArrangement)
                    currentRelativeDegree = (((degreeIncrement-1) - self.referenceDegree)%self.scaleLength) + 1
                    if (currentRelativeDegree in self.currentArrangement):
                        #print("first position of degree and degreeIncrement %s in " % degreeIncrement)
                        #print(self.currentArrangement)
                        note_point.setBrush(Qt.black)
                        note_point.setPen(black_pen)
                        text_item.setBrush(Qt.white)
                        text_item.setPen(white_pen)
                    else:
                        note_point.hide()
                        text_item.hide()
                    # We only work with the first given position of all the ones identified (usually only degree I has two positions)
                    first = False
                    degreeIncrement += 1
                else:
                    note_point.hide()
                    text_item.hide()

    def center_neck_view(self):
        # Get the bounding rectangle of all items in the scene
        rect = self.neck_scene.itemsBoundingRect()

        # Calculate the center point of the bounding rectangle
        center = rect.center()

        # Get the size of the viewport
        view_size = self.neck_graphics_view.viewport().size()

        # Calculate the new position for the scene
        scene_pos = center - QPointF(view_size.width() / 2, view_size.height() / 2)

        # Set the new position for the scene
        self.neck_scene.setSceneRect(scene_pos.x(), scene_pos.y(), view_size.width(), view_size.height())
        self.neck_graphics_view.viewport().update()

    def refresh(self):
        self.center_neck_view()

    def closeEvent(self, event):
        self.mainWindowInstance.full_neck_radioButton.setChecked(False)
        event.accept()



class NoteItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        # Function to execute when mouse enters the ellipse
        print("Mouse entered the ellipse")
        # Add your desired functionality here

    def hoverLeaveEvent(self, event):
        # Function to execute when mouse leaves the ellipse
        print("Mouse left the ellipse")
        # Add your desired functionality here

class CircleAndNeckVBoxFrame(QFrame):
    def __init__(self, topApp, degree, visible=False, name="frame0"):
        super().__init__()

        # The app in which this widget lives (and must have access to its parameters)
        self.topApp = topApp
        self.name = name

        self.once = True
        self.highStringLimit=4
        self.maximum_semitone_difference_in_tuning = 0

        # In the datamodel, degrees in scale are recorded as 1 to 7
        # in the code, we'll use indexes (0 to 6) so we can %7 on them
        # the reference degree is the root position in the scale
        # the current degree is the used degree of the scale in the arrangement
        self.referenceDegree = 1
        self.currentDegree = 1
        self.currentDegree = degree
        self.rotation = 0

        self.scaleName = ""
        self.shownScale = list()
        self.scaleLength = 0
        self.notesOnCircle = {}

        if visible:
            self.show()
        else:
            self.hide()
        self.isVisible = visible

        # All the frame is organized in a VBoxLayout
        self.thisVBoxLayout = QVBoxLayout()
        self.setLayout(self.thisVBoxLayout)

        # Add first circle_graphics_view to layout
        self.circle_graphics_view = QGraphicsView()
        self.circle_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH, GRAPHICSVIEW_HEIGHT)
        self.circle_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.circle_graphics_view.viewport().palette()
        palette.setColor(self.circle_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.circle_graphics_view.viewport().setPalette(palette)
        self.circle_scene = QGraphicsScene()
        #self.circle_scene.setAcceptHoverEvents(True)
        self.circle_graphics_view.setScene(self.circle_scene)
        #self.circle_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH, GRAPHICSVIEW_HEIGHT)
        self.thisVBoxLayout.addWidget(self.circle_graphics_view)

        # Add a central area for label of mode/degree in scale and chord choice
        self.centralHBoxLayout = QHBoxLayout()
        self.create_mode_labels()
        self.create_chords_combobox()
        #self.create_modes_arrow_buttons()
        self.create_strings_number_for_chords_buttons()
        self.thisVBoxLayout.addLayout(self.centralHBoxLayout)

        # Add last neck_graphics_view to layout
        self.neck_graphics_view = QGraphicsView()
        self.neck_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH, GRAPHICSVIEW_HEIGHT)
        self.neck_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.neck_graphics_view.viewport().palette()
        palette.setColor(self.neck_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.neck_graphics_view.viewport().setPalette(palette)
        self.neck_scene = QGraphicsScene()
        self.neck_graphics_view.setScene(self.neck_scene)
        #self.neck_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH, GRAPHICSVIEW_HEIGHT)
        self.thisVBoxLayout.addWidget(self.neck_graphics_view)

        # Groups to hold graphical parts such as general background, note points, line items and center pivot
        self.scale_circle_background = QGraphicsItemGroup()
        self.notes_group = QGraphicsItemGroup()
        self.notes_group.setHandlesChildEvents(False)
        self.scale_circle_center_group = QGraphicsItemGroup()
        self.neck_diagram_background_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group = QGraphicsItemGroup()

        self.identifiedNotes = {}

        # Draw circle and guitar neck backgrounds
        self.draw_scale_circle()

        # Initialisation
        self.set_tuning("Standard 6 \tEADGBE", init=True)
        self.set_scale("Natural")

        self.circle_graphics_view.setRenderHint(QPainter.Antialiasing)
        self.neck_graphics_view.setRenderHint(QPainter.Antialiasing)

    def create_mode_labels(self):
        self.centralMiddleVBoxLayout = QVBoxLayout()

        # Add Scale label to the layout
        ModeNamefont = QFont()
        ModeNamefont.setPointSize(24)
        ModeNamefont.setFamily("Garamond Premier Pro")
        self.labelModeName = QLabel("This is a label")
        self.labelModeName.setAlignment(Qt.AlignCenter)
        self.labelModeName.setFont(ModeNamefont)

        # Add Scale label to the layout
        modeContentfont = QFont()
        modeContentfont.setPointSize(16)
        modeContentfont.setFamily("Garamond Premier Pro")
        modeContentfont.setItalic(True)
        self.labelModeContent = QLabel("This is a label")
        self.labelModeContent.setAlignment(Qt.AlignCenter)
        self.labelModeContent.setFont(modeContentfont)

        self.centralMiddleVBoxLayout.addWidget(self.labelModeName)
        self.centralMiddleVBoxLayout.addWidget(self.labelModeContent)
        self.centralHBoxLayout.addLayout(self.centralMiddleVBoxLayout)

    def create_chords_combobox(self):
        labelFont = QFont()
        labelFont.setPointSize(20)
        labelFont.setFamily("Garamond Premier Pro")
        chordLabel = QLabel("Chord:")
        chordLabel.setAlignment(Qt.AlignLeft)
        chordLabel.setFont(labelFont)
        self.chords_combobox = QComboBox()
        self.chords_combobox.currentTextChanged.connect(lambda: self.show_chords())
        self.chords_combobox.highlighted.connect(self.show_highlighted_chord)

        chordVBoxLayout = QVBoxLayout()
        chordVBoxLayout.addWidget(chordLabel)
        chordVBoxLayout.addWidget(self.chords_combobox)
        self.centralHBoxLayout.addLayout(chordVBoxLayout)

    def create_strings_number_for_chords_buttons(self):
        up_button = QPushButton("↑", self)
        up_button.clicked.connect(self.more_strings_for_chord)
        up_button.setMinimumWidth(30)
        up_button.setMaximumWidth(40)

        down_button = QPushButton("↓", self)
        down_button.clicked.connect(self.less_strings_for_chord)
        down_button.setMinimumWidth(30)
        down_button.setMaximumWidth(40)

        stringsPushButtonsVBoxLayout = QVBoxLayout()
        stringsPushButtonsVBoxLayout.addWidget(up_button)
        stringsPushButtonsVBoxLayout.addWidget(down_button)
        self.centralHBoxLayout.addLayout(stringsPushButtonsVBoxLayout)

    """
    def create_modes_arrow_buttons(self):
        left_button = QPushButton("⤵", self)
        left_button.setGeometry(20, 60, 30, 30)
        left_button.clicked.connect(self.rotate_notes_clockwise)

        right_button = QPushButton("⤹", self)
        right_button.setGeometry(self.width() - 2*45, 60, 30, 30)
        right_button.clicked.connect(self.rotate_notes_counterclockwise)
    """

    def set_scale(self, scale_name):
        #print("\nIn set_scale of %s to set scale %s" % (self.name, scale_name))
        # Keeping current degree, rotation and ref degree
        degreeIndex = self.currentDegree - 1
        referenceDegreeIndex = self.referenceDegree - 1
        rotation = self.rotation
        #print("In set_scale of %s, currentDegree: %s" % (self.name, self.currentDegree))
        #print("In set_scale of %s, referenceDegree: %s" % (self.name, self.referenceDegree))
        #print("In set_scale of %s, rotation: %s" % (self.name, self.rotation))
        #print("In set_scale of %s, currentDegreeIndex: %s" % (self.name, degreeIndex))
        #print("In set_scale of %s, referenceDegreeIndex: %s" % (self.name, referenceDegreeIndex))
        # init before scale change
        self.currentDegree = 1
        self.referenceDegree = 1
        self.rotation = 0
        # scale change
        self.scaleName = scale_name
        self.shownScale = scales[self.scaleName]
        self.scaleLength = len(self.shownScale)
        self.draw_scale()
        self.draw_notes_on_neck()
        # and set back degree and reference degree
        self.set_degree((degreeIndex-referenceDegreeIndex)%self.scaleLength)
        self.set_reference_degree(degrees[referenceDegreeIndex], referenceDegreeIndex)
        #print("In set_scale of %s, currentDegree after scale change: %s" % (self.name, self.currentDegree))
        #print("In set_scale of %s, referenceDegree after scale change: %s" % (self.name, self.referenceDegree))

    def set_tuning(self, tuning_name, init=False):
        self.currentTuning = tunings[tuning_name]
        self.currentTuningName = tuning_name
        if not init:
            self.draw_notes_on_neck()
            self.show_chords()

    def set_degree(self, degreeIndex, movingRef=False):
        #print("\nIn set_degree of %s to set degree to %s for %s moving reference" % (self.name, degreeIndex, movingRef))
        print("\nIn set_degree of frame %s to set degreeIndex %s when movingRef %s" % (self.name, degreeIndex, movingRef))
        if not movingRef:
            print("\nIn set_degree of frame %s to set degreeIndex %s with self.referenceDegree %s" % (self.name, degreeIndex, self.referenceDegree))
            degreeIndex = (degreeIndex + (self.referenceDegree - 1))%self.scaleLength
            print("\nIn set_degree of frame %s to set degreeIndex %s" % (self.name, degreeIndex))

        currentDegreeIndex = self.currentDegree-1
        #print("In set_degree of %s, currentDegreeIndex: %s --- degreeIndex:%s" % (self.name, currentDegreeIndex, degreeIndex))
        if currentDegreeIndex > degreeIndex:
            for i in range(currentDegreeIndex - degreeIndex):
                #print('rotating clockwise')
                self.rotate_notes_clockwise()
        elif currentDegreeIndex < degreeIndex:
            for i in range(degreeIndex-currentDegreeIndex):
                #print('rotating counterclockwise')
                self.rotate_notes_counterclockwise()
        else:
            #print('not rotating')
            self.draw_scale()
            self.draw_notes_on_neck()
        self.currentDegree = degreeIndex+1
        print("In set_degree of %s, current after: %s" % (self.name, self.currentDegree))

    def set_reference_degree(self, degreeName, degreeIndex):
        print("\nIn set_reference_degree of %s to set reference to %s with index %s" % (self.name, degreeName, degreeIndex))
        #print("In set_reference_degree of %s, reference and current before: %s --- %s" % (self.name, self.referenceDegree, self.currentDegree))
        deltaCurrentDegreeToReference = (self.currentDegree-1)-(self.referenceDegree-1)
        CurrentDegreeToSet = (degreeIndex+deltaCurrentDegreeToReference)%self.scaleLength
        #print("In set_reference_degree of %s, delta between current and ref: %s" % (self.name, deltaCurrentDegreeToReference))
        #print("In set_reference_degree of %s, current degree to set: %s" % (self.name, CurrentDegreeToSet))
        self.referenceDegree = degreeIndex+1
        self.set_degree(CurrentDegreeToSet, movingRef=True)
        print("In set_reference_degree of %s, reference after: %s" % (self.name, self.referenceDegree))
        print("In set_reference_degree of %s, current after: %s" % (self.name, self.currentDegree))

    def draw_scale_circle(self):
        center = QPointF(0, 0)
        radius = SCALE_CIRCLE_RADIUS

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(3)      # Set the pen width

        # Draw scale circle
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(SCALE_CIRCLE_RADIUS, SCALE_CIRCLE_RADIUS), QSizeF(2*radius, 2*radius)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.circle_scene.addItem(scale_circle)

    def draw_scale_circle_center(self):
        center = QPointF(0, 0)

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(2)      # Set the pen width
        pen2 = QPen(Qt.white)  # Set the pen color
        pen2.setWidth(2)      # Set the pen width

        # Draw center circle
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(12, 12), QSizeF(24, 24)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen2)
        self.scale_circle_center_group.addToGroup(scale_circle)
        #self.circle_scene.addItem(scale_circle)
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(10, 10), QSizeF(20, 20)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.scale_circle_center_group.addToGroup(scale_circle)
        #self.circle_scene.addItem(scale_circle)
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(5, 5), QSizeF(10, 10)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.scale_circle_center_group.addToGroup(scale_circle)
        #self.circle_scene.addItem(scale_circle)
        if self.scale_circle_center_group not in self.circle_scene.items():
            self.circle_scene.addItem(self.scale_circle_center_group)

    def draw_scale(self):
        scale = self.shownScale
        if tuple(scale) in modes.keys():
            self.modeName = modes[tuple(scale)]
        else:
            self.modeName = ""
        #print("\nIn draw_scale of %s: self.currentDegree: %s --- self.referenceDegree: %s" % (self.name, self.currentDegree, self.referenceDegree))
        DegreeLabel = degrees[(self.rotation - (self.referenceDegree-1))%self.scaleLength]
        labelContent = DegreeLabel + " / " + self.modeName
        self.labelModeName.setText(labelContent)
        self.get_mode_composition()
        root = QPointF(0, -SCALE_CIRCLE_RADIUS)
        center = QPointF(0, 0)
        radius = SCALE_CIRCLE_RADIUS

        semiToneAngle = 2 * math.pi / 12
        angles = [noteInScale * semiToneAngle for noteInScale in scale]
        noteSizes = [10 for noteInScale in scale]
        noteSizes[0] = 2 * noteSizes[0]

        self.notesOnCircle = {noteInScale: list() for noteInScale in scale}

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(2)      # Set the pen width

        self.clear_group(self.notes_group)
        self.clear_group(self.scale_circle_center_group)


        for angle, noteSize, note in zip(angles, noteSizes, scale):
            x = center.x() + radius * math.sin(angle)
            y = center.y() - radius * math.cos(angle)
            point = QPointF(x, y)

            x = center.x() + 1.1 * radius * math.sin(angle)
            y = center.y() - 1.1 * radius * math.cos(angle)
            labelAnchor = QPointF(x, y)

            # Draw line from center to point
            line = QLineF(center, point)
            line_item = QGraphicsLineItem(line)
            self.notes_group.addToGroup(line_item)

            # Draw note point
            note_point = NoteItem(QRectF(point - QPointF(noteSize/2.0, noteSize/2.0), QSizeF(noteSize, noteSize)))
            note_colour = self.color_for_angle(angle)
            note_point.setBrush(note_colour) #Qt.white
            note_point.setPen(pen)
            note_point.setAcceptHoverEvents(True)
            self.notes_group.addToGroup(note_point)

            self.notesOnCircle[note].append((note_point, line_item, note_colour))

        if self.notes_group not in self.circle_scene.items():
            self.circle_scene.addItem(self.notes_group)

        self.draw_scale_circle_center()
        self.get_chords_in_mode()

    def draw_neck_background(self):
        neck_width = FRET_SPACING * (self.num_frets + 1)
        neck_height = STRING_SPACING * (self.num_strings - 1)
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]

        self.clear_group(self.neck_diagram_background_group)

        # Draw strings
        darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        darkGray_pen.setWidth(1)      # Set the pen width

        for i in range(self.num_strings):
            y = i * STRING_SPACING
            line = QGraphicsLineItem(0, y, neck_width, y)
            darkGray_pen.setWidth(strings_thickness[i]/10.0)
            line.setPen(darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

        # Draw frets
        darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        darkGray_pen.setWidth(3)      # Set the pen width

        for i in range(1, self.num_frets + 1):
            x = i * FRET_SPACING
            line = QGraphicsLineItem(x, -5, x, neck_height+5)
            line.setPen(darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

        if self.neck_diagram_background_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_background_group)

    def draw_notes_on_neck(self):
        if self.once:
            self.neckSceneRect = self.neck_scene.sceneRect()

        self.num_strings = len(self.currentTuning)
        self.get_maximum_semitone_difference_in_tuning()
        self.num_frets = self.maximum_semitone_difference_in_tuning + 1

        neck_width = FRET_SPACING * (self.num_frets + 1)
        neck_height = STRING_SPACING * (self.num_strings - 1)

        self.draw_neck_background()

        self.identifiedNotes = {each: list() for each in range(12)}
        self.identifiedNoteTexts = {each: list() for each in range(12)}

        self.clear_group(self.neck_diagram_notes_group)

        font = QFont()
        font.setFamily("Garamond Premier Pro")
        font.setPointSize(.95*(STRING_SPACING - 15))

        # from low to high strings
        for i in range(self.num_strings):
            y = neck_height - (i * STRING_SPACING)
            # from low to high frets
            for j in range(1, self.num_frets):
                x = (FRET_SPACING/2.0) + j * FRET_SPACING
                semitone_text = (self.currentTuning[i] + j) -2
                # If the value in semi-tone modulo 12 (whatever the octave) is part of the scale
                if semitone_text%12 in self.shownScale:
                    point = QPointF(x, y)
                    # If the note is the root note, let's plot a triangle
                    if semitone_text%12 == 0:
                        triangle = QPolygonF()
                        triangle.append(QPointF(STRING_SPACING/2.0, 0))  # Top point
                        triangle.append(QPointF(STRING_SPACING, STRING_SPACING))  # Bottom right point
                        triangle.append(QPointF(0, STRING_SPACING))  # Bottom left point
                        note_point = QGraphicsPolygonItem(triangle)
                        #note_point.setBrush(Qt.black)
                        note_point.setPos(x-STRING_SPACING/2.0, y-STRING_SPACING/2.0)
                    # else, let's plot a simple circle
                    else:
                        note_point = QGraphicsEllipseItem(QRectF(point - QPointF(STRING_SPACING/2.0, STRING_SPACING/2.0), QSizeF(STRING_SPACING, STRING_SPACING)))
                    # We record the symbol object, its note value and string and fret positions by note semi-tone value in the scale
                    self.identifiedNotes[semitone_text%12].append([note_point, semitone_text, i, j])
                    self.neck_diagram_notes_group.addToGroup(note_point)

                    # Generation of label for the note
                    note_number = (1+self.shownScale.index((semitone_text%12)))
                    alteration = self.shownScale[note_number-1] - self.referenceScale[note_number-1]
                    note_value = self.noteValues[note_number-1]
                    if semitone_text > 12 and note_value%2 == 0:
                        note_value+=7

                    # Creation of label object for the note
                    text_item = QGraphicsSimpleTextItem("%s"%(alterations[alteration]+str(note_value)))
                    text_item.setFont(font)
                    if semitone_text%12 == 0:
                        point = QPointF(x, y+5)
                    text_item.setPos(point - QPointF(text_item.boundingRect().width()/2.0, text_item.boundingRect().height()/2.0))
                    text_item.setFlags(QGraphicsItem.ItemIgnoresTransformations)
                    text_item.setFont(font)
                    # We add the label object to the record of the note
                    self.identifiedNotes[semitone_text%12][-1].append(text_item)
                    self.neck_diagram_notes_group.addToGroup(text_item)

        self.color_notes_by_default()

        if self.neck_diagram_notes_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_notes_group)

        if self.once:
            self.once = False
        else:
            self.center_neck_view()
        self.neck_graphics_view.viewport().update()

    def get_maximum_semitone_difference_in_tuning(self):
        self.maximum_semitone_difference_in_tuning = 0
        for i in range(len(self.currentTuning)-2):
            self.maximum_semitone_difference_in_tuning = max(self.maximum_semitone_difference_in_tuning, self.currentTuning[i+1]-self.currentTuning[i])

    def get_mode_composition(self):

        # Sets all the required variables according to the number of notes in the mode
        self.scaleLength = len(self.shownScale)
        if self.scaleLength == 7:
            self.referenceScale = scales["Natural"]
            self.noteValues = [1, 2, 3, 4, 5, 6, 7]
            self.modeComposition = ["", "", "", "", "", "", ""]
            self.evenNoteRejectionMatrix = [0, 4, 1, 5, 2, 6, 3]
        elif self.scaleLength == 6:
            self.referenceScale = [0, 2, 4, 5, 7, 11]
            self.noteValues = [1, 2, 3, 4, 5, 7]
            self.modeComposition = ["", "", "", "", "", ""]
            self.evenNoteRejectionMatrix = [0, 4, 1, 5, 2, 3]
        elif self.scaleLength == 5:
            self.referenceScale = [0, 2, 4, 7, 9]
            self.noteValues = [1, 2, 3, 5, 6]
            self.modeComposition = ["", "", "", "", ""]
            self.evenNoteRejectionMatrix = [0, 3, 1, 2, 4]

        # And generate the label for the mode composition
        for note_number in range(self.scaleLength):
            alteration = self.shownScale[note_number] - self.referenceScale[note_number]
            note_value = self.noteValues[note_number]
            if note_value%2 == 0:
                self.modeComposition[self.evenNoteRejectionMatrix[note_number]] = ("%s"%(alterations[alteration]+str(note_value+7)))
            else:
                self.modeComposition[self.evenNoteRejectionMatrix[note_number]] = ("%s"%(alterations[alteration]+str(note_value)))
        self.modeCompositionString = ', '.join(self.modeComposition)
        self.labelModeContent.setText(self.modeCompositionString)

    def get_chords_in_mode(self):

        self.availableChords = []
        for chord in chords.keys():
            if set(chord).issubset(tuple(self.shownScale)):
                self.availableChords.append(chord)
        self.chords_combobox.clear()
        self.chords_combobox.addItem("", userData=())
        for availableChord in self.availableChords:
            self.chords_combobox.addItem(chords[availableChord]["notation"], userData=availableChord)

    def angle_to_hue(self, angle):
        """
        Cosmetic; compute custom hue based on angle of note in circle (30° = a semi-tone)
        """
        # How about rotating colours too :-)
        #print("\nIn angle_to_hue of %s with rotation: %s" % (self.name, self.rotation))
        #print("In angle_to_hue of %s with scale %s" % (self.name, scales[self.scaleName]))
        #print("In angle_to_hue of %s with number of semi_tone: %s" % (self.name, scales[self.scaleName][self.rotation]))
        angleOfRotation = 30*scales[self.scaleName][self.rotation]
        #print("In angle_to_hue of %s with rotation angle: %s" % (self.name, angleOfRotation))
        # Normalize angle to be between 0 and 360 degrees
        angle = 360*(angle/(2*math.pi))
        angle += angleOfRotation
        angle %= 360
        # Calculate hue based on the angle
        if angle <= 120:
            hue = 60 - angle / 2
        elif angle <= 240:
            hue = 480 - angle
        else:
            hue = 600 - angle*3/2
        # Ensure hue is within valid range [0, 360]
        if hue < 0:
            hue += 360
        return hue

    def color_for_angle(self, angle):
        """
        Cosmetic; Create a QColor from angle
        """
        hue = self.angle_to_hue(angle)
        return QColor.fromHsvF(hue / 360, .45, .95)

    def clear_group(self, group):
        for item in group.childItems():
            if item in self.circle_scene.items():
                self.circle_scene.removeItem(item)
            if item in self.neck_scene.items():
                self.neck_scene.removeItem(item)
            group.removeFromGroup(item)

        if group in self.circle_scene.items():
            self.circle_scene.removeItem(group)
        if group in self.neck_scene.items():
            self.neck_scene.removeItem(group)


    def color_notes_by_default(self):
        #print('color by default with %s strings defined' % self.num_strings)
        black_pen = QPen(Qt.black)
        gray_pen = QPen(Qt.gray)
        # for each note in chord
        for note in self.identifiedNotes.keys():
            # for each position of the note
            for (note_point, semitone_text, string, fret, text_item) in self.identifiedNotes[note]:
                if 0 <= semitone_text <= semitonesToConsiderByNumberOfStrings[self.num_strings]:
                    note_point.setBrush(Qt.black)
                    note_point.setPen(black_pen)
                else:
                    note_point.setBrush(Qt.gray)
                    note_point.setPen(gray_pen)
                text_item.setBrush(Qt.white)
            #for (text_item, semitone_text, string, fret) in self.identifiedNoteTexts[note]:
            #    text_item.setBrush(Qt.white)
            for (note_point, line_item, note_colour) in self.notesOnCircle[self.shownScale[note%self.scaleLength]]:
                colour_pen = QPen(Qt.black)
                colour_pen.setWidth(1)
                line_item.setPen(colour_pen)

    def color_chord_notes(self, chord):
        #print('color by chord with %s strings defined' % self.num_strings)
        white_pen = QPen(Qt.white)
        gray_pen = QPen(Qt.gray)
        notes_potential_positions = {}
        strings_potential_positions = {}

        reserved_string_for_note = {}
        # for each note in chord
        for note in chord:
            notes_potential_positions[note] = []
            # for each position of the note
            for (note_point, semitone_text, string, fret, text_note) in self.identifiedNotes[note]:
                # if on an authorized string not already occupied
                if string <= self.highStringLimit-1 and string not in reserved_string_for_note.keys():
                    if 0 <= semitone_text <= semitonesToConsiderByNumberOfStrings[self.num_strings]:
                        # if note not Root on the first low string
                        if note > 0 and string == 0:
                            pass
                        # we keep the position as a potential position
                        else:
                            if fret < 6:
                                #print("Note: %s, String: %s, fret: %s" % (note, string, fret))
                                notes_potential_positions[note].append((string, fret, note_point, text_note))
            # if note found only in one position
            if len(notes_potential_positions[note]) == 1:
                # we reserve that string for that note
                reserved_string_for_note[notes_potential_positions[note][0][0]] = note

            for (note_point, line_item, note_colour) in self.notesOnCircle[note]:
                colour_pen = QPen(note_colour)
                colour_pen.setWidth(2)
                line_item.setPen(colour_pen)

        for note in chord:
            for each_position in notes_potential_positions[note]:
                # if more than one possible positions for a note
                if len(notes_potential_positions[note])>1:
                    # but passed if this position string already reserved
                    if each_position[0] in reserved_string_for_note.keys():
                        pass
                    else:
                        each_position[2].setBrush(Qt.white)
                        each_position[2].setPen(white_pen)
                        each_position[3].setBrush(Qt.black)
                else:
                    each_position[2].setBrush(Qt.white)
                    each_position[2].setPen(white_pen)
                    each_position[3].setBrush(Qt.black)

    def center_neck_view(self):
        # Get the bounding rectangle of all items in the scene
        rect = self.neck_scene.itemsBoundingRect()
        # Calculate the center point of the bounding rectangle
        center = rect.center()
        # Set the size of the viewport
        self.neck_graphics_view.viewport().setFixedSize(GRAPHICSVIEW_WIDTH, GRAPHICSVIEW_HEIGHT)
        view_size = self.neck_graphics_view.viewport().size()
        #print("In center_neck_view, viewport().size():")
        #print(view_size)
        # Calculate the new position for the scene
        scene_pos = center - QPointF(view_size.width() / 2, view_size.height() / 2)
        # Set the new position for the scene
        self.neck_scene.setSceneRect(scene_pos.x(), scene_pos.y(), view_size.width(), view_size.height())

    def refresh(self):
        self.center_neck_view()

    @Slot()
    def rotate_notes_counterclockwise(self):
        self.rotation +=1
        self.rotation = self.rotation%self.scaleLength
        self.chordBeforeChange = self.chords_combobox.currentText()
        # Rotate notes counterclockwise
        self.shownScale = sorted([(inScale +(12-self.shownScale[1]))%12 for inScale in self.shownScale])
        self.draw_scale()
        self.draw_notes_on_neck()
        for index in range(self.chords_combobox.count()):
            if self.chordBeforeChange == self.chords_combobox.itemText(index):
                self.chords_combobox.setCurrentIndex(index)

    @Slot()
    def rotate_notes_clockwise(self):
        self.rotation -=1
        self.rotation = self.rotation%self.scaleLength
        self.chordBeforeChange = self.chords_combobox.currentText()
        # Rotate notes clockwise
        self.shownScale = sorted([(inScale +(12-self.shownScale[-1]))%12 for inScale in self.shownScale])
        self.draw_scale()
        self.draw_notes_on_neck()
        for index in range(self.chords_combobox.count()):
            if self.chordBeforeChange == self.chords_combobox.itemText(index):
                self.chords_combobox.setCurrentIndex(index)

    @Slot()
    def more_strings_for_chord(self):
        self.highStringLimit = min(self.highStringLimit+1, self.num_strings)
        #print('More: %s!'%self.highStringLimit)
        self.color_notes_by_default()
        self.color_chord_notes(self.chords_combobox.currentData())

    @Slot()
    def less_strings_for_chord(self):
        self.highStringLimit = max(self.highStringLimit-1, 4)
        #print('Less: %s!'%self.highStringLimit)
        self.color_notes_by_default()
        self.color_chord_notes(self.chords_combobox.currentData())

    @Slot()
    def show_chords(self):
        self.color_notes_by_default()
        if self.chords_combobox.currentText() != "":
            self.color_chord_notes(self.chords_combobox.currentData())

    @Slot(int)
    def show_highlighted_chord(self, index):
        self.color_notes_by_default()
        self.color_chord_notes(self.chords_combobox.itemData(index))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎸 Scales Circle Diagram")
        self.neckGeneralView = ''

        self.scaleName = ""
        self.shownScale = list()
        self.scaleLength = 0

        #self.modeName = ""
        self.currentTuningName = ""

        # Set a main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # In which will be a global VBoxLayout
        self.mainVBoxLayout = QVBoxLayout(central_widget)

        # a first horizontal layout for the general tools
        self.topHBoxLayout = QHBoxLayout()
        self.create_scales_combobox(self.topHBoxLayout)
        self.create_reference_degree_combobox(self.topHBoxLayout)
        self.create_degrees_combobox(self.topHBoxLayout)
        self.create_tunings_combobox(self.topHBoxLayout)
        self.create_full_neck_radioButton(self.topHBoxLayout)
        self.full_neck_radioButton.setChecked(False)
        self.mainVBoxLayout.addLayout(self.topHBoxLayout)


        # a second horizontal layout for the max four degrees
        self.midHBoxLayout = QHBoxLayout()
        self.mainVBoxLayout.addLayout(self.midHBoxLayout)

        # Create a first frame for the first Degree to show
        self.degreesFrames = list()
        self.addDegreeFrame(visible=True, name="frame_1")

        # Initialisation
        self.set_scale("Natural")
        self.set_reference_degree("I", 0)
        self.set_arrangement("I", 0)
        self.set_tuning("Standard 6 \tEADGBE")
        self.update()

# -----------------------------------------------------------------------------

    def set_arrangement(self, arrangement, arrIndex):
        print("\nIn set_arrangement to set %s with arrIndex %s" % (arrangement, arrIndex))
        self.arrangementString = arrangement
        self.arrangement = degreeArrangements[arrIndex]
        self.clearDegreeFrames()
        self.setFixedSize(500*len(self.arrangement), 900)
        for i in range(len(self.arrangement)):
            name = "frame_%s"%(1+i)
            self.addDegreeFrame(name=name)
        self.set_reference_degree(self.reference_degree_combobox.currentText(), self.reference_degree_combobox.currentIndex())
        for i in range(len(self.arrangement)):
            print("In set_arrangement to set degree: %s called %s" % (self.arrangement[i], degrees[self.arrangement[i]-1]))
            print("In set_arrangement with self.referenceDegreeIndex: %s" % self.referenceDegreeIndex)
            self.degreesFrames[i].show()
            print('In set_arrangement, frame %s with reference degree %s' % (self.degreesFrames[i].name, self.degreesFrames[i].referenceDegree))
            self.degreesFrames[i].set_degree(self.arrangement[i]-1)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_arrangement(self.arrangement)

    def set_reference_degree(self, degreeName, degreeIndex):
        self.referenceDegreeIndex = degreeIndex
        print("In set_reference_degree with self.referenceDegreeIndex: %s" % self.referenceDegreeIndex)
        for vFrame in self.degreesFrames:
            vFrame.set_reference_degree(degreeName, degreeIndex)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_reference_degree(degreeIndex)

    def set_scale(self, scale_name):
        self.scaleName = scale_name
        self.shownScale = scales[self.scaleName]
        if len(self.shownScale) != self.scaleLength:
            self.scaleLength = len(self.shownScale)
            self.add_compatible_reference_degree_in_Combobox()
        self.scaleLength = len(self.shownScale)
        for vFrame in self.degreesFrames:
            vFrame.set_scale(scale_name)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_scale(self.scaleName)

    def set_tuning(self, tuning_name, init=False):
        self.currentTuning = tunings[tuning_name]
        self.currentTuningName = tuning_name
        for vFrame in self.degreesFrames:
            vFrame.set_tuning(tuning_name, init=init)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_tuning(self.currentTuningName, init=init)

    def toggle_neck_general_view(self):
        if not self.neckGeneralView == '':
            if self.neckGeneralView.isVisible():
                self.neckGeneralView.hide()
            else:
                self.neckGeneralView.show()
        else:
            self.neckGeneralView = NeckWindow(self)
            self.neckGeneralView.set_scale(self.scaleName)
            self.neckGeneralView.set_tuning(self.currentTuningName, init=True)
            self.neckGeneralView.set_reference_degree(self.referenceDegreeIndex)
            self.neckGeneralView.set_arrangement(self.arrangement)
            self.neckGeneralView.setFixedSize(1340, 440)
            self.neckGeneralView.show()
        self.neckGeneralView.refresh()

    def clearDegreeFrames(self):
        for vFrame in self.degreesFrames:
            self.midHBoxLayout.removeWidget(vFrame)
            vFrame.deleteLater()
        self.degreesFrames = list()

    def addDegreeFrame(self, visible=False, name=""):
        #print("\nIn addDegreeFrame...")
        vBoxFrame = CircleAndNeckVBoxFrame(self, 1, visible=visible, name=name)
        self.degreesFrames.append(vBoxFrame)
        vBoxFrame.setFixedSize(483, 834)
        self.midHBoxLayout.addWidget(vBoxFrame)

    def refresh(self):
        for vFrame in self.degreesFrames:
            vFrame.refresh()
        if not self.neckGeneralView == '':
            self.neckGeneralView.refresh()

# -----------------------------------------------------------------------------

    def create_scales_combobox(self, parentLayout):
        self.scales_combobox = QComboBox()
        self.scales_combobox.addItems(scales.keys())
        self.scales_combobox.currentTextChanged.connect(lambda: self.set_scale(self.scales_combobox.currentText()))
        parentLayout.addWidget(self.scales_combobox)

    def create_reference_degree_combobox(self, parentLayout):
        self.reference_degree_combobox = QComboBox()
        #self.reference_degree_combobox.addItems(degrees)
        self.add_compatible_reference_degree_in_Combobox()
        self.reference_degree_combobox.currentTextChanged.connect(lambda: self.set_reference_degree(self.reference_degree_combobox.currentText(), self.reference_degree_combobox.currentIndex()))
        parentLayout.addWidget(self.reference_degree_combobox)

    def create_degrees_combobox(self, parentLayout):
        self.degrees_combobox = QComboBox()
        arrangements = []
        for arrangement in degreeArrangements:
            arrangementStrings = []
            for degree in arrangement:
                 arrangementStrings.append(degrees[degree-1])
            arrangements.append('-'.join(arrangementStrings))
        self.degrees_combobox.addItems(arrangements)
        self.degrees_combobox.currentTextChanged.connect(lambda: self.set_arrangement(self.degrees_combobox.currentText(), self.degrees_combobox.currentIndex()))
        parentLayout.addWidget(self.degrees_combobox)

    def create_tunings_combobox(self, parentLayout):
        self.tunings_combobox = QComboBox()
        self.tunings_combobox.addItems(tunings.keys())
        self.tunings_combobox.currentTextChanged.connect(lambda: self.set_tuning(self.tunings_combobox.currentText()))
        parentLayout.addWidget(self.tunings_combobox)

    def create_full_neck_radioButton(self, parentLayout):
        self.full_neck_radioButton = QRadioButton("Neck window")
        self.full_neck_radioButton.toggled.connect(self.toggle_neck_general_view)
        parentLayout.addWidget(self.full_neck_radioButton)

# -----------------------------------------------------------------------------

    def add_compatible_reference_degree_in_Combobox(self):
        '''
        Adds only the reference degrees present in the current scale.
        If the currently set reference degree is still available in the new scale,
        it is kepts, if not, reference degree is set to I
        '''
        currentReferenceDegree = self.reference_degree_combobox.currentText()
        foundCurrentReferenceDegree = False
        for i in range(self.reference_degree_combobox.count()):
            self.reference_degree_combobox.removeItem(0)
        for i in range(len(degrees)):
            if i < self.scaleLength:
                self.reference_degree_combobox.addItem(degrees[i])
                if (degrees[i] == currentReferenceDegree) and (not foundCurrentReferenceDegree):
                    foundCurrentReferenceDegree = True
        if foundCurrentReferenceDegree:
            self.reference_degree_combobox.setCurrentText(currentReferenceDegree)

    def closeEvent(self, event):
        if not self.neckGeneralView == '':
            self.neckGeneralView.close()
        event.accept()

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setFixedSize(500, 900)
    window.show()


    app.exec()

# -----------------------------------------------------------------------------
