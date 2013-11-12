import xml.etree.cElementTree as ET

def enum(**enums):
	return type("Enum", (), enums)

PartyType = enum(MessageSender="MessageSender", MessageRecipient="MessageRecipient")

class Party:
	def __init__(self, party_id, name, party_type=PartyType.MessageSender):
		self.party_id = party_id
		self.name = name
		self.party_type = party_type

	def write(self):
		party = ET.Element(self.party_type)
		party_id = ET.SubElement(party,'PartyId')
		party_id.text = self.party_id
		name = ET.SubElement(party, 'PartyName')
		full_name = ET.SubElement(name, 'FullName')
		full_name .text = self.name
		return party

	def __eq__(self, other):
		if(isinstance(other, Party)):
			return self.name == other.name and self.party_id == other.party_id
		return NotImplemented

	def __ne__(self, other):
		result = self.__eq__(other)
		if(result is NotImplemented):
			return result
		return not result


