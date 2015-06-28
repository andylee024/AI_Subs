"""
Given a text document, this module determines the character encoding. 
See http://chardet.readthedocs.org/en/latest/usage.html
"""
from chardet.universaldetector import UniversalDetector

def main():

	#####################################
	# input: Given path of text file to detect
	######################################
	path1 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/1-10000_frequency_list_japanese.csv"
	path2 = "/home/andy/Documents/Projects/AI_Subs/files/dictionary_files/EDICT2.txt"
	path3 = "/home/andy/Documents/Projects/AI_Subs/src/package1/hira_debug.txt"


	#intialize document and determine encoding
	f = open(path3,"r")
	detector = UniversalDetector()
	
	for line in f.readlines():
		detector.feed(line)
		if detector.done: break

	detector.close()
	f.close()

	print detector.result


if __name__ == '__main__':
	main()






