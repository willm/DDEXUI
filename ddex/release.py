import xml.etree.cElementTree as ET
"""
todo: figure out how to do enums in python 3.3
from enum import Enum

class ReleaseIdType(Enum):
	upc = 1
	isrc = 2
"""

class ReleaseId:
	def __init__(self, type, id):
		self.type = type
		self.id = id

	def write(self):
		name = None
		attrs = {}
		if(self.type == 1):
			name = "ICPN"
			attrs = {"IsEan": "false"}
		elif(self.type == 2):
			name = "ISRC"
		element = ET.Element(name, attrs)
		element.text = self.id
		return element

class Release:
	def __init__(self, product_name, cline, pline, year, release_reference, release_id, release_type):
		self.release_type = release_type
		self.release_id = release_id
		self.genres = []
		self.pline = pline	
		self.release_reference = release_reference
		self.cline = cline
		self.year = str(year)
		self.product_name = product_name
	
	def write(self):
		release = ET.Element("Release")
		releaseId = ET.SubElement(release, "ReleaseId")
		releaseId.append(self.release_id.write())
		release_type = ET.SubElement(release, "ReleaseType")
		release_type.text = self.release_type
		referenceTitle = ET.SubElement(release, "ReferenceTitle")
		titleText = ET.SubElement(referenceTitle, "TitleText")
		titleText.text = self.product_name
		releaseRef = ET.SubElement(release, "ReleaseReference")
		releaseRef.text = self.release_reference
		releaseDetailsByTerritory = ET.SubElement(release, "ReleaseDetailsByTerritory")
		ET.SubElement(releaseDetailsByTerritory, "TerritoryCode").text = "Worldwide"
		self.__write_genres(releaseDetailsByTerritory)
		pline = ET.SubElement(releaseDetailsByTerritory, "PLine")
		ET.SubElement(pline, "Year").text = self.year
		ET.SubElement(pline, "PLineText").text = self.pline
		cline = ET.SubElement(releaseDetailsByTerritory, "CLine")
		ET.SubElement(cline, "Year").text = self.year
		ET.SubElement(cline, "CLineText").text = self.cline
		ET.SubElement(release, "ReleaseResourceReferenceList")
		return release

	def __write_genres(self, releaseDetailsByTerritory):
		for genre in self.genres:
			genreElement = ET.SubElement(releaseDetailsByTerritory, "Genre")
			ET.SubElement(genreElement, "GenreText").text = genre
