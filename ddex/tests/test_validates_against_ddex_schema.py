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
#	@unittest.skip("work in progress")
	def test_created_ddex_files_validate_against_ddex_xsd(self):
		#helpped by http://alex-sansom.info/content/validating-xml-against-xml-schema-python

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

		resource_reference = "A1"
		resource = SoundRecording(resource_reference, "abc", "Bad", FileParser().parse("ddex/tests/resources/test.mp3"),"T1")
		image_resource_reference = "A2"
		image_resource = Image(image_resource_reference, "abc", FileParser().parse("ddex/tests/resources/test.jpg"),"T2")
		resources = [resource, image_resource]
		release.add_resource_reference(resource_reference)
		release.add_resource_reference(image_resource_reference, "SecondaryResource")

		DDEX(Party('derwwfefw', 'Sony'), Party("34545345", "7digital", PartyType.MessageRecipient),release, resources).write()
		
		tree = ET.parse('/tmp/file.xml')
#		tree = ET.parse('/home/will/Documents/python/DDEXUI/ddex/tests/resources/ddex-sample.xml')
		schema = ET.XMLSchema(file="http://ddex.net/xml/ern/341/release-notification.xsd")
		schema.assertValid(tree)
