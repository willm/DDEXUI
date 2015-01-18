import unittest
from ddex.party import *

class PartyTests(unittest.TestCase):
    def setUp(self):
        self.party = Party('gdfg42jkdz', 'Sony')

    def test_should_serialise_correctly(self):
        print(self.party)
        party_element = self.party.write()
        self.assertEqual(party_element.find('./PartyId').text, 'gdfg42jkdz')
        self.assertEqual(party_element.find('./PartyName/FullName').text, 'Sony')
        
        
