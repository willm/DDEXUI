import xml.etree.cElementTree as ET
import datetime as d

class DDEX:

	def __init__(self, sender, product_release):
		self.product_release = product_release
		self.sender = sender

	def write(self):
		root =  ET.Element("ernm:NewReleaseMessage", {'MessageSchemaVersionId': 'ern/341', 'LanguageAndScriptCode': 'en', 'xs:schemaLocation': 'http://ddex.net/xml/ern/341 http://ddex.net/xml/ern/341/release-notification.xsd', 'xmlns:ernm': 'http://ddex.net/xml/ern/341', 'xmlns:xs':'http://www.w3.org/2001/XMLSchema-instance'})
		header = self.__write_message_header(root)
		releaseList = ET.SubElement(root,"ReleaseList")
		releaseList.append(self.__write_product_release())
		tree = ET.ElementTree(root)
		tree.write("file.xml")
	
	def __write_product_release(self):
		return self.product_release.write()
	
	def __write_message_header(self, root):
		message_header = ET.SubElement(root,"MessageHeader")
		message_header.append(self.sender.write())
		created_date = ET.SubElement(message_header, "MessageCreatedDate")
		created_date.text = d.datetime.now().replace(microsecond=0).isoformat()+ "Z" 
		return message_header
