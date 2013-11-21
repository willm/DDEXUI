import unittest
import configparser
from DDEXUI.ddex.party import *
from DDEXUI.party_repository import *
import sqlite3


class PartyRepositoryTests(unittest.TestCase):
	def setUp(self):
		connection = self.__get_connection()
		connection.execute("DROP TABLE IF EXISTS party")
		connection.execute("CREATE TABLE IF NOT EXISTS party(name text, partyId text, PartyType integer)")
		connection.close()
		self.party = Party('IDIDIDO', 'Some Label Name', PartyType.MessageSender)

	def __get_connection(self):
		return sqlite3.connect("ddexui")

	def tearDown(self):
		c = self.__get_connection()
		cu = c.cursor()
		cu.execute("DROP TABLE IF EXISTS party")
		c.close()

	def test_it_should_return_the_party(self):
		connection = self.__get_connection()
		connection.execute("INSERT INTO party(name, partyId, partyType) VALUES(?,?,?)", (self.party.name, self.party.party_id, self.party.party_type))
		connection.commit()
		connection.close()

		party = PartyRepository().get_party(PartyType.MessageSender)
		self.assertEqual(party, self.party)
		
	def test_it_should_return_none_if_there_is_no_party(self):
		self.assertEqual(PartyRepository().get_party(PartyType.MessageSender), None)
	
	def test_it_should_write_the_party(self):
		repo = PartyRepository()
		repo.write_party(self.party)
		
		self.assertEqual(repo.get_party(PartyType.MessageSender), self.party)

	def test_should_not_overwrite_other_parties_when_saving(self):
		connection = self.__get_connection()
		connection.execute("INSERT INTO party(name, partyId, partyType) VALUES(?,?,?)", (self.party.name, self.party.party_id, self.party.party_type))
		connection.commit()
		connection.close()
		repo = PartyRepository()
		party = Party("GSDFGDFGSEG", "SomeParty", PartyType.MessageRecipient)
		repo.write_party(party)
		self.assertNotEqual(repo.get_party(PartyType.MessageSender), None)	
		self.assertNotEqual(repo.get_party(PartyType.MessageRecipient), None)	
