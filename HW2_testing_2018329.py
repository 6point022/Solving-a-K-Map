import unittest
from HW2_2018329 import minFunc

class testpoint(unittest.TestCase):
	def test_minFunc(self):
		self.assertEqual(minFunc(4, "(1,3,7,11,15) d (0,2,5)"), "w'x'+yz OR w'z+yz")
		self.assertEqual(minFunc(4, "(4,8,10,11,12,15) d (9,14)"), "wx'+wy+xy'z' OR wy+wz'+xy'z'")
		self.assertEqual(minFunc(4, "(2,3,7,9,11,13) d (1,10,15)"), "wz+x'y+yz")
		self.assertEqual(minFunc(3, "(0,1,2,4,5,6) d -"), "x'+y'")
		self.assertEqual(minFunc(2, "(0,1,2) d (3)"), "1")
		self.assertEqual(minFunc(1, "(0) d -"), "w'")

if __name__=='__main__':
	unittest.main()
