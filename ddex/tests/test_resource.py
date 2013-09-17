import unittest
import xml.etree.cElementTree as ET

class SoundRecordingTests(unittest.TestCase):
	def test_resource_should_display_type(self):
		res = SoundRecording("")
		element = res.write()
		self.assertEqual(element.tag, "SoundRecording")

	def test_resource_should_contain_isrc(self):
		res = SoundRecording("abc")
		element = res.write()
		self.assertEqual(element.find("./ISRC").text, "abc")
		
	def	test_should_have_a_worldwide_territory(self):
		res = SoundRecording("")
		element = res.write()
		self.assertEqual(element.find("./SoundRecordingDetailsByTerritory/TerritoryCode").text, "WorldWide")

class SoundRecording:
	def __init__(self, isrc):
		self.isrc = isrc

	def write(self):
		sound_recording = ET.Element("SoundRecording")
		isrc_el = ET.SubElement(sound_recording, "ISRC")
		isrc_el.text = self.isrc
		details_by_territory = ET.SubElement(sound_recording, "SoundRecordingDetailsByTerritory")
		territory_code = ET.SubElement(details_by_territory, "TerritoryCode")
		territory_code.text = "WorldWide"
		return sound_recording	
