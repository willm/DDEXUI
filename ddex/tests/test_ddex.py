import unittest
from ddex.ddex_builder import DDEXBuilder
from ddex.release_builder import ReleaseBuilder
import ddex.tests.data as data

class DDEXBuilderTests(unittest.TestCase):
    def test_should_get_the_release_id(self):
        upc = "0748435453453"
        product_release = data.valid_product_release(upc)
        ddex_builder = DDEXBuilder().add_release(product_release)
        
        self.assertEqual(ddex_builder.get_upc(), upc)
        
    def test_should_raise_exception_if_no_product_release_exists(self):
        self.assertRaises(DDEXBuilder().get_upc)
