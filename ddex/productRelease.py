import xml.etree.cElementTree as ET

class ProductRelease:
	def __init__(self, product_name, upc, cline, pline, year):
		self.product_genres = []
		self.pline = pline	
		self.cline = cline
		self.year = str(year)
		self.upc = upc
		self.product_name = product_name
	
	def write(self):
		release = ET.Element("Release")
		releaseId = ET.SubElement(release, "ReleaseId")
		icpn = ET.SubElement(releaseId, "ICPN", {"IsEan": "false"})
		icpn.text = self.upc
		referenceTitle = ET.SubElement(release, "ReferenceTitle")
		titleText = ET.SubElement(referenceTitle, "TitleText")
		titleText.text = self.product_name
		releaseRef = ET.SubElement(release, "ReleaseReference")
		releaseRef.text = "R0"
		releaseDetailsByTerritory = ET.SubElement(release, "ReleaseDetailsByTerritory")
		ET.SubElement(releaseDetailsByTerritory, "TerritoryCode").text = "Worldwide"
		self.__write_product_genres(releaseDetailsByTerritory)
		pline = ET.SubElement(releaseDetailsByTerritory, "PLine")
		ET.SubElement(pline, "Year").text = self.year
		ET.SubElement(pline, "PLineText").text = self.pline
		cline = ET.SubElement(releaseDetailsByTerritory, "CLine")
		ET.SubElement(cline, "Year").text = self.year
		ET.SubElement(cline, "CLineText").text = self.cline
		ET.SubElement(release, "ReleaseResourceReferenceList")
		return release

	def __write_product_genres(self, releaseDetailsByTerritory):
		for genre in self.product_genres:
			genreElement = ET.SubElement(releaseDetailsByTerritory, "Genre")
			ET.SubElement(genreElement, "GenreText").text = genre
