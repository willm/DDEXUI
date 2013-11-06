import xml.etree.cElementTree as ET
import datetime as d
from uuid import uuid4 as uuid

class MessageHeader:
	def __init__(self, sender, recipient):
		self.sender = sender
		self.recipient = recipient
		

	def write(self):
		message_header = ET.Element('MessageHeader')
		self.__add_element_with_text(message_header, "MessageThreadId", str(uuid()))
		self.__add_element_with_text(message_header, "MessageId", str(uuid()))
		message_header.append(self.sender.write())
		message_header.append(self.recipient.write())
		created_date = ET.SubElement(message_header, "MessageCreatedDateTime")
		created_date.text = d.datetime.now().replace(microsecond=0).isoformat()+ "Z" 
		return message_header

	def __add_element_with_text(self, parent, name, text=""):
		element = ET.SubElement(parent, name)
		element.text = text
