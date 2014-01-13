import unittest
import xml.etree.cElementTree as ET
from DDEXUI.ddex.deal import Deal
from datetime import date

class DealTests(unittest.TestCase):

    def setUp(self):
        self.use_type = "PermanentDownload"
        self.territory = "BE"
        self.start_date = date(1987,2,20)
        self.preorder_date = date(1987,2,19)
        self.preorder_preview_date = date(1987,2,18)
        deal = Deal("PayAsYouGoModel", self.use_type, self.territory, self.start_date, self.preorder_date, self.preorder_preview_date)
        self.element = deal.write()

    def test_should_have_commercial_model_type(self):
        self.assertEqual(self.element.find("./DealTerms/CommercialModelType").text, "PayAsYouGoModel")

    def test_should_have_use_type(self):
        self.assertEqual(self.element.find("./DealTerms/Usage/UseType").text, self.use_type)

    def test_should_have_territory_code(self):
        self.assertEqual(self.element.find("./DealTerms/TerritoryCode").text, self.territory)

    def test_should_have_start_date(self):
        self.assertEqual(self.element.find("./DealTerms/ValidityPeriod/StartDate").text, "1987-02-20") 

    def test_should_have_preorder_date(self):
        self.assertEqual(self.element.find("./DealTerms/PreorderReleaseDate").text, "1987-02-19") 

    def test_should_have_preorder_preview_date(self):
        self.assertEqual(self.element.find("./DealTerms/PreorderPreviewDate").text, "1987-02-18") 
