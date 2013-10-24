import xml.etree.cElementTree as ET

class MessageHeader:
	def __init__(self, party):
		self.party = party

	def write(self):
		element = ET.Element('MessageHeader')
		return element
