"""
Suite of annotation settings for highlighting/converting/translating individual words.
"""

import goslate

#takes kanji and converts to hiragana using kanji:hiragana dictionary
def convert_to_hiragana(kanji, d):
	if kanji in d: return d[kanji]
	else: return kanji

#takes a word and applies color highlighting
def red_highlight(word, d):
	red_start = "{\c&H0708F1&}"
	red_end = "{\c&HFFFFFF&}"
	return red_start + word + red_end

def green_highlight(word, d):
	green_start =  "{\c&H14EB05&}"
	green_end = "{\c&HFFFFFF&}"
	return green_start + word + green_end

#currently only supports japanese
def translate(word, color=None):
	gs = goslate.Goslate() #translation object
	translation = gs.translate(word, 'en', source_language='ja')
	if color == None:
		return " (" + translation + " )"
	if color == "green":
		return " (" + green_highlight(translation) + " )"
	if color == "red":
		return " (" + red_highlight(translation) + " )" 

