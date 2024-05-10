# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# Author: Gregoire Vandenschrick
# Date:   17/02/2024
# ࿄ ࿅ ࿇
# -----------------------------------------------------------------------------

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

enrichments = {
"M": ({"semitones": (14,), "notation": "M9"},),
"m": ({"semitones": (14,), "notation": "m9"},),
"7": ({"semitones": (13,), "notation": "9♭"},{"semitones": (14,), "notation": "9"},{"semitones": (15,), "notation": "9♯"},{"semitones": (18,), "notation": "11♯"}),
"m7": ({"semitones": (14,), "notation": "m9"},{"semitones": (17,), "notation": "m11"}),
"7sus": ({"semitones": (13,), "notation": "sus9♭"},{"semitones": (14,), "notation": "sus9"}),
"7maj": ({"semitones": (14,), "notation": "7maj9"},{"semitones": (18,), "notation": "7maj11♯"}),
"m7maj": ({"semitones": (14,), "notation": "m7maj9"},{"semitones": (18,), "notation": "m7maj11♯"}),
"7maj♯5": ({"semitones": (14,), "notation": "m7maj♯59"},{"semitones": (18,), "notation": "m7maj♯511♯"}),
"7♯5": ({"semitones": (13,), "notation": "9♭"},{"semitones": (14,), "notation": "9"},{"semitones": (15,), "notation": "9♯"},{"semitones": (18,), "notation": "11♯"}),
"7♭5": ({"semitones": (13,), "notation": "7♭5♭9"},{"semitones": (14,), "notation": "7♭59"},{"semitones": (15,), "notation": "7♭5♯9"}),
"m7♭5": ({"semitones": (14,), "notation": "m7♭5m9"},{"semitones": (17,), "notation": "m7♭5m11"}),
"dim7": ({"semitones": (14,), "notation": "dim7m9"},{"semitones": (17,), "notation": "dim7m11"})
}

tunings = {
"Standard bass 4 \tEADG"  : (0, 5, 10, 15),
"Standard bass 5 \tBEADG" : (0, 5, 10, 15, 20),
"Standard 6 \tEADGBE"     : (0, 5, 10, 15, 19, 24),
"Drop D 6 \tDADGBE"       : (0, 7, 12, 17, 21, 26),
"Drop E♭ 6 \tE♭B♭E♭A♭CF"  : (0, 7, 12, 17, 21, 26),
"open 6 \tDGDGBD"         : (0, 5, 12, 17, 21, 24),
"Standard 7 \tBEADGBE"    : (0, 5, 10, 15, 20, 24, 29),
"Drop A 7 \tAEADGBE"      : (0, 7, 12, 17, 22, 26, 31),
"Standard 8 \tF♯BEADGBE"  : (0, 5, 10, 15, 20, 25, 29, 34),
"A-Tuning 8 \tADGCFADG"   : (0, 5, 10, 15, 20, 24, 29, 34),
"Drop E 8 \tEBEADGBE"     : (0, 7, 12, 17, 22, 27, 31, 36),
"Drop D 8 \tDADGCFAD"     : (0, 7, 12, 17, 22, 27, 31, 36)
}

stringGaugeFromNumberOfString = {
4 : "standard 4",
5 : "standard 5",
6 : "standard 6",
7 : ".strandberg＊ 7",
8 : ".standberg＊ 8"
}

semitonesToConsiderByNumberOfStrings = {
4: 24,
5: 24,
6: 24,
7: 24,
8: 36
}

stringSets = {
"standard 4"      : (45, 65, 85, 100),
"standard 5"      : (45, 65, 85, 105, 130),
"standard 6"      : (10, 13, 17, 26, 36, 46),
".strandberg＊ 7" : (9.5, 13, 16, 24, 34, 46, 64),
".standberg＊ 8"  : (9, 12, 15, 22, 30, 42, 56, 84)
}

degrees = ("I", "II", "III", "IV", "V", "VI", "VII")

degreeArrangements = (
(1,),
(2,),
(3,),
(4,),
(5,),
(6,),
(7,),
(1, 2, 3),
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
