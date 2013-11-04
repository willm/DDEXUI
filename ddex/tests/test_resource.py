import unittest
import functools
import xml.etree.cElementTree as ET
import os

class SoundRecordingTests(unittest.TestCase):

	def setUp(self):
		res = SoundRecording("abc","ddex/tests/resources/test.mp3")
#		help(os.path)
		self.element = res.write()

	def test_resource_should_display_type(self):
		self.assertEqual(self.element.tag, "SoundRecording")

	def test_resource_should_contain_isrc(self):
		self.assertEqual(self.element.find("./ISRC").text, "abc")
		
	def	test_should_have_a_worldwide_territory(self):
		self.assertEqual(self.element.find("./SoundRecordingDetailsByTerritory/TerritoryCode").text, "WorldWide")

	def test_should_have_audio_codec(self):
		self.assertEqual(self.world_wide_territory().find("./TechnicalSoundRecordingDetails/AudioCodecType").text, "MP3")
	
	def test_should_have_file_name_and_path(self):
		file_element = self.world_wide_territory().find("./TechnicalSoundRecordingDetails/File")
		self.assertEqual(file_element.find("./FileName").text, "test.mp3")

	def world_wide_territory(self):
		return (list(filter(lambda x: x.find("./TerritoryCode").text == "WorldWide", self.element
					.findall("./SoundRecordingDetailsByTerritory")))[0])

class SoundRecording:
	def __init__(self, isrc, file_path):
		self.isrc = isrc
		self.file_path = file_path

	def write(self):
		sound_recording = ET.Element("SoundRecording")
		isrc_el = ET.SubElement(sound_recording, "ISRC")
		isrc_el.text = self.isrc
		details_by_territory = ET.SubElement(sound_recording, "SoundRecordingDetailsByTerritory")
		territory_code = ET.SubElement(details_by_territory, "TerritoryCode")
		territory_code.text = "WorldWide"
		technical_details = ET.SubElement(details_by_territory, "TechnicalSoundRecordingDetails")
		codec_type = ET.SubElement(technical_details, "AudioCodecType")
		codec_type.text = self.__get_extension()
		file_element = ET.SubElement(technical_details, "File")
		file_name = ET.SubElement(file_element, "FileName")
		file_name.text = os.path.split(self.file_path)[1]
		return sound_recording	

	def __get_extension(self):
		return os.path.splitext(self.file_path)[1].replace(".","").upper()
