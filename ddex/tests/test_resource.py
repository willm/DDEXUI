import unittest
import functools
import xml.etree.cElementTree as ET
from DDEXUI.ddex.file_metadata import FileMetadata
from DDEXUI.ddex.resource import SoundRecording
import os

class SoundRecordingTests(unittest.TestCase):

	def setUp(self):
		self.resource_reference = "A1"
		self.title = "Some Title"
		self.file_metadata = FileMetadata("PT0H2M28.000S", 320,"dff9465befeb68d97cd6fd103547c464","test.mp3", "MP3")
		res = SoundRecording(self.resource_reference, "abc", self.title, self.file_metadata)
		self.element = res.write()

	def test_resource_should_display_type(self):
		self.assertEqual(self.element.tag, "SoundRecording")

	def test_resource_should_display_sound_recording_type(self):
		self.assertEqual(self.element.find("./SoundRecordingType").text, "MusicalWorkSoundRecording")

	def test_resource_should_contain_isrc(self):
		self.assertEqual(self.element.find("./SoundRecordingId/ISRC").text, "abc")
		
	def test_resource_should_contain_resource_reference(self):
		self.assertEqual(self.element.find("./ResourceReference").text, self.resource_reference)
		
	def test_resource_should_contain_reference_title(self):
		self.assertEqual(self.element.find("./ReferenceTitle/TitleText").text, self.title)
		
	def	test_should_have_a_worldwide_territory(self):
		self.assertEqual(self.element.find("./SoundRecordingDetailsByTerritory/TerritoryCode").text, "Worldwide")

	def test_should_have_audio_codec(self):
		self.assertEqual(self.world_wide_territory().find("./TechnicalSoundRecordingDetails/AudioCodecType").text, "MP3")
	
	def test_should_have_file_name_and_path(self):
		file_element = self.world_wide_territory().find("./TechnicalSoundRecordingDetails/File")
		self.assertEqual(file_element.find("./FileName").text, "test.mp3")
		hash_sum = file_element.find("./HashSum")
		self.assertEqual(hash_sum.find("./HashSum").text, "dff9465befeb68d97cd6fd103547c464")
		self.assertEqual(hash_sum.find("./HashSumAlgorithmType").text, "MD5")

	def world_wide_territory(self):
		return (list(filter(lambda x: x.find("./TerritoryCode").text == "Worldwide", self.element
					.findall("./SoundRecordingDetailsByTerritory")))[0])

