import unittest
import adapt_dictionary as AD

class Test_AdaptDictionary(unittest.TestCase):
	
	def setUp(self):
		D = AD()


	#test to ensure that english frequency dictionary is built correctly
	def test_engfreq(self):
		#init
		D.build_eng_freq()
		d1 = D.eng_freq

		#test cases 
		self.assertEqual("thing", d1[97], "english frequency incorrect")
		self.assertEqual("praise", d1[4982], "english frequency incorrect")
		self.assertEqual("sudden", d1[4930], "english frequency incorrect")
		

	#test to ensure that japanese frequency dictionary is built correctly
	def test_jpnfreq(self):
		#init
		D.build_jpn_freq()
		d2 = D.jpn_freq

		#test cases
		self.assertEqual()

	#test to ensure that japanese kanji:hira dictionary is buitl correctly
	def test_jpnhira(self):
		#init
		D.build_jpn_hira()
		d3 = D.jpn_hira

		#test cases
		self.assertEqual()

if __name__ == '__main__':
    unittest.main()