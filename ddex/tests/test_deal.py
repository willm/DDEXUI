import unittest
import xml.etree.cElementTree as ET
from DDEXUI.ddex.deal import Deal

class DealTests(unittest.TestCase):

	def setUp(self):
		deal = Deal("PayAsYouGoModel")
		self.element = deal.write()

	def test_should_have_commercial_model_type(self):
		self.assertEqual(self.element.find("./DealTerms/CommercialModelType").text, "PayAsYouGoModel")

