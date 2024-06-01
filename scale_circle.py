# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsLineItem
from PySide6.QtWidgets import QDialog, QPushButton, QCheckBox, QRadioButton, QComboBox, QSlider, QMenu, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QPointF, QRectF, QLineF, QSizeF, Slot
from PySide6.QtGui import QPolygonF, QPen, QBrush, QPainter, QAction, QFont, QColor, QFontMetrics
import sys, math, itertools

from scale_circle_library import fretZeroNoteItem, NoteItem, TriangleNoteItem, linkModesToScales
from catalogs import notes, scales, modes, alterations, tunings, stringSets, stringGaugeFromNumberOfString, chords, enrichments, semitonesToConsiderByNumberOfStrings, degrees, degreeArrangements
from Inlays import NoBorderEllipseItem, inlays, sideInlays, customColours

# -----------------------------------------------------------------------------

SCALE_CIRCLE_RADIUS = 160
FRET_SPACING = 50
FRET_OVERSHOOT = 4
STRING_SPACING = 30

GRAPHICSVIEW_WIDTH = 459
GRAPHICSVIEW_HEIGHT = 366

NECK_WIDENING = 5

FONT = 'Garamond Premier Pro'
DEGREE_COLOUR = 'Destorm'

ZOOM = 1.0


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class NeckWindow(QDialog):
    def __init__(self, mainWindowInstance, scale_factor=1.0):
        super().__init__()
        self.setWindowTitle("🎸 Neck general view")
        self.mainWindowInstance = mainWindowInstance
        self.scale_factor = scale_factor

        self.once = True
        self.neckSceneRect = ''

        self.scaleName = ""
        self.scale = list()
        self.scaleLength = 0

        self.modeIndex = 0
        self.modeScale = list()

        self.rootNote = ''

        self.currentTuningName = ""
        self.lowStringNoteIndex = 4
        self.currentArrangement = (1,)

        self.num_frets = 24
        self.first_root_position = -1
        self.num_strings = 0

        self.colour_degrees = DEGREE_COLOUR
        self.fanBase = 0
        self.fanHeight = 1000000

        self.labelFont = QFont()
        self.labelFont.setPointSize(20*self.scale_factor)
        self.labelFont.setFamily(FONT)

        self.create_gui()

        self.create_graphic_item_groups()

        self.identifiedNotes = dict()

        # Initialisation
        self.set_tuning(self.mainWindowInstance.currentTuningName, init=True)
        self.set_scale(self.mainWindowInstance.scaleName)


# -----------------------------------------------------------------------------

    def create_gui(self):
        # Add neck_graphics_view to layout
        self.mainVBoxLayout = QVBoxLayout()
        self.topHBoxLayout = QHBoxLayout()
        self.mainVBoxLayout.addLayout(self.topHBoxLayout)

        self.create_neck_graphic_view()

        self.create_option_buttons()
        self.create_root_note_combobox()
        self.create_inlays_combobox()
        self.create_degrees_colours_combobox()

        self.mainVBoxLayout.addWidget(self.neck_graphics_view)
        self.setLayout(self.mainVBoxLayout)

    def create_option_buttons(self):
        '''
        '''
        padding = 15
        self.show_root_checkbox = QCheckBox("Show roots")
        self.show_root_checkbox.setChecked(True)
        self.show_root_checkbox.toggled.connect(self.draw_neck)

        self.show_tuning_checkbox = QCheckBox("Show tuning")
        self.show_tuning_checkbox.setChecked(False)
        self.show_tuning_checkbox.toggled.connect(self.draw_neck)

        self.fan_frets_checkbox = QCheckBox("Fanned frets")
        self.fan_frets_checkbox.setChecked(False)
        self.fan_frets_checkbox.toggled.connect(self.draw_neck)

        self.reg_frets_checkbox = QCheckBox("regular frets")
        self.reg_frets_checkbox.setChecked(True)
        self.reg_frets_checkbox.toggled.connect(self.draw_neck)

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.show_tuning_checkbox)
        vBoxLayout.addWidget(self.show_root_checkbox)
        vBoxLayout.addWidget(self.fan_frets_checkbox)
        vBoxLayout.addWidget(self.reg_frets_checkbox)
        self.topHBoxLayout.addLayout(vBoxLayout)

        self.fan_apex_slider = QSlider(Qt.Horizontal)
        self.fan_apex_slider.setMinimum(0)
        self.fan_apex_slider.setMaximum(FRET_SPACING   * (self.num_frets + 1) *self.scale_factor)
        self.fan_apex_slider.setValue(FRET_SPACING * self.scale_factor)
        self.fan_apex_slider.setGeometry(-padding*self.scale_factor, -2*STRING_SPACING*self.scale_factor, (FRET_SPACING*(self.num_frets)+(2*padding))*self.scale_factor, STRING_SPACING*self.scale_factor)
        self.fan_apex_slider.setStyleSheet("background: transparent;\nhandle: { width: %spx; height: %spx; margin: -%spx 0;}"%(5*self.scale_factor, 5**self.scale_factor, 3*self.scale_factor))
        self.fan_apex_slider.valueChanged.connect(self.draw_neck)
        self.fan_apex_slider.hide()
        self.neck_scene.addWidget(self.fan_apex_slider)

    def create_root_note_combobox(self):
        label = QLabel("Root note:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        self.root_note_combobox = QComboBox()
        self.root_note_combobox.addItems(notes.keys())
        self.rootNote = "E"
        self.root_note_combobox.setCurrentText(self.rootNote)
        self.root_note_combobox.currentTextChanged.connect(lambda: self.setRootNote())
        self.root_note_combobox.highlighted.connect(self.show_highlighted_root)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.root_note_combobox)
        self.topHBoxLayout.addLayout(vBoxLayout)

    def create_inlays_combobox(self):
        label = QLabel("Inlays:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        self.inlays_combobox = QComboBox()
        self.inlays_combobox.addItems(inlays.keys())
        self.inlays_combobox.setCurrentText(".strandberg＊")
        self.inlays_combobox.currentTextChanged.connect(lambda: self.draw_neck())
        self.inlays_combobox.highlighted.connect(self.show_highlighted_inlays)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.inlays_combobox)
        self.topHBoxLayout.addLayout(vBoxLayout)

    def create_degrees_colours_combobox(self):
        label = QLabel("Colours:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        self.degrees_colours_combobox = QComboBox()
        self.degrees_colours_combobox.addItems(customColours.keys())
        self.degrees_colours_combobox.setCurrentText(DEGREE_COLOUR)
        self.degrees_colours_combobox.currentTextChanged.connect(lambda: self.set_degrees_colour())
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.degrees_colours_combobox)
        self.topHBoxLayout.addLayout(vBoxLayout)

    def create_neck_graphic_view(self):
        self.neck_graphics_view = QGraphicsView()
        self.neck_graphics_view.setRenderHint(QPainter.Antialiasing)
        self.neck_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.neck_graphics_view.viewport().palette()
        palette.setColor(self.neck_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.neck_graphics_view.viewport().setPalette(palette)

        self.neck_scene = QGraphicsScene()
        self.neck_graphics_view.setScene(self.neck_scene)

    def create_graphic_item_groups(self):
        # Groups to help manage graphic items
        self.neck_diagram_background_group = QGraphicsItemGroup()
        self.neck_diagram_inlays_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group.setHandlesChildEvents(False)
        self.neck_diagram_colours_group = QGraphicsItemGroup()
        self.neck_diagram_colours_group.setHandlesChildEvents(False)
        self.neck_diagram_degrees_group = QGraphicsItemGroup()
        self.neck_diagram_tuning_group = QGraphicsItemGroup()

# -----------------------------------------------------------------------------

    def set_scale(self, scale_name):
        '''

        '''
        self.scaleName = scale_name
        self.scale = scales[self.scaleName]
        self.scaleLength = len(self.scale)

        self.modeIndex = self.modeIndex%self.scaleLength
        self.set_modeScale()

        self.draw_neck()
        self.label_degrees_on_neck()

    def set_mode(self, modeIndex):
        self.modeIndex = modeIndex

        self.set_modeScale()

        self.draw_neck()
        self.label_degrees_on_neck()

    def set_modeScale(self):
        self.modeScale = self.scale
        for i in range(self.modeIndex):
            self.rotate_mode_scale(+1)

    def set_arrangement(self, arrangement):
        self.currentArrangement = arrangement
        self.label_degrees_on_neck()

    def set_tuning(self, tuning_name, init=False):
        '''
        Takes a tuning name and set it
        If not in init phase, the entire neck is redrawn
        '''
        self.currentTuningName = tuning_name
        self.currentTuning = tunings[self.currentTuningName]
        self.num_strings = len(self.currentTuning)
        if not init:
            self.setRootNote()

    def setRootNote(self, rootNoteValue=-1):
        # All this will be useful to draw a more realistic neck
        tuningNotesComposition = self.currentTuningName.split('\t')[1].split()
        notesByIndex = {value: key for key, value in notes.items()}
        firstTuningNote = ''
        if len(tuningNotesComposition)>0:
            if tuningNotesComposition[0][1] == '♯':
                #print("debug 0")
                firstTuningNote = notesByIndex[notes[tuningNotesComposition[0][0]]+1]
            elif tuningNotesComposition[0][1] == '♭':
                #print("debug 1")
                firstTuningNote = notesByIndex[notes[tuningNotesComposition[0][0]]-1]
            else:
                #print("debug 3")
                firstTuningNote = tuningNotesComposition[0][0]
        firstTuningNoteValue = notes[firstTuningNote]
        self.lowStringNoteIndex = firstTuningNoteValue
        if rootNoteValue == -1:
            rootNoteValue = notes[self.root_note_combobox.currentText()]
        self.rootNote = self.root_note_combobox.currentText()
        self.first_root_position = (rootNoteValue - firstTuningNoteValue)-1
        self.mainWindowInstance.refresh()

        self.draw_neck()
        self.label_degrees_on_neck()

    def set_degrees_colour(self):
        self.colour_degrees = self.degrees_colours_combobox.currentText()
        self.label_degrees_on_neck()
        self.mainWindowInstance.changeColourDegrees(self.colour_degrees)
        self.changeNotesColours()

# -----------------------------------------------------------------------------

    def rotate_mode_scale(self, rotation):
        self.modeScale = sorted([(inScale +(12-self.modeScale[rotation]))%12 for inScale in self.modeScale])

# -----------------------------------------------------------------------------

    def transFan(self, x, y):
        '''
        Displaces the x coordinates according to the current x and y coordinates
        and the apex of the fanned frets, situated at base length from the nut and
        height from the center of the neck middle line, positive on the High E string
        side.
        Base can be modified with a QSlider
        '''
        halfNeckHeight = ((STRING_SPACING * (self.num_strings - 1))/2)*self.scale_factor
        return x - (self.fanBase*self.scale_factor-x)*(y-halfNeckHeight)/(self.fanHeight*self.scale_factor)

    def draw_neck(self, inlaysType=False):
        '''
        General function called when the QSlider value changes.
        '''
        if self.fan_frets_checkbox.isChecked():
            self.fanBase   = self.fan_apex_slider.value()
            self.fanHeight = (60 - (self.num_strings-6)*20) * (STRING_SPACING * (self.num_strings - 1) * self.scale_factor)
            self.fan_apex_slider.show()
            self.inlays_combobox.setCurrentText(".strandberg＊")
        else:
            self.fanBase   = 0
            self.fanHeight = 1000000*self.scale_factor
            self.fan_apex_slider.hide()
        self.draw_notes_on_neck(inlaysType=inlaysType)
        self.set_degrees_colour()

    def draw_neck_background(self, rootUndefined=True, inlaysType=False):
        '''
        Draws all the elements of the neck except the notes
        '''
        self.clear_group(self.neck_diagram_background_group)
        self.clear_group(self.neck_diagram_inlays_group)
        self.clear_group(self.neck_diagram_tuning_group)

        # Draw neck borders
        self.draw_neck_borders()

        # Draw frets
        self.draw_frets()

        # Draw inlays
        if not inlaysType:
            inlaysType = self.inlays_combobox.currentText()
        self.draw_inlays(type=inlaysType)

        # Draw strings
        self.draw_strings()

        if self.show_tuning_checkbox.isChecked():
            self.draw_tuning()

        if self.neck_diagram_inlays_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_inlays_group)
        if self.neck_diagram_tuning_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_tuning_group)
        if self.neck_diagram_background_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_background_group)

    def draw_neck_borders(self):
        neck_width  = FRET_SPACING   * (self.num_frets + 1)*self.scale_factor
        neck_height = STRING_SPACING * (self.num_strings - 1)*self.scale_factor
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]
        highStringThicknessAllowance = (strings_thickness[0]/20)*self.scale_factor
        lowStringThicknessAllowance = (strings_thickness[-1]/20)*self.scale_factor

        darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        darkGray_pen.setWidth(0.5*self.scale_factor)

        #Draw borders of neck
        fretOvershoot = (FRET_OVERSHOOT+1)*self.scale_factor
        # coords of begin and end of top neck border
        xBegin = -15*self.scale_factor
        yBegin = -fretOvershoot-highStringThicknessAllowance
        xEnd = neck_width
        yEnd = -fretOvershoot-NECK_WIDENING*self.scale_factor-highStringThicknessAllowance
        # correction for fanning at the nut
        xBegin = self.transFan(xBegin, yBegin)

        top = QGraphicsLineItem(xBegin, yBegin, xEnd, yEnd)
        top.setPen(darkGray_pen)
        self.neck_diagram_background_group.addToGroup(top)

        # coords of begin and end of bottom neck border
        xBegin = -15*self.scale_factor
        yBegin = neck_height+fretOvershoot+lowStringThicknessAllowance
        xEnd = neck_width
        yEnd = neck_height+fretOvershoot+NECK_WIDENING*self.scale_factor+lowStringThicknessAllowance
        # correction for fanning at the nut
        xBegin = self.transFan(xBegin, yBegin)

        bottom = QGraphicsLineItem(xBegin, yBegin, xEnd, yEnd)
        bottom.setPen(darkGray_pen)
        self.neck_diagram_background_group.addToGroup(bottom)

    def draw_frets(self):
        neck_height = (STRING_SPACING * (self.num_strings - 1))*self.scale_factor
        neck_length = FRET_SPACING * (self.num_frets + 1)*self.scale_factor
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]
        highStringThicknessAllowance = (strings_thickness[0]/20)*self.scale_factor
        lowStringThicknessAllowance = (strings_thickness[-1]/20)*self.scale_factor

        # Draw fret 0
        fret_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        fret_darkGray_pen.setWidth(4*self.scale_factor)      # Set the pen width
        x = 0
        top  = -FRET_OVERSHOOT*self.scale_factor-highStringThicknessAllowance
        bottom = neck_height+FRET_OVERSHOOT*self.scale_factor+lowStringThicknessAllowance
        xTop = self.transFan(x, top)
        xBottom = self.transFan(x, bottom)
        line = QGraphicsLineItem(xTop, top, xBottom, bottom)
        line.setPen(fret_darkGray_pen)
        self.neck_diagram_background_group.addToGroup(line)

        # draw nut
        fret_darkGray_pen.setWidth(10*self.scale_factor)      # Set the pen width
        x = -15*self.scale_factor
        top = (-FRET_OVERSHOOT+4)*self.scale_factor-highStringThicknessAllowance
        bottom = neck_height+(FRET_OVERSHOOT-4)*self.scale_factor+lowStringThicknessAllowance
        xTop = self.transFan(x, top)
        xBottom = self.transFan(x, bottom)
        line = QGraphicsLineItem(xTop, top, xBottom, bottom)
        line.setPen(fret_darkGray_pen)
        self.neck_diagram_background_group.addToGroup(line)

        # Draw frets
        fret_darkGray_pen.setWidth(3*self.scale_factor)      # Set the pen width
        for i in range(0, self.num_frets + 1):
            if self.reg_frets_checkbox.isChecked():
                x = i * FRET_SPACING * self.scale_factor
            else:
                x = 4/3*neck_length - (4/3*neck_length / (2**(i/12)))

            widthAdjustment = NECK_WIDENING*(i/(self.num_frets + 1))*self.scale_factor
            top    = -(FRET_OVERSHOOT*self.scale_factor + widthAdjustment + highStringThicknessAllowance)
            # visual debug
            if i%12 == 0:
                top = top -20
            bottom = neck_height+(FRET_OVERSHOOT*self.scale_factor + widthAdjustment + lowStringThicknessAllowance)
            xTop = self.transFan(x, top)
            xBottom = self.transFan(x, bottom)
            line = QGraphicsLineItem(xTop, top, xBottom, bottom)
            line.setPen(fret_darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

    def draw_inlays(self, type="black_dot"):
        stringNumbersAdjustmentRatio = self.num_strings/6.0
        neck_height = STRING_SPACING * (self.num_strings - 1)*self.scale_factor
        neck_length = FRET_SPACING * (self.num_frets + 1)*self.scale_factor
        halfNeckHeight = neck_height/2

        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]
        highStringThicknessAllowance = (strings_thickness[0]/20)*self.scale_factor
        lowStringThicknessAllowance = (strings_thickness[-1]/20)*self.scale_factor

        for i in range(0, self.num_frets):
            adjustmentForFret = (NECK_WIDENING*i/self.num_frets)*self.scale_factor
            # Neck Inlays
            if i in inlays[type].keys():
                for inlayMark in inlays[type][i]:
                    if self.reg_frets_checkbox.isChecked():
                        x = ((FRET_SPACING*inlayMark['delta_x']) + i * FRET_SPACING)*self.scale_factor
                    else:
                        x = 4/3*neck_length - (4/3*neck_length / (2**(i/12)))
                        nextX = 4/3*neck_length - (4/3*neck_length / (2**((1+i)/12)))
                        thisFretSpacing = nextX - x
                        x = (x + ((thisFretSpacing*inlayMark['delta_x']))) * self.scale_factor

                    if inlayMark['delta_y'] < 0:
                        adjustmentForFret = -adjustmentForFret
                    elif inlayMark['delta_y'] == 0:
                        adjustmentForFret = 0
                    y = halfNeckHeight + halfNeckHeight*inlayMark['delta_y']*stringNumbersAdjustmentRatio + adjustmentForFret
                    newX = self.transFan(x, y)
                    point = QPointF(newX, y)
                    inlay = inlayMark['type'](QRectF(point - QPointF(inlayMark['size_x']/2*self.scale_factor, inlayMark['size_y']/2*self.scale_factor), QSizeF(inlayMark['size_x']*self.scale_factor, inlayMark['size_y']*self.scale_factor)))
                    inlay.setBrush(inlayMark['color'])
                    if 'pen' in inlayMark.keys():
                        inlay.setPen(inlayMark['pen'])
                    self.neck_diagram_inlays_group.addToGroup(inlay)
            # Side inlays
            if i in sideInlays[type].keys():
                for inlayMark in sideInlays[type][i]:
                    if self.reg_frets_checkbox.isChecked():
                        x = ((FRET_SPACING*inlayMark['delta_x']) + i * FRET_SPACING)*self.scale_factor
                    else:
                        x = 4/3*neck_length - (4/3*neck_length / (2**(i/12)))
                        nextX = 4/3*neck_length - (4/3*neck_length / (2**((1+i)/12)))
                        thisFretSpacing = nextX - x
                        x = (x + ((thisFretSpacing*inlayMark['delta_x']))) * self.scale_factor

                    y = halfNeckHeight + halfNeckHeight*inlayMark['delta_y'] + abs(adjustmentForFret) + lowStringThicknessAllowance
                    newX = self.transFan(x, y)
                    point = QPointF(newX, y)
                    inlay = inlayMark['type'](QRectF(point - QPointF(inlayMark['size_x']/2*self.scale_factor, inlayMark['size_y']/2*self.scale_factor), QSizeF(inlayMark['size_x']*self.scale_factor, inlayMark['size_y']*self.scale_factor)))
                    inlay.setBrush(inlayMark['color'])
                    if 'pen' in inlayMark.keys():
                        inlay.setPen(inlayMark['pen'])
                    self.neck_diagram_inlays_group.addToGroup(inlay)

    def draw_strings(self):
        neck_width  = FRET_SPACING   * (self.num_frets + 1)*self.scale_factor
        neck_height = STRING_SPACING * (self.num_strings - 1)*self.scale_factor
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]
        string_darkGray_pen = QPen(Qt.darkGray)  # Set the pen color

        # Draw strings
        for i in range(self.num_strings):
            xBegin = -15*self.scale_factor
            yBegin = i * STRING_SPACING * self.scale_factor
            widthAdjustmentProportion = (yBegin-(neck_height/2))/(neck_height/2)
            xEnd = neck_width
            yEnd = yBegin+(widthAdjustmentProportion*NECK_WIDENING)

            xBegin = self.transFan(xBegin, yBegin)

            line = QGraphicsLineItem(xBegin, yBegin, xEnd, yEnd)
            string_darkGray_pen.setWidth((strings_thickness[i]/10.0)*self.scale_factor)
            line.setPen(string_darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

    def draw_notes_on_neck(self, inlaysType=False):
        '''
        draws all the scale notes on the entire neck
        '''
        if self.once:
            self.neckSceneRect = self.neck_scene.sceneRect()
        if not isinstance(inlaysType, str):
            inlaysType = self.inlays_combobox.currentText()

        neck_width  = FRET_SPACING   * (self.num_frets + 1)*self.scale_factor
        neck_height = STRING_SPACING * (self.num_strings - 1)*self.scale_factor


        self.draw_neck_background(inlaysType=inlaysType)

        self.keepNotesColouringParameters()
        self.identifiedNotes = {each: list() for each in range(12)}
        self.clear_group(self.neck_diagram_notes_group)

        adjustmentForString = 0.0
        adjustmentForFret = 0.0
        noteRadius = (STRING_SPACING / 2.0) *self.scale_factor
        halfNeckHeight = neck_height/2

        zeroFretNoteXadjustment = 13*self.scale_factor

        base   = FRET_SPACING * self.scale_factor
        height = neck_height * 20

        # from low to high strings
        for i in range(self.num_strings):
            y = neck_height - (i * STRING_SPACING*self.scale_factor)
            adjustmentForString = (y-halfNeckHeight)/halfNeckHeight #(for a 6 strings: -1, -0.6, -0.2, 0.2, 0.6, 1)
            # from low to high frets
            for j in range(-1, self.num_frets):
                if self.reg_frets_checkbox.isChecked():
                    x = (j * FRET_SPACING*self.scale_factor) + (FRET_SPACING*self.scale_factor / 2.0)
                else:
                    x = 4/3*neck_width - (4/3*neck_width / (2**(j/12)))
                    nextX = 4/3*neck_width - (4/3*neck_width / (2**((1+j)/12)))
                    thisFretSpacing = nextX - x
                    x = x + ((thisFretSpacing / 2.0))

                adjustmentForFret = (j+.5)/(self.num_frets) #(should go 0 to 1)
                semitone_text = (self.currentTuning[i] + j) - self.first_root_position
                if semitone_text % 12 in self.modeScale:
                    adjustment = adjustmentForString * adjustmentForFret
                    pixAdjustment = NECK_WIDENING * adjustment

                    newY = y + pixAdjustment
                    newX = self.transFan(x, newY)

                    point = QPointF(newX, newY)
                    if j == -1:
                        # Notes generated by fret 0, shown as rectangles just below fret 0
                        yTop = newY - STRING_SPACING*self.scale_factor/2
                        yBot = newY + STRING_SPACING*self.scale_factor/2
                        xLeft = x + zeroFretNoteXadjustment
                        xRight = x + zeroFretNoteXadjustment + noteRadius/2
                        xTopLeft = self.transFan(xLeft, yTop)
                        xTopRight = self.transFan(xRight, yTop)
                        xBotLeft = self.transFan(xLeft, yBot)
                        xBotRight = self.transFan(xRight, yBot)
                        rectangle = QPolygonF()
                        rectangle.append(QPointF(xTopLeft,yTop))
                        rectangle.append(QPointF(xTopRight,yTop))
                        rectangle.append(QPointF(xBotRight,yBot))
                        rectangle.append(QPointF(xBotLeft,yBot))
                        note_point = fretZeroNoteItem(rectangle, embeddingWidget=self)

                    elif self.show_root_checkbox.isChecked() and semitone_text % 12 == self.modeScale[0]:
                        # Root Notes potentially shown as triangles
                        triangle = QPolygonF()
                        triangle.append(QPointF(noteRadius, 0))  # Top point
                        triangle.append(QPointF(STRING_SPACING*self.scale_factor, STRING_SPACING*self.scale_factor))  # Bottom right point
                        triangle.append(QPointF(0, STRING_SPACING*self.scale_factor))  # Bottom left point
                        note_point = TriangleNoteItem(triangle, embeddingWidget=self)
                        note_point.setPos(newX - noteRadius, newY - noteRadius)

                    else:
                        # playable Notes shown as cercles
                        note_point = NoteItem(QRectF(point - QPointF(noteRadius, noteRadius), QSizeF(STRING_SPACING*self.scale_factor, STRING_SPACING*self.scale_factor)), embeddingWidget=self)

                    note_point.note = semitone_text%12
                    note_point.setPen(QPen(Qt.transparent))
                    self.identifiedNotes[semitone_text % 12].append([note_point, semitone_text, i, j])

                    self.neck_diagram_notes_group.addToGroup(note_point)
        self.color_notes_by_default()
        self.applyNotesColouringParameters()
        if self.neck_diagram_notes_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_notes_group)
        if self.once:
            self.once = False
        else:
            self.center_neck_view()

    def draw_tuning(self):
        '''
        setting the usual values and fonts
        '''
        neck_height = STRING_SPACING*self.scale_factor * (self.num_strings - 1)
        halfNeckHeight = neck_height/2
        noteRadius = STRING_SPACING*self.scale_factor / 2.0
        notesByIndex = {value: key for key, value in notes.items()}
        tuningXPosition = (-2 * FRET_SPACING*self.scale_factor) + (FRET_SPACING*self.scale_factor / 2.0)

        font = QFont()
        font.setFamily(FONT)
        font.setPointSize(.8*(STRING_SPACING*self.scale_factor))
        brush = QBrush(Qt.white, bs=Qt.SolidPattern)

        self.clear_group(self.neck_diagram_tuning_group)

        referenceVFrame = self.mainWindowInstance.degreesFrames[0]
        colourCorrection = self.scale[referenceVFrame.degreeIndex]-self.scale[self.modeIndex]

        for i in range(self.num_strings):
            # from low to high frets
            x = tuningXPosition
            y = neck_height - (i * STRING_SPACING*self.scale_factor)
            adjustmentForString = (y-halfNeckHeight)/halfNeckHeight #(for a 6 strings: -1, -0.6, -0.2, 0.2, 0.6, 1)
            adjustmentForFret = (-.5)/(self.num_frets) #(should go 0 to 1)
            adjustment = adjustmentForString * adjustmentForFret
            pixAdjustment = NECK_WIDENING * adjustment

            semitone_text = (self.currentTuning[i] -1) - self.first_root_position
            note_text = notesByIndex[(self.lowStringNoteIndex + self.currentTuning[i])%12]

            colourAngle = ((self.currentTuning[i] - self.first_root_position - colourCorrection)*math.pi/6.0)
            brush.setColor(referenceVFrame.generate_colour_for_angle(colourAngle, includeRotation=True, colours=customColours[self.colour_degrees]))

            newY = y + pixAdjustment
            newX = self.transFan(x, newY)

            point = QPointF(newX, newY)

            text_item = QGraphicsSimpleTextItem(note_text)
            text_item.setFont(font)
            text_item.setPos(point - QPointF(text_item.boundingRect().width()/2.0, text_item.boundingRect().height()/2.0))
            text_item.setFlags(QGraphicsItem.ItemIgnoresTransformations)

            self.neck_diagram_tuning_group.addToGroup(text_item)

    def label_degrees_on_neck(self):
        neck_width  = FRET_SPACING   * (self.num_frets + 1)*self.scale_factor
        neck_height = STRING_SPACING*self.scale_factor * (self.num_strings - 1)

        self.identifiedDegrees = {each: list() for each in range(12)}
        self.clear_group(self.neck_diagram_degrees_group)
        self.clear_group(self.neck_diagram_colours_group)

        font = QFont()
        font.setFamily(FONT)
        font.setPointSize(.95*(STRING_SPACING*self.scale_factor))

        brush = QBrush(Qt.white, bs=Qt.SolidPattern)

        # Label for used Degrees in arrangement
        for j in range(-1, self.num_frets):
            if self.reg_frets_checkbox.isChecked():
                x = (FRET_SPACING*self.scale_factor/2.0) + j * FRET_SPACING*self.scale_factor
            else:
                x = 4/3*neck_width - (4/3*neck_width / (2**(j/12)))
                nextX = 4/3*neck_width - (4/3*neck_width / (2**((1+j)/12)))
                thisFretSpacing = nextX - x
                x = x + ((thisFretSpacing / 2.0))

            y = neck_height + 2.1 * STRING_SPACING*self.scale_factor

            yTop = y - STRING_SPACING/2*self.scale_factor
            yBot = y + STRING_SPACING/2*self.scale_factor
            xLeft = x-FRET_SPACING/2*self.scale_factor
            xRight = x+FRET_SPACING/2*self.scale_factor

            if not self.reg_frets_checkbox.isChecked():
                if j==-1:
                    xLeft = x
                else:
                    xLeft = x - thisFretSpacing/2.0
                print('xleft: %s'%xLeft)
                xRight = x+thisFretSpacing/2.0

            xTopLeft = self.transFan(xLeft, yTop)
            xTopRight = self.transFan(xRight, yTop)
            xBotLeft = self.transFan(xLeft, yBot)
            xBotRight = self.transFan(xRight, yBot)
            # better position first label in-f any
            if not self.reg_frets_checkbox.isChecked() and j==-1:
                x = xLeft + (xRight - xLeft)/2.0
            xLabel = self.transFan(x, y)

            rectangle = QPolygonF()
            rectangle.append(QPointF(xTopLeft,yTop))
            rectangle.append(QPointF(xTopRight,yTop))
            rectangle.append(QPointF(xBotRight,yBot))
            rectangle.append(QPointF(xBotLeft,yBot))

            colorect = fretZeroNoteItem(rectangle, embeddingWidget=self)

            referenceVFrame = self.mainWindowInstance.degreesFrames[0]
            colourCorrection = self.scale[referenceVFrame.degreeIndex]-self.scale[self.modeIndex]
            colourAngle = ((self.currentTuning[0] + j - self.first_root_position - colourCorrection)*math.pi/6.0)

            brush.setColor(referenceVFrame.generate_colour_for_angle(colourAngle, includeRotation=True, colours=customColours[self.colour_degrees]))
            colorect.setBrush(brush)
            colorect.setPen(Qt.NoPen)

            self.neck_diagram_colours_group.addToGroup(colorect)

            semitone = (self.currentTuning[0] + j) - self.first_root_position
            colorect.note = semitone%12
            self.identifiedNotes[semitone%12].append([colorect, semitone, -1, j])
            if (semitone%12 in self.modeScale) and (self.first_root_position <= j <= self.num_frets - self.first_root_position):
                #print("j: %s"%j)
                point = QPointF(xLabel, y+3)

                # Creation of label object for the note
                degreeLabel = degrees[(self.modeScale.index(semitone%12))%self.scaleLength]
                text_item = QGraphicsSimpleTextItem(degreeLabel)
                text_item.setFont(font)
                text_item.setPos(point - QPointF(text_item.boundingRect().width()/2.0, text_item.boundingRect().height()/2.0))
                text_item.setFlags(QGraphicsItem.ItemIgnoresTransformations)
                # We add the label object to the record of the note
                self.identifiedDegrees[semitone%12].append([text_item, semitone, 0, j])

                self.neck_diagram_degrees_group.addToGroup(text_item)

        self.color_degrees(firstOnly=False)

        if self.neck_diagram_colours_group not in self.neck_scene.items():
            self.neck_scene.addItem(self.neck_diagram_colours_group)
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

    def keepNotesColouringParameters(self):
        self.notesColouringParameters = dict()
        for semitone_on_octave in self.identifiedNotes.keys():
            self.notesColouringParameters[semitone_on_octave] = list()
            for (note, semitone, i, j) in self.identifiedNotes[semitone_on_octave]:
                continuouslyColoured = note.continuouslyColoured
                originalColour = note.originalColour
                colour = note.colour
                self.notesColouringParameters[semitone_on_octave].append((semitone, i, j, continuouslyColoured, originalColour, colour))

    def applyNotesColouringParameters(self):
        for semitone_on_octave in self.identifiedNotes.keys():
            for (note, semitone, i, j) in self.identifiedNotes[semitone_on_octave]:
                if semitone_on_octave in self.notesColouringParameters.keys():
                    for (semitone_old, i_old, j_old, continuouslyColoured, originalColour, colour) in self.notesColouringParameters[semitone_on_octave]:
                        if semitone==semitone_old and i==i_old and j==j_old:
                            note.continuouslyColoured = continuouslyColoured
                            note.originalColour = originalColour
                            note.colour = colour

    def color_notes_by_default(self):
        transblack = QColor(Qt.black)
        transblack.setAlpha(128)
        for note in self.identifiedNotes.keys():
            for (note_point, semitone_text, string, fret) in self.identifiedNotes[note]:
                note_point.setBrush(transblack)

    def color_degrees(self, firstOnly=True):
        white_pen = QPen(Qt.white)
        for semiTone in self.identifiedDegrees.keys():
            first = True
            for (text_item, semitone_text, string, fret) in self.identifiedDegrees[semiTone]:
                if first:
                    currentRelativeDegree = ((self.modeScale.index(semiTone))%self.scaleLength) + 1
                    if (currentRelativeDegree in self.currentArrangement):
                        text_item.setBrush(Qt.white)
                        text_item.setPen(white_pen)
                    else:
                        text_item.hide()
                    if firstOnly:
                        first = False
                else:
                    text_item.hide()

    def changeNotesColours(self):
        for semitone_on_octave in self.identifiedNotes.keys():
            for (note, semitone, i, j) in self.identifiedNotes[semitone_on_octave]:
                if i == -1:
                    color = note.brush().color()
            for (note, semitone, i, j) in self.identifiedNotes[semitone_on_octave]:
                if i != -1:
                    note.colourNotes()
                    note.uncolourNotesConditionally()

    def center_neck_view(self):
        '''
        '''
        # Get the bounding rectangle of all items in the scene
        rect = self.neck_scene.itemsBoundingRect()
        # Calculate the center point of the bounding rectangle
        self.setFixedSize(self.width(), (480 + (self.num_strings-6)*STRING_SPACING)*self.scale_factor)
        center = rect.center()
        # Get the size of the viewport
        view_size = self.neck_graphics_view.viewport().size()
        # Calculate the new position for the scene
        scene_pos = center - QPointF(view_size.width() / 2, view_size.height() / 2)
        # Set the new position for the scene
        self.neck_scene.setSceneRect(scene_pos.x(), scene_pos.y(), view_size.width(), view_size.height())
        self.neck_graphics_view.viewport().update()

    def keyPressEvent(self, event):
        self.mainWindowInstance.keyPressEvent(event)

    def refresh(self, scale_factor=1.0):
        self.scale_factor = scale_factor
        padding = 15
        self.fan_apex_slider.setGeometry(-padding*self.scale_factor, -2*STRING_SPACING*self.scale_factor, (FRET_SPACING*(self.num_frets)+(2*padding))*self.scale_factor, STRING_SPACING*self.scale_factor)
        self.fan_apex_slider.setStyleSheet("background: transparent;\nhandle: { width: %spx; height: %spx; margin: -%spx 0;}"%(5*self.scale_factor, 5**self.scale_factor, 3*self.scale_factor))

        self.draw_neck()
        self.mainVBoxLayout.update()
        self.update()
        self.center_neck_view()

    def closeEvent(self, event):
        self.mainWindowInstance.full_neck_radioButton.setChecked(False)
        event.accept()

    @Slot(int)
    def show_highlighted_root(self, index):
        self.setRootNote(rootNoteValue=index)

    @Slot(int)
    def show_highlighted_inlays(self, index):
        self.draw_neck(inlaysType=self.inlays_combobox.itemText(index))







# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class CircleAndNeckVBoxFrame(QFrame):
    def __init__(self, topApp, degree=1, visible=False, name="frame0", scale_factor=1.0):
        super().__init__()

        # The app in which this widget lives (and must have access to its parameters)
        self.topApp = topApp
        self.name = name
        self.scale_factor = scale_factor

        self.once = True
        self.minimumNumberLowerStringsNumber = 4
        self.maximumNumberHigherStringsNumber = 3
        self.highStringLimit=4
        self.lowStringLimit=1
        self.enrichedChords = {}
        self.maximum_semitone_difference_in_tuning = 0

        # In the datamodel, degrees in scale are recorded as 1 to 7
        # in the code, we'll use indexes (0 to 6) so we can %7 on them
        # the reference degree is the root position in the scale
        # the current degree is the used degree of the scale in the arrangement
        self.degreeIndex = degree - 1
        self.degreeRotation = 0

        self.scaleName = ""
        self.shownScale = list()
        self.scaleLength = 0
        self.notesOnCircle = {}

        self.modeIndex = 0
        self.modeRotation = 0
        self.modeScale = list()

        self.colour_degrees = self.topApp.colour_degrees

        self.create_gui()

        self.create_graphic_item_groups()

        self.identifiedNotes = {}

        self.chordIndex = 0
        self.chord_positions = list()

        # Draw circle and guitar neck backgrounds
        self.draw_scale_circle()

        # Initialisation
        self.set_tuning("Standard 6 \tEADGBE", init=True)
        self.set_scale("Natural")

        self.circle_graphics_view.setRenderHint(QPainter.Antialiasing)
        self.neck_graphics_view.setRenderHint(QPainter.Antialiasing)

# -----------------------------------------------------------------------------

    def create_gui(self):
        # All the frame is organized in a VBoxLayout
        self.thisVBoxLayout = QVBoxLayout()
        self.setLayout(self.thisVBoxLayout)

        # Add first circle_graphics_view to layout
        self.circle_graphics_view = QGraphicsView()
        self.circle_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        self.circle_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.circle_graphics_view.viewport().palette()
        palette.setColor(self.circle_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.circle_graphics_view.viewport().setPalette(palette)
        self.circle_scene = QGraphicsScene()
        self.circle_graphics_view.setScene(self.circle_scene)
        self.thisVBoxLayout.addWidget(self.circle_graphics_view)

        # Add a central area for label of mode/degree in scale and chord choice
        self.centralHBoxLayout = QHBoxLayout()
        self.create_mode_labels()
        self.create_chords_combobox()
        self.create_strings_number_for_chords_buttons()
        self.thisVBoxLayout.addLayout(self.centralHBoxLayout)

        # Add last neck_graphics_view to layout
        self.neck_graphics_view = QGraphicsView()
        self.neck_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        self.neck_graphics_view.viewport().setAutoFillBackground(True)
        palette = self.neck_graphics_view.viewport().palette()
        palette.setColor(self.neck_graphics_view.viewport().backgroundRole(), Qt.lightGray)
        self.neck_graphics_view.viewport().setPalette(palette)
        self.neck_scene = QGraphicsScene()
        self.neck_graphics_view.setScene(self.neck_scene)
        self.thisVBoxLayout.addWidget(self.neck_graphics_view)

    def create_mode_labels(self):
        self.centralMiddleVBoxLayout = QVBoxLayout()

        # Add Scale label to the layout
        ModeNamefont = QFont()
        ModeNamefont.setPointSize(24*self.scale_factor)
        ModeNamefont.setFamily(FONT)
        self.labelModeName = QLabel("This is a label")
        self.labelModeName.setAlignment(Qt.AlignCenter)
        self.labelModeName.setFont(ModeNamefont)

        # Add Scale label to the layout
        modeContentfont = QFont()
        modeContentfont.setPointSize(16*self.scale_factor)
        modeContentfont.setFamily(FONT)
        modeContentfont.setItalic(True)
        self.labelModeContent = QLabel("This is a label")
        self.labelModeContent.setAlignment(Qt.AlignCenter)
        self.labelModeContent.setFont(modeContentfont)

        self.centralMiddleVBoxLayout.addWidget(self.labelModeName)
        self.centralMiddleVBoxLayout.addWidget(self.labelModeContent)
        self.centralHBoxLayout.addLayout(self.centralMiddleVBoxLayout)

    def create_chords_combobox(self):
        labelFont = QFont()
        labelFont.setPointSize(20*self.scale_factor)
        labelFont.setFamily(FONT)
        self.chordLabel = QLabel("Chords using %s strings:" % self.highStringLimit)
        self.chordLabel.setAlignment(Qt.AlignLeft)
        self.chordLabel.setFont(labelFont)
        self.chords_combobox = QComboBox()
        self.chords_combobox.currentTextChanged.connect(lambda: self.show_chord())
        self.chords_combobox.highlighted.connect(self.show_highlighted_chord)
        self.alt_chords = QPushButton("Alt")
        self.alt_chords.setEnabled(False)
        self.alt_chords.clicked.connect(lambda: self.show_alternate_chord())

        self.chordGridLayout = QGridLayout()
        #chordVBoxLayout = QVBoxLayout()
        self.chordGridLayout.addWidget(self.chordLabel, 0, 0, 1, 2)
        #chordHBoxLayout = QHBoxLayout()
        self.chordGridLayout.addWidget(self.chords_combobox, 1, 0)
        self.chordGridLayout.addWidget(self.alt_chords, 1, 1)
        #chordVBoxLayout.addLayout(chordHBoxLayout)
        self.centralHBoxLayout.addLayout(self.chordGridLayout)

    def create_strings_number_for_chords_buttons(self):
        up_button = QPushButton("↑", self)
        up_button.clicked.connect(lambda: self.strings_for_chord(1))
        up_button.setMinimumWidth(30*self.scale_factor)
        up_button.setMaximumWidth(40*self.scale_factor)

        down_button = QPushButton("↓", self)
        down_button.clicked.connect(lambda: self.strings_for_chord(-1))
        down_button.setMinimumWidth(30*self.scale_factor)
        down_button.setMaximumWidth(40*self.scale_factor)

        #stringsPushButtonsVBoxLayout = QVBoxLayout()
        self.chordGridLayout.addWidget(up_button, 0, 2)
        self.chordGridLayout.addWidget(down_button, 1, 2)
        #self.centralHBoxLayout.addLayout(stringsPushButtonsVBoxLayout)

    def create_graphic_item_groups(self):
        # Groups to hold graphical parts such as general background, note points, line items and center pivot
        self.scale_circle_background = QGraphicsItemGroup()
        self.notes_group = QGraphicsItemGroup()
        self.notes_group.setHandlesChildEvents(False)
        self.scale_circle_background_group = QGraphicsItemGroup()
        self.scale_circle_center_group = QGraphicsItemGroup()
        self.neck_diagram_background_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group = QGraphicsItemGroup()
        self.neck_diagram_notes_group.setHandlesChildEvents(False)

# -----------------------------------------------------------------------------

    def set_scale(self, scale_name):
        # Keeping current degree, rotation and ref degree
        degreeIndex = self.degreeIndex
        modeIndex = self.modeIndex

        # init before scale change
        self.degreeIndex = 0
        self.modeIndex = 0

        self.degreeRotation = 0
        self.modeRotation = 0

        # scale change
        self.scaleName = scale_name
        self.shownScale = scales[self.scaleName]
        self.modeScale = scales[self.scaleName]
        self.scaleLength = len(self.shownScale)
        # and set back degree and mode
        self.set_mode(modeIndex)
        self.set_degree((degreeIndex-modeIndex)%self.scaleLength)

        self.draw_scale()
        self.draw_notes_on_neck()

    def set_tuning(self, tuning_name, init=False):
        self.currentTuning = tunings[tuning_name]
        self.currentTuningName = tuning_name
        if not init:
            self.draw_notes_on_neck()
            self.show_chord()

    def set_degree(self, degreeIndex, movingRef=False):
        if not movingRef:
            degreeIndex = (degreeIndex + self.modeIndex)%self.scaleLength
        currentDegreeIndex = self.degreeIndex
        self.degreeIndex = degreeIndex

        # keep current selected chord if any
        self.chordBeforeChange = self.chords_combobox.currentText()

        if currentDegreeIndex > degreeIndex:
            for i in range(currentDegreeIndex - degreeIndex):
                self.shownScale = self.rotate_notes(-1, self.shownScale)
                self.degreeRotation = (self.degreeRotation-1)%self.scaleLength
        elif currentDegreeIndex < degreeIndex:
            for i in range(degreeIndex-currentDegreeIndex):
                self.shownScale = self.rotate_notes(1, self.shownScale)
                self.degreeRotation = (self.degreeRotation+1)%self.scaleLength
        else:
            pass
        self.draw_scale()
        self.draw_notes_on_neck()

        # set back selected chord if any and available
        for index in range(self.chords_combobox.count()):
            if self.chordBeforeChange == self.chords_combobox.itemText(index):
                self.chords_combobox.setCurrentIndex(index)

    def set_mode(self, modeIndex):
        deltaDegreeToMode = (self.degreeIndex)-(self.modeIndex)
        CurrentDegreeToSet = (modeIndex+deltaDegreeToMode)%self.scaleLength

        currentModeIndex = self.modeIndex
        self.modeIndex = modeIndex

        if currentModeIndex > modeIndex:
            for i in range(currentModeIndex - modeIndex):
                self.modeScale = self.rotate_notes(-1, self.modeScale)
                self.modeRotation = (self.modeRotation-1)%self.scaleLength
        elif currentModeIndex < modeIndex:
            for i in range(modeIndex-currentModeIndex):
                self.modeScale = self.rotate_notes(1, self.modeScale)
                self.modeRotation = (self.modeRotation+1)%self.scaleLength
        else:
            pass
        self.set_degree(CurrentDegreeToSet, movingRef=True)


# -----------------------------------------------------------------------------

    def draw_scale_circle(self):
        center = QPointF(0, 0)
        radius = SCALE_CIRCLE_RADIUS*self.scale_factor

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(3*self.scale_factor)      # Set the pen width

        # Draw scale circle
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(SCALE_CIRCLE_RADIUS*self.scale_factor, SCALE_CIRCLE_RADIUS*self.scale_factor), QSizeF(2*radius, 2*radius)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.scale_circle_background_group.addToGroup(scale_circle)
        if self.scale_circle_background_group not in self.circle_scene.items():
            self.circle_scene.addItem(self.scale_circle_background_group)

    def draw_scale_circle_center(self):
        center = QPointF(0, 0)

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(2*self.scale_factor)      # Set the pen width
        pen2 = QPen(Qt.white)  # Set the pen color
        pen2.setWidth(2*self.scale_factor)      # Set the pen width

        # Draw center circle
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(12*self.scale_factor, 12*self.scale_factor), QSizeF(24*self.scale_factor, 24*self.scale_factor)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen2)
        self.scale_circle_center_group.addToGroup(scale_circle)
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(10*self.scale_factor, 10*self.scale_factor), QSizeF(20*self.scale_factor, 20*self.scale_factor)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.scale_circle_center_group.addToGroup(scale_circle)
        scale_circle = QGraphicsEllipseItem(QRectF(center - QPointF(5*self.scale_factor, 5*self.scale_factor), QSizeF(10*self.scale_factor, 10*self.scale_factor)))
        scale_circle.setBrush(Qt.white)
        scale_circle.setPen(pen)
        self.scale_circle_center_group.addToGroup(scale_circle)
        if self.scale_circle_center_group not in self.circle_scene.items():
            self.circle_scene.addItem(self.scale_circle_center_group)

    def draw_scale(self):
        scale = self.shownScale
        if tuple(scale) in modes.keys():
            self.modeName = modes[tuple(scale)]
        else:
            self.modeName = ""
        DegreeLabel = degrees[self.degreeRotation-self.modeRotation]
        labelContent = DegreeLabel + " / " + self.modeName
        self.labelModeName.setText(labelContent)
        self.get_mode_composition()
        root = QPointF(0, -SCALE_CIRCLE_RADIUS*self.scale_factor)
        center = QPointF(0, 0)
        radius = SCALE_CIRCLE_RADIUS*self.scale_factor

        semiToneAngle = 2 * math.pi / 12
        angles = [noteInScale * semiToneAngle for noteInScale in scale]
        noteSizes = [(10*self.scale_factor) for noteInScale in scale]
        noteSizes[0] = 2 * noteSizes[0]

        self.notesOnCircle = {noteInScale: list() for noteInScale in scale}

        pen = QPen(Qt.black)  # Set the pen color
        pen.setWidth(2*self.scale_factor)      # Set the pen width

        self.clear_group(self.notes_group)
        self.clear_group(self.scale_circle_center_group)
        self.clear_group(self.scale_circle_background_group)

        self.draw_scale_circle()

        for angle, noteSize, note in zip(angles, noteSizes, scale):
            x = center.x() + radius * math.sin(angle)
            y = center.y() - radius * math.cos(angle)
            point = QPointF(x, y)

            end_of_line_x = center.x() + (radius - noteSize/2 - (5*self.scale_factor)) * math.sin(angle)
            end_of_line_y = center.y() - (radius - noteSize/2 - (5*self.scale_factor)) * math.cos(angle)
            end_of_line_point = QPointF(end_of_line_x, end_of_line_y)

            x = center.x() + 1.1 * radius * math.sin(angle)
            y = center.y() - 1.1 * radius * math.cos(angle)
            labelAnchor = QPointF(x, y)

            # Draw line from center to point
            line = QLineF(center, end_of_line_point)
            line_item = QGraphicsLineItem(line)
            self.notes_group.addToGroup(line_item)

            # Draw note point
            note_point = NoteItem(QRectF(point - QPointF(noteSize/2.0, noteSize/2.0), QSizeF(noteSize, noteSize)), embeddingWidget=self)
            note_point.note = note
            note_point.angle = angle
            note_colour = self.color_for_angle(angle, mode=self.colour_degrees)
            note_point.colour = note_colour
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
        neck_width = FRET_SPACING * (self.num_frets + 1) *self.scale_factor
        neck_height = STRING_SPACING * (self.num_strings - 1) *self.scale_factor
        strings_thickness = stringSets[stringGaugeFromNumberOfString[self.num_strings]]

        self.clear_group(self.neck_diagram_background_group)

        # Draw strings
        darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        darkGray_pen.setWidth(1*self.scale_factor)      # Set the pen width

        for i in range(self.num_strings):
            y = i * STRING_SPACING *self.scale_factor
            line = QGraphicsLineItem(0, y, neck_width, y)
            darkGray_pen.setWidth((strings_thickness[i]/10.0)*self.scale_factor)
            line.setPen(darkGray_pen)
            self.neck_diagram_background_group.addToGroup(line)

        # Draw frets
        darkGray_pen = QPen(Qt.darkGray)  # Set the pen color
        darkGray_pen.setWidth(3*self.scale_factor)      # Set the pen width

        for i in range(1, self.num_frets + 1):
            x = i * FRET_SPACING*self.scale_factor
            line = QGraphicsLineItem(x, -5*self.scale_factor, x, neck_height+(5*self.scale_factor))
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

        neck_width = FRET_SPACING * (self.num_frets + 1) *self.scale_factor
        neck_height = STRING_SPACING * (self.num_strings - 1) *self.scale_factor

        self.draw_neck_background()

        self.identifiedNotes = {each: list() for each in range(12)}
        self.identifiedNoteTexts = {each: list() for each in range(12)}

        self.clear_group(self.neck_diagram_notes_group)

        font = QFont()
        font.setFamily(FONT)
        font.setPointSize(.95*(STRING_SPACING - 15)*self.scale_factor)

        # from low to high strings
        for i in range(self.num_strings):
            y = (neck_height - (i * STRING_SPACING)*self.scale_factor)
            # from low to high frets
            for j in range(1, self.num_frets):
                x = ((FRET_SPACING/2.0) + j * FRET_SPACING)*self.scale_factor
                semitone_text = (self.currentTuning[i] + j) -2
                # If the value in semi-tone modulo 12 (whatever the octave) is part of the scale
                if semitone_text%12 in self.shownScale:
                    point = QPointF(x, y)
                    # If the note is the root note, let's plot a triangle
                    half_string_spacing = (STRING_SPACING/2.0)*self.scale_factor
                    string_spacing = STRING_SPACING*self.scale_factor
                    if semitone_text%12 == 0:
                        triangle = QPolygonF()
                        triangle.append(QPointF(half_string_spacing, 0))  # Top point
                        triangle.append(QPointF(string_spacing, string_spacing))  # Bottom right point
                        triangle.append(QPointF(0, string_spacing))  # Bottom left point
                        note_point = TriangleNoteItem(triangle, embeddingWidget=self)
                        note_point.setPos(x-half_string_spacing, y-half_string_spacing)
                    # else, let's plot a simple circle
                    else:
                        note_point = NoteItem(QRectF(point - QPointF(half_string_spacing, half_string_spacing), QSizeF(string_spacing, string_spacing)), embeddingWidget=self)
                    # We record the symbol object, its note value and string and fret positions by note semi-tone value in the scale
                    note_point.note = semitone_text%12
                    note_point.colour = self.notesOnCircle[note_point.note][0][2]
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

# -----------------------------------------------------------------------------

    def get_maximum_semitone_difference_in_tuning(self):
        self.maximum_semitone_difference_in_tuning = 0
        for i in range(len(self.currentTuning)-2):
            self.maximum_semitone_difference_in_tuning = max(self.maximum_semitone_difference_in_tuning, self.currentTuning[i+1]-self.currentTuning[i])

    def get_mode_composition(self):
        modeComposition = [""] * self.scaleLength
        if self.scaleLength == 7:
            self.referenceScale = scales["Natural"]
            self.noteValues = [1, 2, 3, 4, 5, 6, 7]
            self.evenNoteRejectionMatrix = [0, 4, 1, 5, 2, 6, 3]
        elif self.scaleLength == 6:
            self.referenceScale = [0, 2, 4, 5, 7, 11]
            self.noteValues = [1, 2, 3, 4, 5, 7]
            self.evenNoteRejectionMatrix = [0, 4, 1, 5, 2, 3]
        elif self.scaleLength == 5:
            self.referenceScale = [0, 2, 4, 7, 9]
            self.noteValues = [1, 2, 3, 5, 6]
            self.evenNoteRejectionMatrix = [0, 3, 1, 2, 4]
        # And generate the label for the mode composition
        for note_number in range(self.scaleLength):
            alteration = self.shownScale[note_number] - self.referenceScale[note_number]
            note_value = self.noteValues[note_number]
            if note_value%2 == 0:
                modeComposition[self.evenNoteRejectionMatrix[note_number]] = ("%s"%(alterations[alteration]+str(note_value+7)))
            else:
                modeComposition[self.evenNoteRejectionMatrix[note_number]] = ("%s"%(alterations[alteration]+str(note_value)))
        modeCompositionString = ', '.join(modeComposition)
        self.labelModeContent.setText(modeCompositionString)

    def get_root_note(self):
        if self.topApp.neckGeneralView != '':
            return self.topApp.neckGeneralView.rootNote
        return ''

    def get_note_for_current_degree(self, rootNote=''):
        if rootNote=='':
            rootNote = self.get_root_note()
        if rootNote!='':
            rootNoteIndex = notes[rootNote]
            degreeIndex = self.degreeIndex - self.modeIndex
            noteIndex = (rootNoteIndex + self.modeScale[degreeIndex]) % 12
            note = {value: key for key, value in notes.items()}[noteIndex]
            return note
        return ''

    def get_chords_in_mode(self):
        note = self.get_note_for_current_degree()
        self.availableChords = []
        for chord in chords.keys():
            if set(chord).issubset(tuple(self.shownScale)):
                self.availableChords.append(chord)
        self.enrichedChords = {}
        if self.highStringLimit > 4:
            self.get_enriched_chords_in_mode()
        self.chords_combobox.clear()
        self.chords_combobox.addItem("", userData=())
        for availableChord in self.availableChords:
            chordName = note+chords[availableChord]["notation"]
            self.chords_combobox.addItem(chordName, userData=availableChord)
        for enrichedChord in self.enrichedChords.keys():
            chordName = note+enrichedChord
            self.chords_combobox.addItem(chordName, userData=self.enrichedChords[enrichedChord])

    def get_enriched_chords_in_mode(self):
        self.enrichedChords = {}
        for chord in self.availableChords:
            if chords[chord]["notation"] in enrichments.keys():
                for enrichment in enrichments[chords[chord]["notation"]]:
                    if enrichment["semitones"][0] % 12 in self.shownScale:
                        enrichedChord =[semitone for semitone in chord]
                        enrichedChord.append(enrichment["semitones"][0])
                        self.enrichedChords[enrichment["notation"]] = enrichedChord


# -----------------------------------------------------------------------------


    def interpolate_colors(self, color1, color2, ratio):
        # Convert hex colors to RGB
        rgb_color1 = self.hex_to_rgb(color1)
        rgb_color2 = self.hex_to_rgb(color2)

        # Interpolate between RGB values based on the ratio
        interpolated_rgb = tuple(int(color1 + (color2 - color1) * ratio) for color1, color2 in zip(rgb_color1, rgb_color2))

        # Convert interpolated RGB colors back to hex
        interpolated_hex_color = '#' + ''.join(format(color, '02x') for color in interpolated_rgb)

        return interpolated_hex_color

    def generate_colour_for_angle(self, angle, includeRotation=True, colours=customColours[DEGREE_COLOUR]):
        # Normalize angle to be between 0 and 360 degrees
        angle = 360*(angle/(2*math.pi))
        # How about rotating colours too :-)
        if includeRotation:
            #rotation = (self.modeRotation + self.degreeRotation)%self.scaleLength
            angleOfRotation = 30*scales[self.scaleName][self.degreeRotation]
            angle += angleOfRotation
        angle %= 360

        number_of_colours = len(colours)-1 #-1 because first and last are the same, it's a circle of colours
        angle_between_colours = 360.0/number_of_colours
        index1 = int(angle // angle_between_colours)
        index2 = int((index1 + 1)%number_of_colours)
        ratio = (angle - (index1 * angle_between_colours)) / angle_between_colours
        colour = self.interpolate_colors(colours[index1], colours[index2], ratio)
        return colour

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def hex_to_qcolor(self, hex_color):
        # Remove '#' from the beginning of the hexadecimal string if present
        color = self.hex_to_rgb(hex_color)
        # Create a QColor object with the RGB values
        qcolor = QColor(color[0], color[1], color[2])
        return qcolor

    def angle_to_hue(self, angle):
        """
        Cosmetic; compute custom hue based on angle of note in circle (30° = a semi-tone)
        """
        # How about rotating colours too :-)
        angleOfRotation = 30*scales[self.scaleName][self.degreeRotation]
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
        angle %= 360
        return hue

    def color_for_angle(self, angle, mode=DEGREE_COLOUR):
        """
        Cosmetic; Create a QColor from angle
        """
        if mode == 'Hue':
            hue = self.angle_to_hue(angle)
            colour = QColor.fromHsvF(hue / 360, 1, 1)
        else:
            colour = self.hex_to_qcolor(self.generate_colour_for_angle(angle, colours=customColours[mode]))
        return colour

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
        black_pen = QPen(Qt.black)
        gray_pen = QPen(Qt.gray)
        trans_pen = QPen(Qt.transparent)
        # for each note in chord
        for note in self.identifiedNotes.keys():
            # for each position of the note
            for (note_point, semitone_text, string, fret, text_item) in self.identifiedNotes[note]:
                if 0 <= semitone_text <= semitonesToConsiderByNumberOfStrings[self.num_strings]:
                    note_point.setBrush(Qt.black)
                    note_point.setPen(trans_pen)
                else:
                    note_point.setBrush(Qt.gray)
                    note_point.setPen(trans_pen)
                text_item.setBrush(Qt.white)
            for (note_point, line_item, note_colour) in self.notesOnCircle[self.shownScale[note%self.scaleLength]]:
                colour_pen = QPen(Qt.black)
                colour_pen.setWidth(1)
                line_item.setPen(colour_pen)

    def color_chord_notes(self, chord):
        notes_positions = self.get_positions_of_chord_notes(chord)
        self.chord_positions = self.get_positions_combinations_for_chord(chord, notes_positions)
        self.colour_chord(self.chord_positions)

    def changeColourDegrees(self, colour):
        self.colour_degrees = colour
        self.refresh(scale_factor=self.scale_factor)

    def get_positions_of_chord_notes(self, chord):
        notes_positions = {}
        for note in chord:
            notes_positions[note] = []
            # for each position of the note
            for (note_marker, semitone, string, fret, note_label) in self.identifiedNotes[note%12]:
                authorizedString = (self.lowStringLimit-1 <= string <= self.highStringLimit-1)
                authorizedFret = (fret < 6)
                authorizedSemitoneByNumberOfStrings = (0 <= semitone <= semitonesToConsiderByNumberOfStrings[self.num_strings])
                if authorizedString and authorizedFret and authorizedSemitoneByNumberOfStrings:
                    notes_positions[note].append((string, fret, note_marker, note_label))
        return notes_positions

    def get_positions_combinations_for_chord(self, chord, notes_positions):
        # detection of note of chord with a single position
        reserved_strings_for_note = {}
        for note in chord:
            if len(notes_positions[note]) == 1:
                reserved_strings_for_note[notes_positions[note][0][2]] = note

        # notes positions that respect the single position of other notes
        notes_positions_respecting_notes_with_single_occurence = {}
        for note in chord:
            #notes_positions_respecting_notes_with_single_occurence[note] = []
            for (string, fret, note_marker, note_label) in notes_positions[note]:
                reservedString = (string in reserved_strings_for_note.keys())
                # we keep the note in all cases except when the string is reserved but the note does not correspond
                if not (reservedString and not (reserved_strings[string] == note)):
                    if not string in notes_positions_respecting_notes_with_single_occurence.keys():
                        notes_positions_respecting_notes_with_single_occurence[string] = []
                    notes_positions_respecting_notes_with_single_occurence[string].append((note, fret, note_marker, note_label))

        # Generate all the possible notes position combinations
        # Create a new list where each tuple is paired with its key
        notes_positions_with_note = {string: [(string, note, fret, note_marker, note_label) for (note, fret, note_marker, note_label) in tuples] for string, tuples in notes_positions_respecting_notes_with_single_occurence.items()}
        # Extract the keyed lists
        stringIndexesSorted = sorted(notes_positions_with_note.keys())
        #lists = list(notes_positions_with_note.values())
        lists = [notes_positions_with_note[stringIndex] for stringIndex in stringIndexesSorted]
        # Use itertools.product to generate combinations of keyed tuples
        potential_chord_positions = list(itertools.product(*lists))

        # We need to eliminate all the combinations that do not have all the note of the chord

        #print('\n')
        #print(chord)
        potential_complete_chord_positions = []
        for potential_chord_position in potential_chord_positions:
            foundAllNote = True
            for note in chord:
                foundNote = False
                for (string, noteOnNeck, fret, note_marker, note_label) in potential_chord_position:
                    foundNote = (foundNote or (noteOnNeck == note))
                foundAllNote = (foundAllNote and foundNote)
            if foundAllNote:
                potential_complete_chord_positions.append(potential_chord_position)

        # We need to compute the intrinsic distance of the chord position to rank them
        # distance will be the sum of the absolute difference of fret from one string to the next
        weighted_chord_positions = []
        for potential_chord_position in potential_complete_chord_positions:
            distance = 0
            for i in range(1, len(potential_chord_position)-1):
                distance += abs(potential_chord_position[i-1][2] - potential_chord_position[i][2])
            #print(distance, potential_chord_position)
            weighted_chord_positions.append((distance,potential_chord_position))
        weighted_chord_positions = sorted(weighted_chord_positions, key=lambda x: x[0])
        #print(weighted_chord_positions)
        return weighted_chord_positions

    def colour_chord(self, chord_positions):
        white_pen = QPen(Qt.white)
        gray_pen = QPen(Qt.gray)
        trans_pen = QPen(Qt.transparent)

        #print(chord_positions[self.chordIndex])

        for (string, note, fret, note_marker, note_label) in chord_positions[self.chordIndex][1]:
            note_marker.setBrush(Qt.white)
            note_marker.setPen(trans_pen)
            note_label.setBrush(Qt.black)



# -----------------------------------------------------------------------------

    def center_neck_view(self):
        # Get the bounding rectangle of all items in the scene
        rect = self.neck_scene.itemsBoundingRect()
        # Calculate the center point of the bounding rectangle
        center = rect.center()
        # Set the size of the viewport
        self.neck_graphics_view.viewport().setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        view_size = self.neck_graphics_view.viewport().size()
        # Calculate the new position for the scene
        scene_pos = center - QPointF(view_size.width() / 2, view_size.height() / 2)
        # Set the new position for the scene
        self.neck_scene.setSceneRect(scene_pos.x(), scene_pos.y(), view_size.width(), view_size.height())

    def center_scale_view(self):
        # Get the bounding rectangle of all items in the scene
        rect = self.circle_scene.itemsBoundingRect()
        # Calculate the center point of the bounding rectangle
        center = rect.center()
        # Set the size of the viewport
        self.circle_graphics_view.viewport().setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        view_size = self.circle_graphics_view.viewport().size()
        # Calculate the new position for the scene
        scene_pos = center - QPointF(view_size.width() / 2, view_size.height() / 2)
        # Set the new position for the scene
        self.circle_scene.setSceneRect(scene_pos.x(), scene_pos.y(), view_size.width(), view_size.height())

    def refresh(self, scale_factor=1.0):
        print("scale_factor: %s" % scale_factor)
        self.scale_factor = scale_factor
        self.circle_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        self.circle_graphics_view.viewport().update()
        self.neck_graphics_view.setFixedSize(GRAPHICSVIEW_WIDTH*self.scale_factor, GRAPHICSVIEW_HEIGHT*self.scale_factor)
        self.neck_graphics_view.viewport().update()
        self.thisVBoxLayout.update()
        self.centralHBoxLayout.update()
        self.update()
        self.draw_scale()
        self.draw_notes_on_neck()
        self.get_chords_in_mode()
        self.center_neck_view()
        self.center_scale_view()

# -----------------------------------------------------------------------------

    @Slot(int)
    def rotate_notes(self, rotation, scale):
        scale = sorted([(inScale +(12-scale[rotation]))%12 for inScale in scale])
        return scale

    @Slot(int)
    def strings_for_chord(self, increment):
        if increment > 0:
            if self.highStringLimit < self.num_strings:
                self.highStringLimit = min(self.highStringLimit+1, self.num_strings)
            else:
                self.lowStringLimit = min(self.lowStringLimit+1, self.maximumNumberHigherStringsNumber)
        else:
            if self.lowStringLimit > 1:
                self.lowStringLimit = max(self.lowStringLimit-1, 1)
            else:
                self.highStringLimit = max(self.highStringLimit-1, self.minimumNumberLowerStringsNumber)
        self.chordLabel.setText("Chords using %s strings:" % (self.highStringLimit-self.lowStringLimit+1))
        self.chordBeforeChange = self.chords_combobox.currentText()
        self.color_notes_by_default()
        self.get_chords_in_mode()
        self.color_chord_notes(self.chords_combobox.currentData())
        for index in range(self.chords_combobox.count()):
            if self.chordBeforeChange == self.chords_combobox.itemText(index):
                self.chords_combobox.setCurrentIndex(index)

    @Slot()
    def show_chord(self):
        self.color_notes_by_default()
        if self.chords_combobox.currentText() != "":
            if len(self.chord_positions) > 1:
                self.alt_chords.setEnabled(True)
            self.color_chord_notes(self.chords_combobox.currentData())
        else:
            self.alt_chords.setEnabled(False)
            self.chordIndex = 0

    @Slot()
    def show_alternate_chord(self):
        self.color_notes_by_default()
        #print("chordIndex: %s" % self.chordIndex)
        #print("len(self.chord_positions): %s" % len(self.chord_positions))

        self.chordIndex = (self.chordIndex+1)%len(self.chord_positions)
        #print("chordIndex: %s" % self.chordIndex)

        self.color_chord_notes(self.chords_combobox.currentData())

    @Slot(int)
    def show_highlighted_chord(self, index):
        self.color_notes_by_default()
        if len(self.chord_positions) > 1:
            self.alt_chords.setEnabled(True)
        self.chordIndex = 0
        self.color_chord_notes(self.chords_combobox.itemData(index))







# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, scale_factor=1.0):
        super().__init__()

        self.scale_factor = scale_factor
        self.last_scale_Factor = scale_factor
        self.initUI()

        self.neckGeneralView = ''

        self.scaleName = ""
        self.scale = list()
        self.scaleLength = 0

        self.modeIndex = 0
        self.modesListByScaleDic = linkModesToScales()

        self.currentTuningName = ""

        self.colour_degrees = DEGREE_COLOUR

        self.labelFont = QFont()
        self.labelFont.setPointSize(20*self.scale_factor)
        self.labelFont.setFamily(FONT)

        self.create_gui()

        # Create a first frame for the first Degree to show
        self.degreesFrames = list()
        vframe = self.addDegreeFrame(visible=True, name="frame_1")

        # Initialisation
        self.set_scale("Natural")
        self.set_mode("I - Ionian (major)", 0)
        self.set_arrangement("I", 0)
        self.set_tuning("Standard 6 \tEADGBE")

# -----------------------------------------------------------------------------

    def initUI(self):
        self.setWindowTitle("🎸 Scales Circle Diagram")

    def create_gui(self):
        # Set a main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # In which will be a global VBoxLayout
        self.mainVBoxLayout = QVBoxLayout(self.central_widget)

        # a first horizontal layout for the general tools
        self.topHBoxLayout = QHBoxLayout()
        self.create_scale_combobox(self.topHBoxLayout)
        self.create_mode_combobox(self.topHBoxLayout)
        self.create_arrangement_combobox(self.topHBoxLayout)
        self.create_tuning_combobox(self.topHBoxLayout)
        self.create_full_neck_radioButton(self.topHBoxLayout)
        self.full_neck_radioButton.setChecked(False)
        self.mainVBoxLayout.addLayout(self.topHBoxLayout)

        # a second horizontal layout for the max four degrees
        self.midHBoxLayout = QHBoxLayout()
        self.mainVBoxLayout.addLayout(self.midHBoxLayout)
        #print(self.mainVBoxLayout.getStyleSheet())

    def create_scale_combobox(self, parentLayout):
        '''
        Create the combobox letting the user choose the general scale to work with
        '''
        label = QLabel("Scale:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        #label.originalFontSize = 20
        self.scales_combobox = QComboBox()
        self.scales_combobox.addItems(scales.keys())
        self.scales_combobox.currentTextChanged.connect(lambda: self.set_scale(self.scales_combobox.currentText()))

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.scales_combobox)
        parentLayout.addLayout(vBoxLayout)

    def create_mode_combobox(self, parentLayout):
        '''
        Create the combobox that let the user choose the mode of the scale to be the root mode
        '''
        label = QLabel("Mode:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        #label.originalFontSize = 20
        self.mode_combobox = QComboBox()
        self.add_compatible_modes_in_Combobox()
        self.mode_combobox.currentTextChanged.connect(lambda: self.set_mode(self.mode_combobox.currentText(), self.mode_combobox.currentIndex()))

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.mode_combobox)
        parentLayout.addLayout(vBoxLayout)

    def create_arrangement_combobox(self, parentLayout):
        '''
        Create the combobox that let the user choose a succession of degrees in
        the chosen mode of the scale, aka an arrangement
        '''
        label = QLabel("Arrangmt:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        #label.originalFontSize = 20
        self.arrangement_combobox = QComboBox()
        self.add_arrangements_to_combobox()
        self.arrangement_combobox.currentTextChanged.connect(lambda: self.set_arrangement(self.arrangement_combobox.currentText(), self.arrangement_combobox.currentIndex()))
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.arrangement_combobox)
        parentLayout.addLayout(vBoxLayout)

    def create_tuning_combobox(self, parentLayout):
        label = QLabel("Tuning:")
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.labelFont)
        #label.originalFontSize = 20
        self.tunings_combobox = QComboBox()
        self.tunings_combobox.addItems(tunings.keys())
        self.tunings_combobox.setCurrentText("Standard 6 \tEADGBE")
        self.tunings_combobox.currentTextChanged.connect(lambda: self.set_tuning(self.tunings_combobox.currentText()))
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(self.tunings_combobox)
        parentLayout.addLayout(vBoxLayout)

    def create_full_neck_radioButton(self, parentLayout):
        self.full_neck_radioButton = QRadioButton("Neck window")
        self.full_neck_radioButton.toggled.connect(self.toggle_neck_general_view)
        parentLayout.addWidget(self.full_neck_radioButton)

# -----------------------------------------------------------------------------

    def add_compatible_modes_in_Combobox(self):
        '''
        Adds only the reference degrees present in the defined scale.
        If the currently set mode is still available in the new scale,
        it is kept, if not, mode is set to I
        '''
        # keep record of set mode
        currentMode = self.mode_combobox.currentText()
        currentModeIndex = self.mode_combobox.currentIndex()
        foundCurrentMode = False
        self.modesListByScaleDic
        # clean and fill mode_combobox
        for i in range(self.mode_combobox.count()):
            self.mode_combobox.removeItem(0)
        for i in range(len(degrees)):
            if i < self.scaleLength:
                modeName = self.modesListByScaleDic[self.scaleName][i]
                mode_text = degrees[i] + "\t" + modeName
                self.mode_combobox.addItem(mode_text)
                if (i == currentModeIndex) and (not foundCurrentMode):
                    foundCurrentMode = True
        if foundCurrentMode:
            self.mode_combobox.setCurrentIndex(currentModeIndex)

    def add_arrangements_to_combobox(self):
        '''
        '''
        arrangements = []
        for arrangement in degreeArrangements:
            arrangementStrings = []
            for degree in arrangement:
                 arrangementStrings.append(degrees[degree-1])
            arrangements.append('-'.join(arrangementStrings))
        self.arrangement_combobox.addItems(arrangements)

    def set_scale(self, scale_name):
        '''
        set the global scale used
        '''
        self.scaleName = scale_name
        self.scale = scales[self.scaleName]
        self.scaleLength = len(self.scale)
        self.add_compatible_modes_in_Combobox()
        self.scaleLength = len(self.scale)
        for vFrame in self.degreesFrames:
            vFrame.set_scale(scale_name)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_scale(self.scaleName)

    def set_mode(self, modeName, modeIndex):
        '''
        set the mode of the root
        '''
        self.modeIndex = modeIndex
        for vFrame in self.degreesFrames:
            vFrame.set_mode(modeIndex)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_mode(modeIndex)

    def set_arrangement(self, arrangement, arrIndex):
        height = 500*self.scale_factor
        width = 940*self.scale_factor
        self.arrangementString = arrangement
        self.arrangement = degreeArrangements[arrIndex]
        self.clearDegreeFrames()
        self.setFixedSize(height * len(self.arrangement), width)
        for i in range(len(self.arrangement)):
            name = "frame_%s"%(1+i)
            vFrame = self.addDegreeFrame(name=name)
            # One needs to re-apply all the settings for the frames were recreated
            vFrame.set_scale(self.scales_combobox.currentText())
            vFrame.set_mode(self.mode_combobox.currentIndex())
            vFrame.set_degree(self.arrangement[i]-1)
            vFrame.set_tuning(self.tunings_combobox.currentText())
            vFrame.show()
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_arrangement(self.arrangement)

    def set_tuning(self, tuning_name, init=False):
        self.currentTuning = tunings[tuning_name]
        self.currentTuningName = tuning_name
        for vFrame in self.degreesFrames:
            vFrame.set_tuning(tuning_name, init=init)
        if not self.neckGeneralView == "":
            self.neckGeneralView.set_tuning(self.currentTuningName, init=init)

    def clearDegreeFrames(self):
        for vFrame in self.degreesFrames:
            self.midHBoxLayout.removeWidget(vFrame)
            vFrame.deleteLater()
        self.degreesFrames = list()

    def addDegreeFrame(self, visible=False, name=""):
        width = 483*self.scale_factor
        height = 854*self.scale_factor
        vBoxFrame = CircleAndNeckVBoxFrame(self, 1, visible=visible, name=name, scale_factor=self.scale_factor)
        self.degreesFrames.append(vBoxFrame)
        vBoxFrame.setFixedSize(width, height)
        self.midHBoxLayout.addWidget(vBoxFrame)
        return vBoxFrame

    def changeColourDegrees(self, colourDegrees):
        self.colour_degrees = colourDegrees
        for vFrame in self.degreesFrames:
            vFrame.changeColourDegrees(self.colour_degrees)

# -----------------------------------------------------------------------------

    def toggle_neck_general_view(self):
        if not self.neckGeneralView == '':
            if self.neckGeneralView.isVisible():
                self.neckGeneralView.hide()
            else:
                self.neckGeneralView.show()
        else:
            self.create_neck_general_view()
        self.neckGeneralView.refresh(scale_factor=self.scale_factor)

    def create_neck_general_view(self):
        width = 1500*self.scale_factor
        height = 440*self.scale_factor
        self.neckGeneralView = NeckWindow(self, scale_factor=self.scale_factor)
        self.refresh()
        self.neckGeneralView.set_scale(self.scaleName)
        self.neckGeneralView.set_tuning(self.currentTuningName, init=True)
        self.neckGeneralView.set_mode(self.modeIndex)
        self.neckGeneralView.set_arrangement(self.arrangement)
        self.neckGeneralView.setFixedSize(width, height)
        self.neckGeneralView.show()

    def keyPressEvent(self, event):
        print("event.key: %s" % event.key())
        if event.key() == 43:
            print("scale up")
            self.last_scale_Factor = self.scale_factor
            self.scale_factor += .1
            #self.zoomIn()
            self.refresh()
        elif event.key() == 95:
            print("scale down")
            self.last_scale_Factor = self.scale_factor
            self.scale_factor -= .1
            #self.zoomOut()
            self.refresh()
        else:
            super().keyPressEvent(event)

    def scale_all_labels(self):
        relative_scale_factor = self.scale_factor/self.last_scale_Factor
        for widget in self.findChildren(QLabel):
            font = widget.font()
            if hasattr(widget, 'originalFontSize'):
                original_point_size = widget.originalFontSize
                if original_point_size > 0:  # If a point size is set
                    font.setPointSizeF(original_point_size * self.scale_factor)
                    widget.setFont(font)
            else:
                original_point_size = font.pointSize()
                if original_point_size > 0:  # If a point size is set
                    font.setPointSizeF(original_point_size * relative_scale_factor)
                    widget.setFont(font)
            widget.setStyleSheet(f"padding: {int(5 * relative_scale_factor)}px; margin: {int(5 * relative_scale_factor)}px;")

    def scale_all_comboboxes(self):
        relative_scale_factor = self.scale_factor/self.last_scale_Factor
        for widget in self.findChildren(QComboBox):
            #print("treating QCombobox: %s" % widget)
            new_width = widget.size().width() * relative_scale_factor
            new_height = widget.size().height() * relative_scale_factor
            '''
            font = widget.font()
            original_point_size = font.pointSize()
            if original_point_size > 0:  # If a point size is set
                print("original_point_size > 0")
                font.setPointSize(original_point_size * self.scale_factor/self.last_scale_Factor)
                widget.setFont(font)
            '''
            print("widget.style elements: %s" % dir(widget.style()))
            print("widget.style layout spacing: %s" % widget.style().__getattribute__('layoutSpacing'))

            #widget.setStyleSheet(f"padding: {int(5 * relative_scale_factor)}px; margin: {int(5 * relative_scale_factor)}px;")

            widget.setFixedSize(new_width, new_height)

    def scale_all_pushbuttons(self):
        for widget in self.findChildren(QPushButton):
            print("scale_all_pushbuttons: %s" % widget)
            font = widget.font()
            font_metrics = QFontMetrics(font)
            original_point_size = font_metrics.height()
            print(original_point_size)
            if original_point_size > 0:  # If a point size is set
                font.setPointSize(int(original_point_size * self.scale_factor/self.last_scale_Factor))
                widget.setFont(font)
            relative_scale_factor = self.scale_factor/self.last_scale_Factor
            widget.setStyleSheet(f"padding: {int(5 * relative_scale_factor)}px; margin: {int(5 * relative_scale_factor)}px;")

    def find_all_layouts(self):
        layouts = []

        def _find_layouts(w):
            # Check if the widget has a layout
            layout = w.layout()
            if layout:
                layouts.append(layout)
                # Recursively find layouts in child widgets
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item.widget():
                        _find_layouts(item.widget())
                    elif item.layout():
                        layouts.append(item.layout())

        _find_layouts(self)
        return layouts

    def scale_spacings(self):
        layouts = self.find_all_layouts()
        for layout in layouts:
            current_spacing = layout.spacing()
            layout.setSpacing(current_spacing* self.scale_factor/self.last_scale_Factor)

    def refresh(self):
        width = 510 * self.scale_factor
        height = 940 * self.scale_factor
        self.labelFont.setPointSize(20*self.scale_factor)
        #self.scale_all_labels()
        #self.scale_all_comboboxes()
        #self.scale_all_pushbuttons()
        #self.scale_spacings()
        self.setFixedSize(width, height)
        self.update()

        self.central_widget.update()

        currentArrangement = self.arrangement_combobox.currentText()
        currentArrangementIndex = self.arrangement_combobox.currentIndex()
        self.set_arrangement('II', 1)
        #for vFrame in self.degreesFrames:
        #    vFrame.refresh(scale_factor=self.scale_factor)
        self.set_arrangement(currentArrangement, currentArrangementIndex)
        if not self.neckGeneralView == '':
            width = 1500*self.scale_factor
            height = 440*self.scale_factor
            self.neckGeneralView.setFixedSize(width, height)
            self.neckGeneralView.refresh(scale_factor=self.scale_factor)

    def closeEvent(self, event):
        if not self.neckGeneralView == '':
            self.neckGeneralView.close()
        event.accept()







# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scale_factor = 1.0
    window = MainWindow(scale_factor=scale_factor)
    width = 510 * scale_factor
    height = 940 * scale_factor
    window.setFixedSize(width, height)
    window.show()
    sys.exit(app.exec())

# -----------------------------------------------------------------------------
