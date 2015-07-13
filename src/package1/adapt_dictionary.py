# -*- coding: utf-8 -*-
"""
This module builds the following dictionaries that are useful for translation services. 
	1. english frequency list (1-5000)
	2. japanese frequency list (1-20000)
	3. japanese (kanji: hiragana) dictionary

It is important to remember that all our dictionary entries for japanese are being encoded in utf-8, so to display them correctly
we'll need to decode them from "utf-8". See test1.py for implementation details.

Notes:
1. Exception detection in jpn_hira
  Some lines in the dictionary file require special attention to process correctly. jpnhira1.txt contains a collection of types of lines
  we have come across in the dictionary. Details on how to process those lines are also included in the file. 

"""
import re
import codecs #library to read input in utf-8
import pandas as pd
import string
import chardet

class D_bot:
	def __init__(self):
		#set data fields
		self.eng_freq = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/5000wordfrequencylist.csv"
		self.jpn_freq1 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/1-10000_frequency_list_japanese.csv" 
		self.jpn_freq2 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/10001-20000_frequency_list_japanese.csv"
		self.jpn_hira_path = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/EDICT2.txt"

		self.eng = {}
		self.jpn = {}
		self.jpn_hira = {}

		self.error_log = open("/home/andy/Documents/Projects/AI_Subs/test/logs/error_log_dict.txt","w")

		#initialize dictionaries
		#build_eng_freq()
		#build_jpn_freq()
		#build_jpn_hira()
	

	def build_eng_freq(self):
		#initialization
		d = {}
		path = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/5000wordfrequencylist.csv"
		
		#processing
		df = pd.read_csv(path header=0)
		word_list = df['Word'][1:]
		rank_list = df['Rank'][1:]
		for i in range(1, len(word_list)+1): #iterate through words to create dictionary
			w = str(word_list[i]).strip('\xc2\xa0') #get rid of spaces in word string
			self.eng[w] = int(rank_list[i]) 
		return self.eng
	
	def build_jpn_freq(self):
		exclude = set(string.punctuation) #set of punctuation to clear from words 
		
		#1 to 10,000 most common
		with codecs.open(self.jpn_freq1,'r',encoding='utf-8') as f1:
			for i in range(1, 10001):
				word = clean(f1.readline(), exclude)
				rank = i
				self.jpn[word] = rank
			f1.close()

		#10,000 to 20,000 most common 
		with codecs.open(self.jpn_freq2,'r',encoding='utf-8') as f2:
			for i in range(10001, 20001):
				word = clean(f2.readline(), exclude)
				rank = i
				self.jpn[word] = rank 
			f2.close()

		return self.jpn

	def build_jpn_hira(self):

		with codecs.open(self.jpn_hira_path, 'r', encoding="utf-8") as f3:	
			for line in f3:
				match = re.search(r'([^\[\]]*)(\[)([^\[\]]*)(\])',line,re.UNICODE) #parse entry into kanji and hiragana according to format 
				
				try:
					kanji = match.group(1) 
					hiragana = match.group(3)
					for tup in process_jpn_hira(kanji, hiragana):
						self.jpn_hira[tup[0]] = tup[1]
					
				except AttributeError: 
					s = "error_prcessing %s" % line
					s = s.encode("UTF-8")
					self.error_log.write("error | %s \n" % s)
					continue

		f3.close()
		self.error_log.close()

		return self.jpn_hira



###########################
# Processing Functions
###########################
"""
Given a dictionary entry of EDICT2.txt split into kanji and hiragana portions, return a list of tuples
with each tuple representing a dictionary entry. 
"""
def process_jpn_hira(k,h):

	"""
	1. Setup
	"""
	kanji_elements = k.split(";") #kanji and hiragana elements are delimited by semicolons. 
	hiragana_elements = h.split(";")
	no_kanji = len(kanji_elements)
	no_hiragana = len(hiragana_elements)
	l = [] # final list to be returned


	"""
	2. Basic checks to deal with special formatting issues
	"""
	if no_kanji == 0 or no_hiragana == 0: #error checking
		raise AttributeError("no kanji or hiragana in line")
		return

	#clean kanji and hiragana elements of grammar tags
	clean_kanji_elements = clean_grammar_tags(kanji_elements)
	clean_hiragana_elements = clean_grammar_tags(hiragana_elements)

	#detect exceptions (see notes)
	if detect_format_exception(clean_hiragana_elements): 
		for item in clean_hiragana_elements: 
			l.extend(process_hiragana_exception(item))
		return l

	"""
	3. Process line 
	"""

	#same number of elements for both kanji and hiragana implies one to one correspondence between the elements
	if no_kanji == no_hiragana:
		for i in range(no_kanji):
			tup = (clean_kanji_elements[i].strip(), clean_hiragana_elements[i].strip())
			l.append(tup)
		return l

	#kanji elements more than hiragana elements -> link all kanji elements to first hiragana element
	#hiragana elements more than kanji elements -> same as above (link all kanji elements to first hiragana element and disregard other hiragana elements)
	else:
		for i in range(no_kanji):
			tup = (clean_kanji_elements[i].strip(), clean_hiragana_elements[0].strip())
			l.append(tup)
		return l

##############################
# Processing exception lines
################################
"""
Given a hiragana exception, process line accordingly. 

E.G. 
input: おにころし(鬼殺し,鬼ころし)
output: [(鬼殺し,おにころし ), (鬼ころし,おにころし)]
"""

def detect_format_exception(expression_list):
	for e in expression_list: 
		match = re.search(r'\(', e) #check expression for parantheses
		if match: return True
	return False

def process_hiragana_exception(entry):
	l = []
	match = re.search(r'([^\(\)]*)(\()([^\(\)]*)(\))',entry,re.UNICODE) #separate entry into kanji and hiragana
	if match:
		hiragana, kanji = match.group(1), match.group(3)
		for k in kanji.split(","): 
			l.append((k.strip(),hiragana.strip()))
	return l


###########################
#Helper functions
###########################


#Given a list of kanji/hiragana expressions, function removes grammar tags [(P, (oK), (ateji), ....)]
def clean_grammar_tags(s):
	problem_expressions = ["\(P\)","\(iK\)","\(ik\)","\(oK\)","\(ok\)","\(io\)","\(ateji\)","\(gikun\)"]
	for i in range(len(s)):
		for p in problem_expressions:
			s[i] = re.sub(p,"",s[i])
	return s

#Given a string and a set of symbols to exclude, function clears away all characters in exclusion set.
def clean(s,exclude):
	return "".join(ch for ch in s if ch not in exclude).strip()


###########################
""" Main (used for testing dictionary builds) """
###########################

def main():
	# use this to do run simple tests
	"""
	D = D_bot()
	D.build_jpn_hira()
	d3 = D.jpn_hira
	
	s = u"お会計"
	log = open("/home/andy/Documents/Projects/AI_Subs/src/package1/debug.txt","w")
	log.write(s.encode("utf-8") + "\n")
	log.write("keys start here \n")
	
	for item in d3.keys():
		log.write(item.encode("utf-8") + "\n")
		if s == item: print "YAY"
	log.close()
	"""

if __name__ == '__main__':
	main()



