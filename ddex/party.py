import xml.etree.cElementTree as ET
from DDEXUI.ddex.enum import enum

PartyType = enum(MessageSender=1, MessageRecipient=2)

class Party:
    def __init__(self, party_id, name, party_type=PartyType.MessageSender):
        self.party_id = party_id
        self.name = name
        self.party_type = party_type

    def write(self):
        party = ET.Element(PartyType.reverse_mapping[self.party_type])
        party_id = ET.SubElement(party,'PartyId')
        party_id.text = self.party_id
        name = ET.SubElement(party, 'PartyName')
        full_name = ET.SubElement(name, 'FullName')
        full_name .text = self.name
        return party

    def __eq__(self, other):
        if(isinstance(other, Party)):
            return self.name == other.name and self.party_id == other.party_id and self.party_type == other.party_type
        return NotImplemented

    def __str__(self):
        return str.join(":",[self.party_id,self.name,PartyType.reverse_mapping[self.party_type]])

    def __ne__(self, other):
        result = self.__eq__(other)
        if(result is NotImplemented):
            return result
        return not result


