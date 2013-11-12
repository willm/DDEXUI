import unittest
from DDEXUI.ddex.file_metadata import FileParser

class FileParserTests(unittest.TestCase):

	def setUp(self):
		self.subject = FileParser()
		#self.duration = self.subject.get_duration("./ddex/tests/resources/test.mp3")
		self.file_metadata = self.subject.parse("ddex/tests/resources/test.mp3")

	def test_should_have_duration(self):
		self.assertEqual(self.file_metadata.duration, "PT0M4.000S")

	def test_should_have_bitrate(self):
		self.assertEqual(self.file_metadata.bit_rate, 64)

	def test_should_have_codec(self):
		self.assertEqual(self.file_metadata.codec, "MP3")

	def test_should_have_hash(self):
		self.assertEqual(self.file_metadata.md5, "dff9465befeb68d97cd6fd103547c464")

	def test_should_have_name(self):
		self.assertEqual(self.file_metadata.name, "test.mp3")

	def test_should_have_extension(self):
		self.assertEqual(self.file_metadata.extension, "MP3")
