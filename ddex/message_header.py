import xml.etree.cElementTree as ET
import datetime as d

class MessageHeader:
	def __init__(self, sender):
		self.sender = sender

	def write(self):
		message_header = ET.Element('MessageHeader')
		message_header.append(self.sender.write())
		created_date = ET.SubElement(message_header, "MessageCreatedDate")
		created_date.text = d.datetime.now().replace(microsecond=0).isoformat()+ "Z" 
		return message_header
