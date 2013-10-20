from DDEXUI.ddex.productRelease import ReleaseId
import unittest

class ReleaseIdTests(unittest.TestCase):
	def test_it_should_serialise_upc_ids(self):
		upc = "123432222222"
		id = ReleaseId(1, upc).write()
		self.assertEqual(id.text, upc)
		#todo check the element name and attrs

	def test_it_should_serialise_upc_ids(self):
		isrc = "123432222222"
		id = ReleaseId(2, isrc).write()
		self.assertEqual(id.text, isrc)
		#todo check the element name and attrs
