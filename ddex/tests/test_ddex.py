import unittest
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.release_builder import ReleaseBuilder
import DDEXUI.ddex.tests.data as data

class DDEXTests(unittest.TestCase):
	def test_should_get_the_release_id(self):
		upc = "0748435453453"
		product_release = data.valid_product_release(upc)
		ddex = DDEX(None, None, [product_release])
		
		self.assertEqual(ddex.product_release_id(), upc)
		
	def test_should_raise_exception_if_no_product_release_exists(self):
		ddex = DDEX(None, None, [])
		
		self.assertRaises(ddex.product_release_id)
