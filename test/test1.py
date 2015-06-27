# -*- coding: utf-8 -*-

import unittest
import sys


#sys paths
sys.path.append("/home/andy/Documents/Projects/AI_Subs/src")
from package1.adapt_dictionary import D_bot


class Test_AdaptDictionary(unittest.TestCase):
	
	def setUp(self):
		pass

	#test to ensure that english frequency dictionary is built correctly -passed
	@unittest.skip("skip jpn freq")
	def test_engfreq(self):
		#init
		D = D_bot()
		D.build_eng_freq()
		d1 = D.eng

		#test cases 
		self.assertTrue("thing" in d1)
		self.assertEqual(97, d1["thing"], "english frequency incorrect")
		self.assertEqual(4982, d1["praise"], "english frequency incorrect")
		self.assertEqual(4930, d1["sudden"], "english frequency incorrect")
		

	#test to ensure that japanese frequency dictionary is built correctly -passed
	@unittest.skip("skip jpn freq")
	def test_jpnfreq(self):
		#init
		D = D_bot()
		D.build_jpn_freq()
		d2 = D.jpn
		
		#build test cases 
		p1 = ("報復".decode("utf-8"), 7950)
		p2 = ("足りる".decode("utf-8"), 7961) 
		p3 = ("乳房".decode("utf-8"), 16547)
		
		#run tests
		self.assertEqual(d2[p1[0]],p1[1], "jpn frequency incorrect")
		self.assertEqual(d2[p2[0]],p2[1], "jpn frequency incorrect")
		self.assertEqual(d2[p3[0]],p3[1], "jpn frequency incorrect")
		
		
	#test to ensure that japanese kanji:hira dictionary is buitl correctly
	#@unittest.skip("skip jpn hira")
	def test_jpnhira(self):
		#init
		D = D_bot()
		D.build_jpn_hira()
		d3 = D.jpn_hira

		#build test cases
		p1 = ("お会計".decode("utf-8"), "おかいけい".decode("utf-8"))
		p2 = ("バフ盤".decode("utf-8"), "バフばん".decode("utf-8"))
		p3 = ("鬼乳".decode("utf-8"), "きにゅう".decode("utf-8"))

		#experiments 
		print "%s, %s" % (p1[0], p1[1])
		print "%s, %s" % (p2[0], p2[1])
		print "%s, %s" % (p3[0], p3[1])
		
		#f3 = open("/home/andy/Documents/Projects/AI_Subs/test/japanese_hiragana_log.txt",'w')
		#for item in d3.items():
		#	 f3.write("%s | %s" % (item[0].decode("utf-8"), item[1].decode("utf-8")) + "\n")
		#f3.close()

		#run tests
		#self.assertEqual(d3[p1[0], p1[1]], "jpn hira incorrect")
		#self.assertEqual(d3[p2[0], p2[1]], "jpn hira incorrect")
		#self.assertEqual(d3[p3[0], p3[1]], "jpn hira incorrect")


		
"""
Given a dictionary and a value, returns the key corresponding to the value 
"""
def getKey(d, v):
	lKey = [key for (key,value) in d.iteritems() if value == v]
	return lKey[0]

if __name__ == '__main__':
    unittest.main()