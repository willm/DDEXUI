import unittest
import configparser
from DDEXUI.ddex.party import *

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

class PartyRepository:
	def __init__(self):
		self.config = configparser.RawConfigParser()

	def __read_config_file(self):
		self.config.read('ddexui.cfg')
		
	def __party_exists(self):
		self.__read_config_file();
		return self.config.has_option('Sender', 'party_id')
		
	def get_party(self):
		if(self.__party_exists()):
			return Party(self.config.get('Sender', 'party_id'), self.config.get('Sender', 'name'))
		return None
		
	def write_party(self, party):
		self.config.add_section('Sender')
		self.config.set('Sender', 'party_id', party.party_id)
		self.config.set('Sender', 'name', party.name)
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
