import unittest
from DDEXUI.ddex.release import ReleaseIdType, ReleaseType, Release
from DDEXUI.ddex.ddex_builder import DDEXBuilder

class DDEXBuilderTests(unittest.TestCase):
	
	def test_errors_if_a_non_resources_are_added_to_resouces(self):
		self.assertRaises(TypeError, lambda: DDEXBuilder().add_resource(""))

		
