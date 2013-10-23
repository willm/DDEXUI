import unittest
import configparser

class PartyIdRepositoryTests(unittest.TestCase):
	def setUp(self):
		self.config = configparser.RawConfigParser()
		self.config.add_section('Sender')

	def test_it_should_notify_if_a_party_id_exists(self):
		self.config.set('Sender', 'party_id', 'LETSHAVEAPARTY')
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
		
		self.assertTrue(PartyIdRepository().party_id_exists())
		
	def test_it_should_notify_if_no_party_id_exists(self):
		self.config.remove_option('Sender', 'party_id')
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
		
		self.assertFalse(PartyIdRepository().party_id_exists())

		
		
class PartyIdRepository:
	def party_id_exists(self):
		config = configparser.RawConfigParser()
		config.read('ddexui.cfg')
		return config.has_option('Sender', 'party_id')