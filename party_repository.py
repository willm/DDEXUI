import configparser
from DDEXUI.ddex.party import Party

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
