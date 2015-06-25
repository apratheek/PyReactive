import unittest
from pyreactive import *

class Observe(Observe):
	def notify(self):
		print("Updated")

class PyReactiveTests(unittest.TestCase):
	"""Tests for all PyReactive objects"""
	def test_basic_list_len(self):
		a = List([1, 2, 3])
		b = Observe(a, method='len')
		self.assertEqual(b.value, 3)
		a.append(4)
		self.assertEqual(b.value, 4)
	
	def test_basic_list_count(self):
		a = List([1, 2, 3])
		b = Observe(a, method='count', methodParameter=2)
		self.assertEqual(b.value, 1)
		a.pop()
		self.assertEqual(b.value, 1)
		a.extend(List([2, 5]))
		self.assertEqual(b.value, 2)
		a.remove(2)
		self.assertEqual(b.value, 1)
	
	def test_basic_list_reverse(self):
		a = List([1, 2, 3])
		b = Observe(a, method='reverse')
		c = Observe(b, method='firstel')
		self.assertEqual(b.value, List([3, 2, 1]))
		self.assertEqual(c.value, 3)
		a.append(4)
		self.assertEqual(b.value, List([4,3,2,1]))
		self.assertEqual(c.value, 4)
		a.insert(2, 2.5)
		self.assertEqual(b.value, List([4, 3, 2.5, 2, 1]))
		c.modifyMethod(method='slice', methodParameter=slice(2, 3))
		self.assertEqual(c.value, 2.5)
	
	def test_basic_list_sort(self):
		a = List([8, 45, 21])
		b = Observe(a, method='sort')
		self.assertEqual(b.value, List([8, 21, 45]))

if __name__ == '__main__':
	unittest.main()
	
	
	#'len', 'count', 'reverse', 'sort', 'lastel', 'firstel', 'slice', 'set', 'sum'