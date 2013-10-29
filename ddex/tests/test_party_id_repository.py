import unittest
import configparser
from DDEXUI.ddex.party import *
from DDEXUI.party_repository import *

class PartyRepositoryTests(unittest.TestCase):
	def setUp(self):
		self.config = configparser.RawConfigParser()
		self.config.add_section('Sender')
		self.party = Party('LETSHAVEAPARTY', 'Some Label Name')
		self.config.set('Sender', 'party_id', self.party.party_id)
		self.config.set('Sender', 'name', self.party.name)
		
	def test_it_should_return_the_party(self):
		self.__write_config()
		
		self.assertEqual(PartyRepository().get_party(), self.party)
		
	def test_it_should_return_none_if_there_is_no_party(self):
		self.config.remove_option('Sender', 'party_id')
		self.__write_config()
		
		self.assertEqual(PartyRepository().get_party(), None)
	
	def test_it_should_write_the_party(self):
		self.config.remove_option('Sender', 'party_id')
		self.config.remove_option('Sender', 'name')
		self.__write_config()
		repo = PartyRepository()
		repo.write_party(self.party)
		
		self.assertEqual(repo.get_party(), self.party)
		

	def __write_config(self):
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
