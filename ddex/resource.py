import xml.etree.cElementTree as ET
import os

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
