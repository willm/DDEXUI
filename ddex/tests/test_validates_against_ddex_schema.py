import lxml.etree as ET
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.release import Release, ReleaseId
from DDEXUI.ddex.party import Party, PartyType
from DDEXUI.ddex.deal import Deal
from DDEXUI.ddex.resource import SoundRecording, Image
from DDEXUI.ddex.message_header import MessageHeader
from DDEXUI.ddex.file_metadata import FileParser
from datetime import date
import unittest

class DDEXSchemaValidation(unittest.TestCase):
	def test_created_ddex_files_validate_against_ddex_xsd(self):
		#helped by http://alex-sansom.info/content/validating-xml-against-xml-schema-python
		output_file = "/tmp/file.xml"

		release = self.create_product_release()

		sound_recording = self.create_sound_recording()

		image_resource = self.create_image()
		resources = [sound_recording, image_resource]
		release.add_resource_reference(sound_recording.resource_reference())
		release.add_resource_reference(image_resource.resource_reference(), "SecondaryResource")
		releases = [release]

		DDEX(Party('derwwfefw', 'Sony'), Party("34545345", "7digital", PartyType.MessageRecipient),releases, resources).write(output_file)
		
		tree = ET.parse(output_file)
		schema = ET.XMLSchema(file="http://ddex.net/xml/ern/341/release-notification.xsd")
		schema.assertValid(tree)

	def create_product_release(self):
		release = (Release(
			"Bad",
			"copyright MJ",
			"Published by MJ",
			1987,
			"R0",
			ReleaseId(1,"1234567898764"),
			"Album",
			"Michael Jackson",
			"Epic",
			True))

		deal = Deal("PayAsYouGoModel", "PermanentDownload", "FR", date(2012,1,3))

		release.add_deal(deal)
		return release

	def create_sound_recording(self):
		resource_reference = "A1"
		resource = SoundRecording(resource_reference, "abc", "Bad", FileParser().parse("ddex/tests/resources/test.mp3"),"T1")
		return resource
	
	def create_image(self):
		image_resource_reference = "A2"
		image_resource = Image(image_resource_reference, "abc", FileParser().parse("ddex/tests/resources/test.jpg"),"T2")
		return image_resource
