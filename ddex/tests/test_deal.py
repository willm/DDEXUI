import unittest
import xml.etree.cElementTree as ET
from DDEXUI.ddex.deal import Deal

class DealTests(unittest.TestCase):

	def setUp(self):
		self.use_type = "PermanentDownload"
		deal = Deal("PayAsYouGoModel", self.use_type)
		self.element = deal.write()

	def test_should_have_commercial_model_type(self):
		self.assertEqual(self.element.find("./DealTerms/CommercialModelType").text, "PayAsYouGoModel")

	def test_should_have_use_type(self):
		self.assertEqual(self.element.find("./DealTerms/Usage/UseType").text, self.use_type)
