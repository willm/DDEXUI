import xml.etree.cElementTree as ET
from DDEXUI.ddex.message_header import MessageHeader

class DDEX:

	def __init__(self, sender, recipient, product_release, resources=[], update=False):
		self.update =update
		self.product_release = product_release
		self.resources = resources
		self.sender = sender
		self.recipient = recipient

	def write(self):
		root =  ET.Element("ernm:NewReleaseMessage", {'MessageSchemaVersionId': 'ern/341', 'LanguageAndScriptCode': 'en', 'xs:schemaLocation': 'http://ddex.net/xml/ern/341 http://ddex.net/xml/ern/341/release-notification.xsd', 'xmlns:ernm': 'http://ddex.net/xml/ern/341', 'xmlns:xs':'http://www.w3.org/2001/XMLSchema-instance'})
		header = self.__write_message_header(root)
		root.append(header)
		
		update_indicator = ET.SubElement(root, "UpdateIndicator")
		if(self.update):
			update_indicator.text = "UpdateMessage"
		else:
			update_indicator.text = "OriginalMessage"

		resource_list = ET.SubElement(root,"ResourceList")
		for resource in self.resources:
			resource_list.append(resource.write())

		release_list = ET.SubElement(root,"ReleaseList")
		release_list.append(self.__write_product_release())

		deal_list = ET.SubElement(root,"DealList")
		deal_list.append(self.product_release.write_deals())
		
		tree = ET.ElementTree(root)
		tree.write("/tmp/file.xml")
	
	def __write_product_release(self):
		return self.product_release.write()
	
	def __write_message_header(self, root):
		return MessageHeader(self.sender, self.recipient).write();
