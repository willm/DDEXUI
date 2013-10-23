import unittest
import configparser

class PartyIdRepositoryTests(unittest.TestCase):
	def setUp(self):
		self.config = configparser.RawConfigParser()
		self.config.add_section('Sender')
		self.party_id = 'LETSHAVEAPARTY'
		self.config.set('Sender', 'party_id', self.party_id)
		
	def test_it_should_return_the_party_id(self):
		self.__write_config()
		
		self.assertEqual(PartyIdRepository().get_party_id(), self.party_id)
		
	def test_it_should_return_none_if_there_is_no_party_id(self):
		self.config.remove_option('Sender', 'party_id')
		self.__write_config()
		
		self.assertEqual(PartyIdRepository().get_party_id(), None)
	
	@unittest.skip("work in progress")
	def test_it_should_write_the_party_id(self):
		self.config.remove_option('Sender', 'party_id')
		repo = PartyIdRepository()
		repo.write_party_id(self.party_id)
		
		self.assertEqual(repo.get_party_id(), self.party_id)
		

	def __write_config(self):
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
		
		
class PartyIdRepository:
	def __init__(self):
		self.config = configparser.RawConfigParser()

	def __read_config_file(self):
		self.config.read('ddexui.cfg')
		
	def __party_id_exists(self):
		self.__read_config_file();
		return self.config.has_option('Sender', 'party_id')
		
	def get_party_id(self):
		if(self.__party_id_exists()):
			return self.config.get('Sender', 'party_id')
		return None
		
	def write_party_id(self):
		pass