import unittest
from DDEXUI.ddex.party import Party
from DDEXUI.ddex.message_header import MessageHeader

class MessageHeaderTests(unittest.TestCase):
	def setUp(self):
		self.subject = MessageHeader(Party('12343243', 'Sony'))
	
	def test_should_serialize_as_exected(self):
		element = self.subject.write()
		self.assertEqual(element.tag, 'MessageHeader')
		self.assertNotEqual(element.find("./MessageCreatedDate"),None)
