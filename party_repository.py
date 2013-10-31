import configparser
from DDEXUI.ddex.party import Party

class PartyRepository:
	def __init__(self):
		self.config = configparser.RawConfigParser()

	def __read_config_file(self):
		self.config.read('ddexui.cfg')
		
	def __party_exists(self, section):
		self.__read_config_file();
		return self.config.has_option(section, 'party_id')

	def __write_party(self, section, party):
		self.config.add_section(section)
		self.config.set(section, 'party_id', party.party_id)
		self.config.set(section, 'name', party.name)
		with open('ddexui.cfg', 'w') as configfile:
			self.config.write(configfile)
		
		
	def get_party(self):
		if(self.__party_exists('Sender')):
			return Party(self.config.get('Sender', 'party_id'), self.config.get('Sender', 'name'))
		return None

	def get_recipient_party(self):
		if(self.__party_exists('Recipient')):
			return Party(self.config.get('Recipient', 'party_id'), self.config.get('Recipient', 'name'))
		return None
		
	def write_party(self, party):
		self.__write_party('Sender', party)

	def write_recipient_party(self, party):
		self.__write_party('Recipient', party)
