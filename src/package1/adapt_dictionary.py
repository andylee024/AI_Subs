
"""
This module builds the following dictionaries that are useful for translation services. 
	1. english frequency list (1-5000)
	2. japanese frequency list (1-20000)
	3. japanese (kanji: hiragana) dictionary

Further Improvements:
	- convert dictionaries into database
	- do further check to ensure that all entries are processed correctly

"""
import re
import codecs #library to read input in utf-8

class D_bot:
	def __init__(self):
		#set data fields
		self.eng_freq = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/5000wordfrequencylist.csv"
		self.jpn_freq1 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/1-10000_frequency_list_japanese.csv" 
		self.jpn_freq2 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/10001-20000_frequency_list_japanese.csv"
		self.jpn_hira = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/EDICT2.txt"

		self.eng = {}
		self.jpn = {}
		self.jpn_hira = {}

		self.error_log = open("../log/error_log.txt","w")

		#initialize dictionaries
		#build_eng_freq()
		#build_jpn_freq()
		#build_jpn_hira()

	def build_eng_freq(self):
		df = pd.read_csv(self.eng_freq, header=0)
		word_list = df['Word'][1:]
		rank_list = df['Rank'][1:]
		for i in range(1, len(word_list)+1): #iterate through words to create dictionary
			w = str(word_list[i]).strip('\xc2\xa0') #get rid of spaces in word string
			self.eng[w] = int(rank_list[i]) 
		return 
	
	def build_jpn_freq(self):
		#1 to 10,000 most common
		with codecs.open(self.jpn_freq1,'r',encoding='utf8') as f1:
			for i in range(1, 10001):
				word = f1.readline().strip()
				rank = i
				self.jpn[word] = rank
			f1.close()

		#10,000 to 20,000 most common 
		with codecs.open(self.jpn_freq2,'r',encoding='utf8') as f2:
			for i in range(10001, 20001):
				word = f2.readline().strip()
				rank = i
				self.jpn[word] = rank 
			f2.close()
	
	def build_jpn_hira(self):
		
		error_log = open("../log/error_log2.txt","w")

		with codecs.open(self.jpn_hira, 'r', encoding="utf8") as f3:
			for line in f3:
				#clean problematic format syntax
				line = format_clean(line) 

				#split kanji, hiragana
				match = re.search(r'([^\[\]]*)(\[)([^\[\]]*)(\])',line,re.UNICODE) #parse entry according to format 
				
				"""this error occurs if the entry is already in hiragana, which implies that there's no kanji portion to split""" 
				try:
					kanji = match.group(1) 
					hiragana = match.group(3)
				except AttributeError: 
					s = "error_prcessing %s" % line
					s = s.encode("UTF-8")
					#error_log.write(s + "\n") #to see the entries giving this error specifically, uncomment the write operation
					continue

				#parse entry and update dictionary accordingly
				if parantheses_check(hiragana): self.h_build(hiragana)
				else: self.regular_build(kanji,hiragana)

			
		#close documents
		f3.close()
		self.error_log.close()

	"""Special build processes for kanji/hiragana dictionary"""
	def regular_build(self, k,h):
		k_list = k.split(";")
		h_list = h.split(";")
		
		#clean kanji of parantheses
		for k in k_list:
			if parantheses_check(k): k = kanji_clean(k)

		#equal entries match up
		if len(k_list) == len(h_list):
			for i in range(len(k_list)):
				self.jpn_hira[k_list[i]] = h_list[i]
			
		#unequal number of entries so just use first hiragana entry for all kanji
		else:
			for k in k_list:
				self.jpn_hira[k] = h_list[0]

	def h_build(self, h):
		h_list = h.split(";")
		
		for entry in h_list:
			
			""" try/except occurs when within particular hiragana entry, there are parts with parantheses and parts without"""
			try:
				match = re.search(r'(.*)(\()(.*)(\))', entry)
				hiragana = match.group(1)
				kanji = match.group(3)
				kanji_list = kanji.split(",")

				for k in kanji_list:
					self.jpn_hira[k] = hiragana
			
			except AttributeError:
				error = "hiragana raising attribute error"
				message = "full entry: %s  | portion raising error: %s" % (h,entry)
				self.write_log(message, error)
				continue

	def write_log(self, error, msg):
		output = (error + " | " + msg).encode("UTF-8")
		self.error_log.write(output+"\n")





###########################
"""Helper functions"""
###########################

#Takes kanji and hiragana expression and clears away annoying formatting guides [(P, (oK), (ateji), ....)]
def format_clean(s):
	problem_expressions = ["\(P\)","\(iK\)","\(ik\)","\(oK\)","\(ok\)","\(io\)","\(ateji\)","\(gikun\)"]
	for p in problem_expressions: 
		s = re.sub(p,"",s)
	return s


#takes a kanji expression and clears away any items embedded within parantheses
def kanji_clean(k): 
	match = re.search(r'(.+)(\()(.+)(\))',k)
	return match.group(1)

#checks if there is a parentheses in expression
def parantheses_check(s):
	match = re.search(r'\(', s)
	if match: return True
	return False



###########################
""" Main (used for testing dictionary builds) """
###########################

def main():
	#testing building jpn_hira
	D = D_bot()
	D.build_jpn_hira()
	

if __name__ == '__main__':
	main()





