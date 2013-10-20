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
	def __init__(self, product_name, cline, pline, year, release_reference, release_id, release_type, artist, label):
		self.release_type = release_type
		self.release_id = release_id
		self.genres = []
		self.pline = pline	
		self.release_reference = release_reference
		self.cline = cline
		self.year = str(year)
		self.product_name = product_name
		self.artist = artist
		self.label = label
	
	def write(self):
		release = ET.Element("Release")
		self.__add_element(release, "ReleaseType", self.release_type)
		releaseId = ET.SubElement(release, "ReleaseId")
		releaseId.append(self.release_id.write())
		referenceTitle = ET.SubElement(release, "ReferenceTitle")
		self.__add_element(referenceTitle, "TitleText", self.product_name)
		self.__add_element(release, "ReleaseReference", self.release_reference)
		releaseDetailsByTerritory = ET.SubElement(release, "ReleaseDetailsByTerritory")
		ET.SubElement(releaseDetailsByTerritory, "TerritoryCode").text = "Worldwide"
		self.__write_genres(releaseDetailsByTerritory)
		pline = ET.SubElement(releaseDetailsByTerritory, "PLine")
		self.__add_element(pline, "Year", self.year)
		self.__add_element(pline, "PLineText", self.pline)
		cline = ET.SubElement(releaseDetailsByTerritory, "CLine")
		self.__add_element(cline, "Year", self.year)
		self.__add_element(cline, "CLineText", self.cline)
		self.__add_element(releaseDetailsByTerritory, "DisplayArtistName", self.artist)
		self.__add_element(releaseDetailsByTerritory, "LabelName", self.label)
		ET.SubElement(release, "ReleaseResourceReferenceList")
		return release

	def __add_element(self, parent, name, text):
		element = ET.SubElement(parent, name)
		element.text = text

	def __write_genres(self, releaseDetailsByTerritory):
		for genre in self.genres:
			genreElement = ET.SubElement(releaseDetailsByTerritory, "Genre")
			ET.SubElement(genreElement, "GenreText").text = genre
