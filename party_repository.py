import configparser
from DDEXUI.ddex.party import Party

class PartyRepository:
	def __init__(self):
		self.config = configparser.RawConfigParser()

	def __read_config_file(self):
		self.config.read('ddexui.cfg')
		
	def __party_exists(self, party_type):
		self.__read_config_file();
		return self.config.has_option(party_type, 'party_id')

	def __write_party(self, party):
		self.config.add_section(party.party_type)
		self.config.set(party.party_type, 'party_id', party.party_id)
		self.config.set(party.party_type, 'name', party.name)
		with open('ddexui.cfg', 'a') as configfile:
			self.config.write(configfile)
		
		
	def get_party(self, party_type):
		if(self.__party_exists(party_type)):
			return Party(self.config.get(party_type, 'party_id'), self.config.get(party_type, 'name'), party_type)
		return None

	def write_party(self, party):
		self.__write_party(party)
