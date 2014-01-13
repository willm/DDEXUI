import unittest
import datetime
from DDEXUI.ddex.ddex import generate_batch_id

class TestIdGenerators(unittest.TestCase):
    def test_batch_id_should_be_in_expected_format(self):
        now = datetime.datetime(2013,12,31,23,59,30,123000)
        batch_id = generate_batch_id(lambda: now)
        self.assertEqual("20131231235930123", batch_id)

