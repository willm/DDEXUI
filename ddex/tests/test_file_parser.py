import unittest
from nose.tools import *
from DDEXUI.file_parser import FileParser

def test_generator():
	cases = ([ ("ddex/tests/resources/test.mp3", "dff9465befeb68d97cd6fd103547c464", "test.mp3", "MP3"), 
				("ddex/tests/resources/test.jpg", "55e031153f2c0d8c63e6bf7c9baa58ba", "test.jpg", "JPG")])
	for path, hash, name, extension in cases:
		yield check_file, path, hash, name, extension

def check_file(path, hash, name, extension):
	file_metadata = FileParser().parse(path)
	assert_equal(file_metadata.md5, hash)
	assert_equal(file_metadata.name, name)
	assert_equal(file_metadata.extension, extension)

class FileParserTests(unittest.TestCase):

	def setUp(self):
		self.subject = FileParser()
		self.file_metadata = self.subject.parse("ddex/tests/resources/test.mp3")

	def test_should_have_duration(self):
		self.assertEqual(self.file_metadata.duration, "PT0M4.000S")

	def test_should_have_bitrate(self):
		self.assertEqual(self.file_metadata.bit_rate, 64)

	def test_should_have_codec(self):
		self.assertEqual(self.file_metadata.codec, "MP3")

class ImageFileParserTests(unittest.TestCase):
	def setUp(self):
		self.subject = FileParser()
		self.file_metadata = self.subject.parse("ddex/tests/resources/test.jpg")

	def test_should_have_height(self):
		self.assertEqual(self.file_metadata.height, 500)

	def test_should_have_width(self):
		self.assertEqual(self.file_metadata.width, 463)

	def test_should_have_codec(self):
		self.assertEqual(self.file_metadata.codec, "JPEG")
