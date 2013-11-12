import xml.etree.cElementTree as ET

class SoundRecording:
	def __init__(self, resource_reference, isrc, title ,file_metadata):
		self.title = title
		self.resource_reference = resource_reference
		self.isrc = isrc
		self.file_metadata = file_metadata

	def write(self):
		sound_recording = ET.Element("SoundRecording")
		self.__append_element_with_text(sound_recording, "SoundRecordingType", "MusicalWorkSoundRecording")
		sound_recording_id = self.__append_element_with_text(sound_recording, "SoundRecordingId")
		self.__append_element_with_text(sound_recording_id, "ISRC", self.isrc)
		self.__append_element_with_text(sound_recording, "ResourceReference", self.resource_reference)		
		title = self.__append_element_with_text(sound_recording, "ReferenceTitle")
		self.__append_element_with_text(title, "TitleText", self.title)

		self.__append_element_with_text(sound_recording, "Duration", self.file_metadata.duration)

		details_by_territory = ET.SubElement(sound_recording, "SoundRecordingDetailsByTerritory")
		self.__append_element_with_text(details_by_territory, "TerritoryCode", "Worldwide")
		technical_details = ET.SubElement(details_by_territory, "TechnicalSoundRecordingDetails")

		self.__append_element_with_text(technical_details, "AudioCodecType", self.file_metadata.extension)
		file_element = ET.SubElement(technical_details, "File")
		self.__append_element_with_text(file_element, "FileName", self.file_metadata.name)
		hash_sum = ET.SubElement(file_element, "HashSum")
		self.__append_element_with_text(hash_sum, "HashSum", self.file_metadata.md5)
		self.__append_element_with_text(hash_sum, "HashSumAlgorithmType", "MD5")
		return sound_recording

	def __append_element_with_text(self, parent, name, text=""):
		el = ET.SubElement(parent, name)
		el.text = text
		return el
