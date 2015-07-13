
import tinysegmenter #segmentation api for japanese
import codecs #library to read input in utf-8


"""
TODO: 
1. specify output paths for annotater class 
2. debug regular expressions for ENG_Transcript
3. Write unit tests 
"""

"""
Base Class for parsing subtitle (i.e. interface)
"""
class Transcript:

	def __init__(self, path, language, level):
		
		#input
		self.path = path
		self.language = language
		self.level = level
		

"""
Derived Classes (language specific)
"""
# Fields
# @ string path: path of subtitle file to be annotated
# @ string langauge: source 
# @ int level: level of user
# @ file output: output file that annotated transcript is written to

# Methods 
# @ Annotate() : calls process() function with corresponding parse function and output file.
# @ parse_line(): parse function for target language



class ENG_Transcript(Transcript):

	def __init__(self, path, language, level):
		Transcript.__init__(self, path, language, level) 
		self.output = open("new_transcript.txt","w") #designate path
		self.Annotater = ENG_Annotater(self.level)

	def annotate(self):
		process(self.path, self.parse_line, self.output)


	def parse_line(self, line):
		
		#regex to break line into (time | content)	 
		match = re.search(r'([:\.\,\w\s]+,,0,0,0,,)([\w\s\,\.\'()\\-]*)',line)
		
		#annotation step
		if match:
			time = match.group(1)
			message = match.group(2).split()

			#annotate each unit (word) accordingly
			for i in range(len(message)): 
				message[i] = annotate_eng(message[i],d)
				
			#create new annotated_line
			annotated_message = " ".join(message)
			return time + annotated_message 



 
class JPN_Transcript(Transcript):

	def __init__(self, path, language, level):
		Transcript.__init__(self, path, language, level)
		self.output = open("new_transcript.txt","w") 
		self.TS = tinysegmenter.TinySegmenter() #Japanese segmenter object
		self.Annotater = JPN_Annotater(self.level)

	def annotate(self):
		process(self.path, self.parse_line, self.output)

	def parse_line(self):

		#regex to break line into (time | content)	 
		match = re.search(r'([:\.\,\w\s]+,,0,0,0,,)([\w\W]*)', line, re.UNICODE)
		
		#annotation step
		if match:
			time = match.group(1)
			message = TS.tokenize( match.group(2).decode("UTF-8") )

			#annotate each unit (segmented phrase) accordingly
			for i in range(len(message)):
				message[i] = annotate_jpn(message[i],d)

			#create new annotated_line
			annotated_message = "".join(m)
			return time + annotated_message 



"""
Processing functions
"""	

# Process()
# @param String path: path of original subtitle file
# @param function parse: parse function that takes in a line of dialogue and highlights accordingly
# @param file output: output file for annotated subtitle file  
# Description: opens a file and processes it according to a parse function to render an annotated subtitle file.

def process(path, parse, output):
	
	f = open(path,"r")
	
	for line in subtitle_file:
		#case 1 = empty line   
		if line.split() == []: 
			output.write("\n")

		#case 2 = irrelevant line (no content)
		elif line.split()[0] != "Dialogue:": 
			output.write(line)

		#case 3 = relevant line with content
		else:
			annotated = parse(line, freq_list)
			annotated_utf = annotated.encode("UTF-8") #encode string in UTF to display correctly
			output.write(annotated_utf+"\n")

	f.close()
	output.close()
	
	return
