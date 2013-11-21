import unittest
from DDEXUI.ddex.party import *
from DDEXUI.ddex.message_header import MessageHeader

class MessageHeaderTests(unittest.TestCase):
	def setUp(self):
		self.subject = MessageHeader(Party('12343243', 'Sony'), Party('7777777', '7digital', PartyType.MessageRecipient))
	
	def test_should_serialize_as_exected(self):
		element = self.subject.write()
		self.assertEqual(element.tag, 'MessageHeader')
		self.assertNotEqual(element.find("./MessageThreadId").text, None)
		self.assertNotEqual(element.find("./MessageId").text, None)
		self.assertNotEqual(element.find("./MessageCreatedDateTime"),None)
		self.assertNotEqual(element.find("./MessageSender"),None)
		self.assertNotEqual(element.find("./MessageRecipient"),None)
