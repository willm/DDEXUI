import xml.etree.cElementTree as ET
import hashlib
import os

class SoundRecording:
	def __init__(self, isrc, file_path):
		self.isrc = isrc
		self.file_path = file_path

	def write(self):
		sound_recording = ET.Element("SoundRecording")
		self.__append_element_with_text(sound_recording, "ISRC", self.isrc)

		details_by_territory = ET.SubElement(sound_recording, "SoundRecordingDetailsByTerritory")
		self.__append_element_with_text(details_by_territory, "TerritoryCode", "WorldWide")
		technical_details = ET.SubElement(details_by_territory, "TechnicalSoundRecordingDetails")

		self.__append_element_with_text(technical_details, "AudioCodecType", self.__get_extension())
		file_element = ET.SubElement(technical_details, "File")
		self.__append_element_with_text(file_element, "FileName", os.path.split(self.file_path)[1])
		hash_sum = ET.SubElement(file_element, "HashSum")
		self.__append_element_with_text(hash_sum, "HashSum", self.__get_hash())
		self.__append_element_with_text(hash_sum, "HashSumAlgorithmType", "MD5")
		return sound_recording	

	def __append_element_with_text(self, parent, name, text=""):
		el = ET.SubElement(parent, name)
		el.text = text

	def __get_extension(self):
		return os.path.splitext(self.file_path)[1].replace(".","").upper()

	def __get_hash(self):
		hash = hashlib.md5()
		with open(self.file_path, 'rb') as resource:
			hash.update(resource.read())
		return hash.hexdigest()
