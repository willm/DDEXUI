import unittest
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.tests.data import valid_product_release, valid_track_release

class DDEXBuilderTests(unittest.TestCase):

    def test_the_product_release_should_be_added_to_the_start(self):
        upc = "0344444435356"
        isrc = "GB3454532345"
        ddex = DDEXBuilder().add_release(valid_track_release(isrc)).add_product_release(valid_product_release(upc)).build()
        self.assertEqual(ddex.releases[0].release_id.id, upc)
