#!/usr/bin/fontforge -script
"""
Makes an HTML table showing how many glyphs are in each range in each font,
and tries to collate that with the OS/2 character range support bit flags.

Runs under FontForge.
	fontforge -script ranges.py

This is a hack--in no way authoritative.  
Lots of guesswork; much is wrong; the coding is gross.

See
http://www.w3.org/TR/REC-CSS2/notes.html
http://shlimazl.nm.ru/eng/fonts_ttf.htm
http://www.evertype.com/standards/iso10646/ucs-collections.html

The intervals are partly just the assigned interval, but often I have
listed the ranges that have characters assigned to them.


$Id: ranges.py,v 1.28 2009-05-01 07:47:15 Stevan_White Exp $
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys
import time


class interval:
	def __init__( self, begin, end ):
		self.begin = begin
		self.end = end

	def len( self ):
		return 1 + self.end - self.begin

	def __str__( self ):
		return '[' + str( self.begin ) + ',' + str( self.end ) + ']'

	def contains( self, val ):
		return val <= self.end and val >= self.begin


# NOTE the OpenType spec is much more thorough
# http://www.microsoft.com/OpenType/OTSpec/os2.htm
ulUnicodeRange = [
[0,	'Basic Latin', [interval(0x0020, 0x007E)] ],
[1,	'Latin-1 Supplement',[interval(0x00A0, 0x00FF)] ],
[2,	'Latin Extended-A',	[interval(0x0100, 0x017F)] ],
[3,	'Latin Extended-B',     [interval(0x0180, 0x024F)]],
[4,	'IPA and Phonetic Extensions',     [interval(0x0250, 0x02AF),
			interval(0x1D00, 0x1D7F),	# Phonetic Extensions
			interval(0x1D80, 0x1DBF)	# Phonetic Extensions S.
	]],
[5,	'Spacing Modifier Letters',     [interval(0x02B0, 0x02FF),
			interval(0xA700, 0xA71F)	# Modifier Tone Letters
	]],
[6,	'Combining Diacritical Marks',     [interval(0x0300, 0x036F)]],
[7,	'Greek and Coptic',     [interval(0x0370, 0x0377),
			interval(0x037A, 0x037E),
			interval(0x0384, 0x038A),
			interval(0x038C, 0x038C),
			interval(0x038E, 0x03A1),
			interval(0x03A3, 0x03CF),
			interval(0x03D0, 0x03FF)
			] ],
[8,	'Coptic',     [interval(0x2C80, 0x2CFF)]],
[9,	'Cyrillic',     [
	interval(0x0400, 0x04FF),	# Cyrillic
	interval(0x0500, 0x0523),	# Cyrillic Supplement
	interval(0x2DE0, 0x2DFF),	# Cyrillic Extended-A
	interval(0xA640, 0xA65F),	# Cyrillic Extended-B
	interval(0xA662, 0xA673),
	interval(0xA67C, 0xA697)
	]
	],
[10,	'Armenian',     [interval(0x0531, 0x0556),
			interval(0x0559, 0x055F),
			interval(0x0561, 0x0587),
			interval(0x0589, 0x058A)
			]
	],
[11,	'Hebrew',    [
			interval(0x0591, 0x05C7),
			interval(0x05D0, 0x05EA),
			interval(0x05F0, 0x05F4)
		]], # See http://webcenter.ru/~kazarn/eng/ululinks.htm
[12,	'Vai',    [interval(0xA500, 0xA62B),
		]],
[13,	'Arabic (+supplement)',     [interval(0x0600, 0x0603),
			interval(0x0606, 0x061B),
			interval(0x061E, 0x061F),
			interval(0x0621, 0x0652),
			interval(0x0653, 0x06FF),	# Supplement
	]
	],
[14,	'', [interval(0x07C0, 0x07FF)]],	# unclear ? Part of Arabic?
[15,	'Devanagari',     [interval(0x0901, 0x0939),
			interval(0x093C, 0x094D),
			interval(0x0950, 0x0954),
			interval(0x0958, 0x0972),
			interval(0x097B, 0x097F)
			]],
[16,	'Bengali',     [interval(0x0981, 0x0983),
		interval(0x0985, 0x098C),
		interval(0x098F, 0x0990),
		interval(0x0993, 0x09A8),
		interval(0x09AA, 0x09B0),
		interval(0x09B2, 0x09B2),
		interval(0x09B6, 0x09B9),
		interval(0x09BC, 0x09C4),
		interval(0x09C7, 0x09C8),
		interval(0x09CB, 0x09CE),
		interval(0x09D7, 0x09D7),
		interval(0x09DC, 0x09DD),
		interval(0x09DF, 0x09E3),
		interval(0x09E6, 0x09FA),
	]],
[17,	'Gurmukhi',     [interval(0x0A01, 0x0A03),
		interval(0x0A05, 0x0A0A),
		interval(0x0A0F, 0x0A10),
		interval(0x0A13, 0x0A28),
		interval(0x0A2A, 0x0A30),
		interval(0x0A32, 0x0A33),
		interval(0x0A35, 0x0A36),
		interval(0x0A38, 0x0A39),
		interval(0x0A3C, 0x0A3C),
		interval(0x0A3E, 0x0A42),
		interval(0x0A47, 0x0A48),
		interval(0x0A4B, 0x0A4D),
		interval(0x0A51, 0x0A51),
		interval(0x0A59, 0x0A5C),
		interval(0x0A5E, 0x0A5E),
		interval(0x0A66, 0x0A75),
		]],
[18,	'Gujarati',     [interval(0x0A81, 0x0A83),
		interval(0x0A85, 0x0A8D),
		interval(0x0A8F, 0x0A91),
		interval(0x0A93, 0x0AA8),
		interval(0x0AAA, 0x0AB0),
		interval(0x0AB2, 0x0AB3),
		interval(0x0AB5, 0x0AB9),
		interval(0x0ABC, 0x0AC5),
		interval(0x0AC7, 0x0AC9),
		interval(0x0ACB, 0x0ACD),
		interval(0x0AD0, 0x0AD0),
		interval(0x0AE0, 0x0AE3),
		interval(0x0AE6, 0x0AEF),
		interval(0x0AF1, 0x0AF1)
		]],
[19,	'Oriya',     [interval(0x0B01, 0x0B03),
		interval(0x0B05, 0x0B0C),
		interval(0x0B0F, 0x0B10),
		interval(0x0B13, 0x0B28),
		interval(0x0B2A, 0x0B30),
		interval(0x0B32, 0x0B33),
		interval(0x0B35, 0x0B39),
		interval(0x0B3C, 0x0B44),
		interval(0x0B47, 0x0B48),
		interval(0x0B4B, 0x0B4D),
		interval(0x0B56, 0x0B57),
		interval(0x0B5C, 0x0B5D),
		interval(0x0B5F, 0x0B63),
		interval(0x0B66, 0x0B71),
	]],
[20,	'Tamil',     [interval(0x0B82, 0x0B83),
		interval(0x0B85, 0x0B8A),
		interval(0x0B8E, 0x0B91),
		interval(0x0B92, 0x0B95),
		interval(0x0B99, 0x0B9A),
		interval(0x0B9C, 0x0B9C),
		interval(0x0B9E, 0x0B9F),
		interval(0x0BA3, 0x0BA4),
		interval(0x0BA8, 0x0BAA),
		interval(0x0BAE, 0x0BB9),
		interval(0x0BBE, 0x0BC2),
		interval(0x0BC6, 0x0BC8),
		interval(0x0BCA, 0x0BCD),
		interval(0x0BD0, 0x0BD0),
		interval(0x0BD7, 0x0BD7),
		interval(0x0BE6, 0x0BFA)
	]],
[21,	'Telugu',     [interval(0x0C01, 0x0C03),
		interval(0x0C05, 0x0C0C),
		interval(0x0C0E, 0x0C11),
		interval(0x0C12, 0x0C28),
		interval(0x0C2A, 0x0C33),
		interval(0x0C35, 0x0C39),
		interval(0x0C3d, 0x0C44),
		interval(0x0C46, 0x0C48),
		interval(0x0C4a, 0x0C4d),
		interval(0x0C55, 0x0C56),
		interval(0x0C58, 0x0C59),
		interval(0x0C60, 0x0C63),
		interval(0x0C66, 0x0C6f),
		interval(0x0C78, 0x0C7f),
			]
			],
[22,	'Kannada',     [interval(0x0C82, 0x0C83),
		interval(0x0C85, 0x0C8C),		
		interval(0x0C8E, 0x0C90),		
		interval(0x0C92, 0x0CA8),		
		interval(0x0CAA, 0x0CB3),		
		interval(0x0CB5, 0x0CB9),		
		interval(0x0CBC, 0x0CC4),		
		interval(0x0CC6, 0x0CC8),		
		interval(0x0CCA, 0x0CCD),		
		interval(0x0CD5, 0x0CD6),		
		interval(0x0CDE, 0x0CDE),		
		interval(0x0CE0, 0x0CE3),		
		interval(0x0CE6, 0x0CEF),		
		interval(0x0CF1, 0x0CF2),		
	]],
[23,	'Malayalam',     [interval(0x0D02, 0x0D03),
		interval(0x0D05, 0x0D0C),
		interval(0x0D0E, 0x0D10),
		interval(0x0D12, 0x0D28),
		interval(0x0D2A, 0x0D39),
		interval(0x0D3D, 0x0D44),
		interval(0x0D46, 0x0D48),
		interval(0x0D4A, 0x0D4D),
		interval(0x0D57, 0x0D57),
		interval(0x0D60, 0x0D63),
		interval(0x0D66, 0x0D75),
		interval(0x0D79, 0x0D7F),
	]],
[24,	'Thai',     [interval(0x0E01, 0x0E3A),
			interval(0x0E3F, 0x0E5B)
			]
		],
[25,	'Lao',     [interval(0x0E80, 0x0EFF)]],
[26,	'Georgian (+supplement)',    [
		interval(0x10A0, 0x10C5),
		interval(0x10D0, 0x10FC)]],	# Supplement
[27,	'Balinese', [interval(0x1B00, 0x1B7F)]],
[28,	'Hangul Jamo',     [interval(0x1100, 0x11FF)]],
[29,	'Latin Extended (Additional,C,D)',     [
		interval(0x1E00, 0x1EFF),	# Additional
		interval(0x2C60, 0x2C6F),	# C
		interval(0x2C71, 0x2C7D),	# C
		interval(0xA720, 0xA78C),	# D
		interval(0xA7FB, 0xA7FF)	# D
		]],
[30,	'Greek Extended',     [interval(0x1F00, 0x1F15),
		interval(0x1F18, 0x1F1D),
		interval(0x1F20, 0x1F45),
		interval(0x1F48, 0x1F4D),
		interval(0x1F50, 0x1F57),
		interval(0x1F59, 0x1F59),
		interval(0x1F5B, 0x1F5B),
		interval(0x1F5D, 0x1F5D),
		interval(0x1F5F, 0x1F7D),
		interval(0x1F80, 0x1FB4),
		interval(0x1FB6, 0x1FC4),
		interval(0x1FC6, 0x1FD3),
		interval(0x1FD6, 0x1FDB),
		interval(0x1FDD, 0x1FEF),
		interval(0x1FF2, 0x1FF4),
		interval(0x1FF6, 0x1FFE)
	]],
[31,	'General Punctuation (+suppl)',     [interval(0x2000, 0x2064),
		interval(0x206A, 0x206F),
		interval(0x2E00, 0x2E30),	# Supplemental
	]],
[32,	'Superscripts and Subscripts',     [interval(0x2070, 0x2071),
		interval(0x2074, 0x208E),
		interval(0x2090, 0x2094)
	]
	],
[33,	'Currency Symbols',     [interval(0x20A0, 0x20B5)]],
[34,	'Combining Diacritical Marks for Symbols',     [interval(0x20D0, 0x20F0)]],
[35,	'Letterlike Symbols',     [interval(0x2100, 0x214F)]],
[36,	'Number Forms',     [interval(0x2153, 0x2188)]],
[37,	'Arrows (+suppl)',     [interval(0x2190, 0x21FF),
	interval(0x27F0, 0x27FF),	# Supplemental Arrows-A
	interval(0x2900, 0x297F),	# Supplemental Arrows-B
	interval(0x2B00, 0x2BFF)	# Miscellaneous Symbols and Arrows
	]],
[38,	'Mathematical Operators',     [ 
	interval(0x2200, 0x22FF),
	interval(0x2A00, 0x2AFF),	# Supplemental Mathematical Operators
	interval(0x27C0, 0x27CA),	# Miscellaneous Mathematical Symbols-A
	interval(0x27CC, 0x27CC),
	interval(0x27D0, 0x27EF),
	interval(0x2980, 0x29FF)	# Miscellaneous Mathematical Symbols-B
	]
		],
[39,	'Miscellaneous Technical',     [interval(0x2300, 0x23E7)]],
[40,	'Control Pictures',     [interval(0x2400, 0x2426)]],
[41,	'Optical Character Recognition',     [interval(0x2440, 0x244A)]],
[42,	'Enclosed Alphanumerics',     [interval(0x2460, 0x24FF)]],
[43,	'Box Drawing',     [interval(0x2500, 0x257F)]],
[44,	'Block Elements',     [interval(0x2580, 0x259F)]],
[45,	'Geometric Shapes',     [interval(0x25A0, 0x25FF)]],
[46,	'Miscellaneous Symbols',     [
			interval(0x2600, 0x269D),
			interval(0x26A0, 0x26C3)
			]
			],
[47,	'Dingbats',     [interval(0x2701, 0x2704),
			interval(0x2706, 0x2709),
			interval(0x270C, 0x2727),
			interval(0x2729, 0x274B),
			interval(0x274D, 0x274D),
			interval(0x274F, 0x2752),
			interval(0x2756, 0x2756),
			interval(0x2758, 0x275E),
			interval(0x2761, 0x2794),
			interval(0x2798, 0x27AF),
			interval(0x27B1, 0x27BE)
	]],
[48,	'CJK Symbols and Punctuation', [interval(0x3000, 0x303F)]],
[49,	'Hiragana', [interval(0x3040, 0x309F)]],
[50,	'Katakana', [interval(0x30A0, 0x30FF)]],
[51,	'Bopomofo', [interval(0x3100, 0x312F)]],
[52,	'Hangul Compatibility Jamo', [interval(0x3130, 0x318F)]],
[53,	'CJK Miscellaneous', [interval(0x3190, 0x319F)]],
[54,	'Enclosed CJK Letters and Months', [interval(0x3200, 0x32FF)]],
[55,	'CJK Compatibility', [interval(0x3300, 0x33FF)]],
[56,	'Hangul', [interval(0x3400, 0x3D2D)]],
[57,	'Non-Plane 0', [interval(0xD800, 0xDFFF)]],
[58,	'Phoenician', [interval(0x10900, 0x1091B), 
		interval(0x1091F, 0x1091F)], True],
[59,	'CJK Unified Ideographs', [interval(0x4E00, 0x9FFF)]], #FIXME complex
[60,	'Private Use Area', [interval(0xE800, 0xF8FF)]],
[61,	'CJK Compatibility Ideographs', [interval(0xF900, 0xFAFF)]],
[62,	'Alphabetic Presentation Forms', [
			interval(0xFB00, 0xFB06),
			interval(0xFB13, 0xFB17),
			interval(0xFB1D, 0xFB36),
			interval(0xFB38, 0xFB3C),
			interval(0xFB3E, 0xFB3E),
			interval(0xFB40, 0xFB41),
			interval(0xFB43, 0xFB44),
			interval(0xFB46, 0xFB4F),
		]],
[63,	'Arabic Presentation Forms-A', [interval(0xFB50, 0xFBB1),
				interval(0xFBD3, 0xFD3F),
				interval(0xFD50, 0xFD8F),
				interval(0xFD92, 0xFDC7),
				interval(0xFDF0, 0xFDFD)
				]
		],
[64,	'Combining Half Marks', [interval(0xFE20, 0xFE2F)]],
[65,	'CJK Compatibility Forms', [interval(0xFE10, 0xFE1F),	# Vertical forms
		interval(0xFE30, 0xFE4F)	# Compatability forms
	]],
[66,	'Small Form Variants', [interval(0xFE50, 0xFE52),
				interval(0xFE54, 0xFE66),
				interval(0xFE58, 0xFE5B)
				]
		],
[67,	'Arabic Presentation Forms-B', [interval(0xFE70, 0xFE74),
				interval(0xFE76, 0xFEFC),
				interval(0xFEFF, 0xFEFF)
				]
		],
[68,	'Halfwidth and Fullwidth Forms', [interval(0xFF00, 0xFFEF)]],
[69,	'Specials', [interval(0xFFF9, 0xFFFD)]],
[70, 	'Tibetan', [interval(0x0F00, 0x0FFF)]],
[71, 	'Syriac', [interval(0x0700, 0x070D),
		interval(0x070F, 0x074A),
		interval(0x074D, 0x074F)
	]],
[72, 	'Thaana', [interval(0x0780, 0x07B1)]],
[73, 	'Sinhala', [interval(0x0D82, 0x0D83),
		interval(0x0D85, 0x0D96),
		interval(0x0D9A, 0x0DB1),
		interval(0x0DB3, 0x0DBB),
		interval(0x0DBD, 0x0DBD),
		interval(0x0DC0, 0x0DC6),
		interval(0x0DCA, 0x0DCA),
		interval(0x0DCF, 0x0DD4),
		interval(0x0DD6, 0x0DD6),
		interval(0x0DD8, 0x0DDF),
		interval(0x0DF2, 0x0DF4)]],
[74, 	'Myanmar', [interval(0x1000, 0x109F)]],
[75, 	'Ethiopic (+supplement, extended)', [
		interval(0x1200, 0x1248),
		interval(0x124A, 0x124D),
		interval(0x1250, 0x1256),
		interval(0x1258, 0x1258),
		interval(0x125A, 0x125D),
		interval(0x1260, 0x1288),
		interval(0x128A, 0x128D),
		interval(0x1290, 0x12B0),
		interval(0x12B2, 0x12B5),
		interval(0x12B8, 0x12BE),
		interval(0x12C0, 0x12C0),	# page 2
		interval(0x12C2, 0x12C5),
		interval(0x12C8, 0x12D6),
		interval(0x12D8, 0x1310),
		interval(0x1312, 0x1315),
		interval(0x1318, 0x135A),
		interval(0x135F, 0x137C),
		interval(0x1380, 0x139F),	# supplement
		interval(0x2D80, 0x2DDF)	# extended
		]
		],
[76,	'Cherokee', [interval(0x13A0, 0x13F4)]],
[77, 	'Unified Canadian Aboriginal Syllabics', [interval(0x1401, 0x1676)]],
[78, 	'Ogham', [interval(0x1680, 0x169F)]],
[79, 	'Runic', [interval(0x16A0, 0x16F1)]],
[80, 	'Khmer (+symbols)', [interval(0x1780, 0x17FF),
		interval(0x19E0, 0x19FF)	# symbols
	]],
[81, 	'Mongolian', [interval(0x1800, 0x18AF)]],	#FIXME ranges
[82, 	'Braille Patterns', [interval(0x2800, 0x28FF)]],
[83, 	'Yi Syllables, Radicals', [interval(0xA000, 0xA0EF),
		interval(0xA490, 0xA4CF)]
		],
[84, 	'Tagalog Hanunoo Buhid Tagbanwa', 
		[interval(0x1700, 0x1714),
		interval(0x1720, 0x1736),
		interval(0x1740, 0x1753),
		interval(0x1750, 0x1773)
		]
		],
[85, 	'Old Italic', [interval(0x10300, 0x10320)], True],
[86, 	'Gothic', [interval(0x10330, 0x1034A)], True],
[87, 	'Deseret', [interval(0x10400, 0x1044F)], True],
[88, 	'Byzantine &amp; Western Musical Symbols', [interval(0x1D000, 0x1D0F5),
			interval(0x1D100, 0x1D126),
			interval(0x1D129, 0x1D1DD)
			], True],
[89, 	'Mathematical Alphanumeric Symbols', [interval(0x1D400, 0x1D454),
		interval(0x1D456, 0x1D49C),
		interval(0x1D49E, 0x1D49F),
		interval(0x1D4A2, 0x1D4A2),
		interval(0x1D4A5, 0x1D4A6),
		interval(0x1D4A9, 0x1D4AC),
		interval(0x1D4AE, 0x1D4B9),
		interval(0x1D4BB, 0x1D4BB),
		interval(0x1D4BD, 0x1D4C3),
		interval(0x1D4C5, 0x1D4FF),
		interval(0x1D500, 0x1D505),	# page 2
		interval(0x1D507, 0x1D50A),
		interval(0x1D50D, 0x1D514),
		interval(0x1D516, 0x1D51C),
		interval(0x1D51E, 0x1D539),
		interval(0x1D53B, 0x1D53E),
		interval(0x1D540, 0x1D544),
		interval(0x1D546, 0x1D546),
		interval(0x1D54A, 0x1D550),
		interval(0x1D552, 0x1D5FF),	
		interval(0x1D600, 0x1D6A5),	# page 3
		interval(0x1D6A8, 0x1D6FF),
		interval(0x1D700, 0x1D7CB),	# page 4
		interval(0x1D7CE, 0x1D7FF),
	], True],
[90, 	'Private Use (plane 15,16)', [
		interval(0xFF000, 0xFFFFD),	# plane 15
		interval(0x100000, 0x10FFFD)	# plane 16
	], True],
[91, 	'Variation Selectors (+suppl)', [interval(0xFE00, 0xFE0F),
		interval(0xE0100, 0xE01EF)	# supplement
		], True],
[92, 	'Tags', [interval(0xE0000, 0xE01EF)], True],
[93, 	'Limbu', [interval(0x1900, 0x194F)]],
[94, 	'Tai Le', [interval(0x1950, 0x196D),
		interval(0x1970, 0x1974)
	]],
[95, 	'New Tai Lue', [interval(0x1980, 0x19DF)]],
[96, 	'Buginese', [interval(0x1A00, 0x1A1B),
		interval(0x1A1E, 0x1A1F)]],
[97, 	'Glagolitic', [ interval(0x2C00, 0x2C2E),
		interval(0x2C30, 0x2C5E) ]],
[98, 	'Tifinagh', [interval(0x2D30, 0x2D65),
		interval(0x2D6F, 0x2D6F)
	]],
[99, 	'Ying Hexagram Symbols', [interval(0x4DC0, 0x4DFF)]],
[100, 	'Syloti Nagri', [interval(0xA800, 0xA82F)]],
[101, 	'Linear B Syllabary etc', [interval(0x10000, 0x1013F)], True],
[102, 	'Ancient Greek Numbers', [interval(0x10140, 0x1018F)], True],
[103, 	'Ugaritic', [interval(0x10380, 0x1039D),
		interval(0x1039F, 0x1039F)
	], True],
[104, 	'Old Persian', [interval(0x103A0, 0x103C3),
		interval(0x103C8, 0x103D6),
	], True],
[105, 	'Shavian', [interval(0x10450, 0x1047F)], True],
[106, 	'Osmanya', [interval(0x10480, 0x104AF)], True],
[107, 	'Cypriot Syllabary', [interval(0x10800, 0x1083F)], True],
[108, 	'Kharoshthi', [interval(0x10A00, 0x10A5F)], True],
[109, 	'Tai Xuan Jing Symbols', [interval(0x1D300, 0x1D35F)], True],
[110, 	'Cuneiform (+numbers)', [interval(0x12000, 0x1247F)], True],
[111, 	'Counting Rod Numerals', [interval(0x1D360, 0x1D37F)], True],
[112, 	'Sundanese', [interval(0x1B80, 0x1BBF)]],
[113, 	'Lepcha', [interval(0x1C00, 0x1C4F)]],
[114, 	'Ol Chiki', [interval(0x1C50, 0x1C7F)]],
[115, 	'Saurashtra', [interval(0xA880, 0xA8DF)]],
[116, 	'Kayah Li', [interval(0xA900, 0xA92F)]],
[117, 	'Reiang', [interval(0xA930, 0xA95F)]],
[118, 	'Cham', [interval(0xAA00, 0xAA5F)]],
[119, 	'Ancient Symbols', [interval(0x10190, 0x101CF)], True],
[120, 	'Phaistos Disc', [interval(0x101D0, 0x101FF)], True],
[121, 	'Carian, Lycian, Lydian', [interval(0x102A0, 0x102DF),
		interval(0x10280, 0x1029F),	# Lycian
		interval(0x10920, 0x1093F)	# Lydian
	], True],
[122, 	'Domino and Mahjong Tiles', [
		interval(0x1F000, 0x1F02B),	# Mahjong
		interval(0x1F030, 0x1F093)	# Domino
	], True],
#[96-127, 	'Reserved for Unicode SubRanges', []]
]

"""
From the OpenType standard 
http://www.microsoft.com/OpenType/OTSpec/os2.htm

0 	Basic Latin
1 	Latin-1 Supplement
2 	Latin Extended-A
3 	Latin Extended-B
4 	IPA Extensions
5 	Spacing Modifier Letters
6 	Combining Diacritical Marks
7 	Greek and Coptic
8 	Reserved for Unicode SubRanges
9 	Cyrillic
  	Cyrillic Supplementary
10 	Armenian
11 	Hebrew
12 	Reserved for Unicode SubRanges
13 	Arabic
14 	Reserved for Unicode SubRanges
15 	Devanagari
16 	Bengali
17 	Gurmukhi
18 	Gujarati
19 	Oriya
20 	Tamil
21 	Telugu
22 	Kannada
23 	Malayalam
24 	Thai
25 	Lao
26 	Georgian
27 	Reserved for Unicode SubRanges
28 	Hangul Jamo
29 	Latin Extended Additional
30 	Greek Extended
31 	General Punctuation
32 	Superscripts And Subscripts
33 	Currency Symbols
34 	Combining Diacritical Marks For Symbols
35 	Letterlike Symbols
36 	Number Forms
37 	Arrows
  	Supplemental Arrows-A
  	Supplemental Arrows-B
38 	Mathematical Operators
  	Supplemental Mathematical Operators
  	Miscellaneous Mathematical Symbols-A
  	Miscellaneous Mathematical Symbols-B
39 	Miscellaneous Technical
40 	Control Pictures
41 	Optical Character Recognition
42 	Enclosed Alphanumerics
43 	Box Drawing
44 	Block Elements
45 	Geometric Shapes
46 	Miscellaneous Symbols
47 	Dingbats
48 	CJK Symbols And Punctuation
49 	Hiragana
50 	Katakana
  	Katakana Phonetic Extensions
51 	Bopomofo
  	Bopomofo Extended
52 	Hangul Compatibility Jamo
3 	Reserved for Unicode SubRanges
54 	Enclosed CJK Letters And Months
55 	CJK Compatibility
56 	Hangul Syllables
57 	Non-Plane 0 *
58 	Reserved for Unicode SubRanges
59 	CJK Unified Ideographs
  	CJK Radicals Supplement
  	Kangxi Radicals
  	Ideographic Description Characters
  	CJK Unified Ideograph Extension A
  	CJK Unified Ideographs Extension B
  	Kanbun
60 	Private Use Area
61 	CJK Compatibility Ideographs
  	CJK Compatibility Ideographs Supplement
62 	Alphabetic Presentation Forms
63 	Arabic Presentation Forms-A
64 	Combining Half Marks
65 	CJK Compatibility Forms
66 	Small Form Variants
67 	Arabic Presentation Forms-B
68 	Halfwidth And Fullwidth Forms
69 	Specials
70 	Tibetan
71 	Syriac
72 	Thaana
73 	Sinhala
74 	Myanmar
75 	Ethiopic
76	Cherokee
77 	Unified Canadian Aboriginal Syllabics
78 	Ogham
79 	Runic
80 	Khmer
81 	Mongolian
82 	Braille Patterns
83 	Yi Syllables
  	Yi Radicals
84 	Tagalog
  	Hanunoo
  	Buhid
  	Tagbanwa
85 	Old Italic
86 	Gothic
87 	Deseret
88 	Byzantine Musical Symbols
  	Musical Symbols
89 	Mathematical Alphanumeric Symbols
90 	Private Use (plane 15)
  	Private Use (plane 16)
91 	Variation Selectors
92 	Tags
93-127 	Reserved for Unicode SubRanges
"""
"""
Overview of the BMP (group=00, plane=00)

======= A-ZONE (alphabetical characters and symbols) =======================
00      (Control characters,) Basic Latin, Latin-1 Supplement (=ISO/IEC 8859-1)
01      Latin Extended-A, Latin Extended-B
02      Latin Extended-B, IPA Extensions, Spacing Modifier Letters
03      Combining Diacritical Marks, Basic Greek, Greek Symbols and Coptic
04      Cyrillic
05      Armenian, Hebrew
06      Basic Arabic, Arabic Extended
07--08  (Reserved for future standardization)
09      Devanagari, Bengali
0A      Gumukhi, Gujarati
0B      Oriya, Tamil
0C      Telugu, Kannada
0D      Malayalam
0E      Thai, Lao
0F      (Reserved for future standardization)
10      Georgian
11      Hangul Jamo
12--1D  (Reserved for future standardization)
1E      Latin Extended Additional
1F      Greek Extended
20      General Punctuation, Super/subscripts, Currency, Combining Symbols
21      Letterlike Symbols, Number Forms, Arrows
22      Mathematical Operators
23      Miscellaneous Technical Symbols
24      Control Pictures, OCR, Enclosed Alphanumerics
25      Box Drawing, Block Elements, Geometric Shapes
26      Miscellaneous Symbols
27      Dingbats
28--2F  (Reserved for future standardization)
30      CJK Symbols and Punctuation, Hiragana, Katakana
31      Bopomofo, Hangul Compatibility Jamo, CJK Miscellaneous
32      Enclosed CJK Letters and Months
33      CJK Compatibility
34--4D  Hangul

======= I-ZONE (ideographic characters) ===================================
4E--9F  CJK Unified Ideographs

======= O-ZONE (open zone) ================================================
A0--DF  (Reserved for future standardization)

======= R-ZONE (restricted use zone) ======================================
E0--F8  (Private Use Area)
F9--FA  CJK Compatibility Ideographs
FB      Alphabetic Presentation Forms, Arabic Presentation Forms-A
FC--FD  Arabic Presentation Forms-A
FE      Combining Half Marks, CJK Compatibility Forms, Small Forms, Arabic-B
FF      Halfwidth and Fullwidth Forms, Specials
"""

"""
See also
http://developer.apple.com/textfonts/TTRefMan/RM06/Chap6OS2.html
Says 128 bits are split into 96 and 32 bits.
96 is Unicode block, 32 for script sets...

This talks about TrueType and OpenType versions
http://webcenter.ru/~kazarn/eng/fonts_ttf.htm#os2tab
and this says what the ranges of Hebrew, Greek etc are

OK, the right thing is here: the OpenType specs
http://www.microsoft.com/OpenType/OTSpec/os2.htm
"""

def total_intervals( intervals ):
	num = 0
	for i in intervals:
		num += i.len()
	return num

def count_glyphs_in_intervals( font, intervals ):
	num = 0
	for r in intervals:
		# select() will throw up if try to select value 
		# beyond the range of the encoding
		if r.begin < len( font ) and r.end < len( font ):
			try: 
				font.selection.select( ( 'ranges', None ),
					r.begin, r.end )
				g = font.selection.byGlyphs
				for e in g:
					num += 1
			except ValueError:
				print >> sys.stderr, "interval " + str( r ) \
				+ " not representable in " + font.fontname
				exit( 1 )
	return num

def glyphHasRange( encoding ):
	for ulr in ulUnicodeRange:
		ranges = ulr[2]
		for r in ranges:
			if r.contains( encoding ):
				return True
	return False

class SupportInfo:
	def __init__( self, os2bit, supports, total ):
		self.os2bit = os2bit
		self.supports = supports
		self.total = total

class FontSupport:
	""" A record of support for all OS/2 ranges within a single font.
	    Uses a dictionary internally, to avoid loss of the index info.
	"""
	def __init__( self, fontPath, short ):
		font = fontforge.open( fontPath )
		self.name = font.fontname
		self.short = short
		self.myInfos = {}
		self.totalGlyphs = 0
		self.fontTotalGlyphs = 0

		r = font.os2_unicoderanges

		# print >> sys.stderr, font.fontname, hex( r[0] ), hex( r[1] ),hex( r[2] ),hex( r[3] );

		nRanges = len( ulUnicodeRange )

		for index in range( 0, nRanges ):
			byte = index / 32
			bit = index % 32

			self.collectRangeInfo( font, r[byte], bit, index )

		for f in font.glyphs():
			self.fontTotalGlyphs += 1
			if not glyphHasRange( f.encoding ):
				print >> sys.stderr, font.fontname, \
					"no range for", hex( f.encoding ) \
					+ " '" + f.glyphname + "'"

	def collectRangeInfo( self, font, os2supportbyte, bit, index ):
		supports = ( os2supportbyte & (1 << bit) ) != 0
		rangeName = ulUnicodeRange[index][1]
		intervals = ulUnicodeRange[index][2]
		nglyphs = count_glyphs_in_intervals( font, intervals )
		self.setRangeSupport( index, supports, nglyphs )
		self.totalGlyphs += nglyphs

	def setRangeSupport( self, idx, supports, total ):
		if self.myInfos.has_key( idx ):
			print >> sys.stderr, "OS/2 index", idx, " duplicated"
			exit( 1 )
		self.myInfos[idx] = SupportInfo( idx, supports, total )

	def getInfo( self, idx ):
		if not self.myInfos.has_key( idx ):
			print >> sys.stderr, "OS/2 index", idx, " not found"
			exit( 1 )
		return self.myInfos[ idx ]

def print_font_range_table( fontSupportList ):
	print '<table class="fontrangereport" cellspacing="0" cellpadding="0" frame="box" rules="all">'
	print '<caption>'
	print "OS/2 character ranges vs. FreeFont faces " 
	print '</caption>'
	print '<colgroup>'
	print '<col /><col /><col />'
	print '</colgroup>'
	print '<colgroup>'
	print '<col class="roman"/><col /><col /><col />'
	print '<col /><col /><col /><col />'
	print '</colgroup>'
	print '<colgroup>'
	print '<col class="roman"/><col /><col /><col />'
	print '<col /><col /><col /><col />'
	print '</colgroup>'
	print '<colgroup>'
	print '<col class="roman"/><col /><col /><col />'
	print '<col /><col /><col /><col />'
	print '</colgroup>'
	print '<thead>'
	print '<tr><th>OS/2 character range</th>' 
	print '<th>range<br />total</th>' 
	print '<td></td>' 
	for fsl in fontSupportList:
		print '<th colspan="2">' + fsl.short + '</th>' 
	print '</tr>'
	print '</thead>'
	for r in ulUnicodeRange:
		idx = r[0]
		range_name = r[1]
		intervals = r[2]

		rowclass = ' class="low"'
		if len( ulUnicodeRange[idx] ) > 3 and ulUnicodeRange[ idx ][3]:
			rowclass = ' class="high"'
			
		print '<tr' + rowclass + '><td>' + range_name + '</td>' 
		print '<td class="num">' + str( total_intervals( intervals ) ) \
			+ '</td>'
		print '<td></td>' 
		for fsl in fontSupportList:
			supportInfo = fsl.getInfo( idx )
			supportString = ''
			if supportInfo.supports:
				supportString = '&bull;'
			totalStr = str( supportInfo.total )
			if not supportInfo.total:
				totalStr = '&nbsp;'

			print '<td class="num">' \
				+ totalStr \
				+ '</td><td>'	\
				+ supportString \
				+ '</td>'

		print '</tr>'
	print '<tr><th colspan="3">ranges total</th>' 
	for fsl in fontSupportList:
		print '<td class="num" colspan="2">' \
			+ str( fsl.totalGlyphs ) \
			+ '&nbsp;</td>'
	print '</tr>'
	print '<tr><th colspan="3">font total</th>' 
	for fsl in fontSupportList:
		print '<td class="num" colspan="2">' \
			+ str( fsl.fontTotalGlyphs ) \
			+ '&nbsp;</td>'
	print '</tr>'
	# Would also like to total glyphs in ranges for each font,
	# and also print total glyphs in each font.
	print '</table>'
table_introduction = """
For historical reasons, TrueType classifies Unicode ranges according to
an extension of the old OS/2 character ranges.  This table shows how many
characters FontForge finds in each of the ranges for each face in the family.
"""

table_explanation = """
<p>
Ranges for which (FontForge reports that) the font's OS/2 support
bit is set are marked with a bullet.
</p>
<p>
The "font total" row is the total number of glyphs in the font, whereas 
"ranges total" is the total number of glyphs within the listed ranges.
The numbers should be the same.
</p>
<p>
For many ranges, I took the liberty of reducing the set of characters
considered to those listed for the range in the current Unicode charts.
The number of characters supported can thus be less than the width of the range.
</p>
<p>
Note that there is a discrepancy in the Greek Symbols, Hebrew Extended and
Arabic Extended ranges, between what FontForge reports here and in its Font
Info window under OS/2 Character Ranges. I don't know why, but these ranges
are also not well defined in the TrueType standard.
</p>
<p>
Note the two characters from Devanagri.  These are the danda and double-danda
used by other Indic scripts.
</p>
<p>
The ranges <span style="color: gray">beyond Unicode point 0xFFFF</span>, are
shaded.  </p>
"""

def print_font_range_report( fontSupportList ):
	print '<html>'
	print '<head>'
	print '<p>'
	print table_introduction
	print '</p>'
	print '<title>'
	print 'Gnu FreeFont character range support'
	print '</title>'
	print '<style type="text/css">'
	print '	tr.high { color: gray }'
	print '	td.num { text-align: right }'
	print '	td { padding-right: 0.25ex }'
	print '	th { padding: 0.25ex }'
	print '	.roman { border-left: medium black solid; }'
	print '	caption { font-size: larger; font-weight: bold; }'
	print '</style>'
	print '</head>'
	print '<body>'
	print '<h1>'
	print 'Gnu FreeFont support for OpenType OS/2 character ranges'
	print '</h1>'
	print_font_range_table( fontSupportList )
	print '<p>'
	print table_explanation
	time.tzset()
	print 'Generated by <code>ranges.py</code> on ' \
			+ time.strftime('%X %x %Z') + '.'
	print '</p>'
	print '</body>'
	print '</html>'

supportList = []
supportList.append( FontSupport( '../sfd/FreeSerif.sfd', 'Srf' ) )
supportList.append( FontSupport( '../sfd/FreeSerifItalic.sfd', 'Srf I' ) )
supportList.append( FontSupport( '../sfd/FreeSerifBold.sfd', 'Srf B' ) )
supportList.append( FontSupport( '../sfd/FreeSerifBoldItalic.sfd', 'Srf BI' ) )
supportList.append( FontSupport( '../sfd/FreeSans.sfd', 'Sans' ) )
supportList.append( FontSupport( '../sfd/FreeSansOblique.sfd', 'Sans O' ) )
supportList.append( FontSupport( '../sfd/FreeSansBold.sfd', 'Sans B' ) )
supportList.append( FontSupport( '../sfd/FreeSansBoldOblique.sfd', 'Sans BO' ) )
supportList.append( FontSupport( '../sfd/FreeMono.sfd', 'Mono' ) )
supportList.append( FontSupport( '../sfd/FreeMonoOblique.sfd', 'Mono O' ) )
supportList.append( FontSupport( '../sfd/FreeMonoBold.sfd', 'Mono B' ) )
supportList.append( FontSupport( '../sfd/FreeMonoBoldOblique.sfd', 'Mono BO' ) )

print_font_range_report( supportList )
