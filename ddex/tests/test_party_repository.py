import unittest
import configparser
from DDEXUI.ddex.party import *
from DDEXUI.party_repository import *

class PartyRepositoryTests(unittest.TestCase):
	def setUp(self):
		self.config = configparser.RawConfigParser()
		self.config.add_section('MessageSender')
		self.party = Party('LETSHAVEAPARTY', 'Some Label Name')
		self.config.set('MessageSender', 'party_id', self.party.party_id)
		self.config.set('MessageSender', 'name', self.party.name)
		
	def test_it_should_return_the_party(self):
		self.__write_config()
		
		self.assertEqual(PartyRepository().get_party(PartyType.MessageSender), self.party)
		
	def test_it_should_return_none_if_there_is_no_party(self):
		self.config.remove_option('MessageSender', 'party_id')
		self.__write_config()
		
		self.assertEqual(PartyRepository().get_party(PartyType.MessageSender), None)
	
	def test_it_should_write_the_party(self):
		self.config.remove_option('MessageSender', 'party_id')
		self.config.remove_option('MessageSender', 'name')
		self.__write_config()
		repo = PartyRepository()
		repo.write_party(self.party)
		
		self.assertEqual(repo.get_party(PartyType.MessageSender), self.party)

	def test_it_should_save_the_message_recipient(self):
		if(self.config.has_option('MessageRecipient', 'party_id')):
			self.config.remove_option('MessageRecipient', 'party_id')

		if(self.config.has_option('MessageRecipient', 'name')):
			self.config.remove_option('MessageRecipient', 'name')
		self.__write_config()
		repo = PartyRepository()
		party = Party('IWantYourStuff', 'iTunes', PartyType.MessageRecipient)
		repo.write_party(party)
		
		self.assertEqual(repo.get_party(PartyType.MessageRecipient), party)

	def __write_config(self):
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
