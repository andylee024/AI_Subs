
import goslate

"""
TODO:
1. specify import path for dictionary object in Annotater constructor 

Notes:
1. goslate translation object can be optimized by batching all translations into one iterable (i.e. list or tuple)

"""

"""
Base Class
"""
class Annotater:
	def __init__(self, level):
		self.user_level = level
		self.annotation_type = "blank"
		self.D = adapt_dictionary.D_bot() #specify import path 

	def annotate():
		pass

"""
Derived classes
"""
# Fields
# @param int level : specifies user level
# @param int annotation_type : score combining user level and content difficulty that determines optimal highlighting scheme

# Methods
# annotate(): takes word and annotation_type and returns transformed word 

class ENG_Annotater(Annotater):
	def __init__(self, level):
		Annotater.__init__(level)
		d_freq = (self.D).build_eng_freq

	def annotate(self, word):
		pass



class JPN_Annotater(Annotater):
	
	def __init__(self, level):
		Annotater.__init__(level)
		self.d_freq = (self.D).build_jpn_freq  
		self.hira = (self.D).build_jpn_hira


	def annotate_hira(self,word):
		if word in self.d_freq:

			#option 1 - green (hira) + english 
			if self.level == 0:
				rank = d_freq[word]
				if rank > 40 and rank < 60:
					hira = green_highlight(convert_to_hiragana(word, self.hira))
					translation = translate(word, color='green', source='ja', target='en')
					return hira + " " + translation
				
				return word

			#option 2 - green (hira) + red ( hira + english)
			elif self.level == 1:
				rank = d_freq[word]
				if rank > 75 and rank < 200:
					hira = "(" + green_highlight( + convert_to_hiragana(word, self.hira)) + ")"
					word = green_highlight(word)
					return word + " " + hira

				elif rank >= 200 and rank <=300:
					hira = red_highlight( convert_to_hiragana(word, self.hira) )
					translation = red_highlight( translate(word, color='green', source='ja', target='en')) 
					return hira + " " + translation 

				return word  
			
			#option 3 - green (hira) + red (hira) (english)
			elif self.level == 3:
				if rank < 300: 
					return word 
				
				if rank >= 300 and rank < 500:
					kanji = green_highlight(word)
					hira = "(" + green_highlight(convert_to_hiragana(word, self.hira)) + ")"
					return kanji + " " + hira

				if rank >= 500 and rank < 800:
					hira = red_highlight(convert_to_hiragana(word, self.hira))
					translation = translate(word, color='red', source='ja', target='en')
					return hira + " " + translation 

			else:
				return word 
		
		return word 




"""
Helper functions for highlighting and transforming words
"""

#takes kanji and converts to hiragana using kanji:hiragana dictionary
def convert_to_hiragana(kanji, d):
	if kanji in d: return d[kanji]
	else: return kanji

#takes a word and applies color highlighting
def red_highlight(word):
	red_start = "{\c&H0708F1&}"
	red_end = "{\c&HFFFFFF&}"
	return red_start + word + red_end

def green_highlight(word):
	green_start =  "{\c&H14EB05&}"
	green_end = "{\c&HFFFFFF&}"
	return green_start + word + green_end

def translate(word, color=None, source=None, target = 'en'):
	gs = goslate.Goslate() #translation object
	translation = gs.translate(word, source_language = source, target_language = target)
	if color == None:
		return " (" + translation + " )"
	if color == "green":
		return " (" + green_highlight(translation) + " )"
	if color == "red":
		return " (" + red_highlight(translation) + " )" 

