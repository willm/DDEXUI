import unittest

from DDEXUI.ddex.productRelease import ProductRelease
import xml.etree.cElementTree as ET

class Test(unittest.TestCase):
	def test_all_genres_should_be_written(self):
		release = ProductRelease()
		release.product_genres.append("Rock")
		release.product_genres.append("Pop")

		release_element = release.write()

		genre_elements = release_element.findall("./ReleaseDetailsByTerritory/Genre/GenreText")
		genres = list(map(lambda el: el.text, genre_elements))
		self.assertEqual(["Rock","Pop"], genres)

	def test_title_text_should_be_written(self):
		release = ProductRelease()
		name = "Bob"
		release.product_name = name
		
		element = release.write()

		self.assertEqual(name, element.find("./ReferenceTitle/TitleText").text)

	def test_upc_should_be_written(self):
		release = ProductRelease()
		upc = "0132384103241"
		release.upc = upc
		
		element = release.write()

		self.assertEqual(upc, element.find("./ReleaseId/ICPN").text)

	def test_release_reference_should_be_set(self):
		release = ProductRelease()
		element = release.write()
		self.assertEqual("R0",element.find("./ReleaseReference").text)
	
	def test_release_refernce_territory_code_should_be_worldwide(self):
		release = ProductRelease()

		element = release.write()

		self.assertEqual("Worldwide",element.find("./ReleaseDetailsByTerritory/TerritoryCode").text)

	def test_pline_should_be_written(self):
		release = ProductRelease()
		pline = "Published by brillient music"
		release.pline = pline 

		element = release.write()

		self.assertEqual(release.pline,element.find("./ReleaseDetailsByTerritory/PLine/PLineText").text)

	def test_cline_should_be_written(self):
		release = ProductRelease()
		cline = "Copyright brillient music"
		release.cline = cline 

		element = release.write()

		self.assertEqual(release.cline,element.find("./ReleaseDetailsByTerritory/CLine/CLineText").text)

	def test_year_should_be_written(self):
		release = ProductRelease()
		release.year = 2013

		element = release.write()

		self.assertEqual(2013, element.find("./ReleaseDetailsByTerritory/CLine/Year").text)
		self.assertEqual(2013, element.find("./ReleaseDetailsByTerritory/PLine/Year").text)


class DDEX:

	def __init__(self, product_release):
		self.product_release = product_release

	def write(self):
		root =  ET.Element("ernm:NewReleaseMessage", {'MessageSchemaVersionId': 'ern/341', 'LanguageAndScriptCode': 'en', 'xs:schemaLocation': 'http://ddex.net/xml/ern/341 http://ddex.net/xml/ern/341/release-notification.xsd', 'xmlns:ernm': 'http://ddex.net/xml/ern/341', 'xmlns:xs':'http://www.w3.org/2001/XMLSchema-instance'})
		releaseList = ET.SubElement(root,"ReleaseList")
		releaseList.append(self.__write_product_release())
		tree = ET.ElementTree(root)
		tree.write("file.xml")
	
	def __write_product_release(self):
		return product_release.write()

if __name__ == '__main__':
	unittest.main()


#product_release = ProductRelease()
#product_release.product_name = "bob"
#product_release.upc = "926194268695"
#product_release.product_genres.append("Pop")
#product_release.product_genres.append("Rock")
#ddex = DDEX(product_release)
#ddex.write()
