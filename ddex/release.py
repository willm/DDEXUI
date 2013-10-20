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
	def __init__(self, title, cline, pline, year, release_reference, release_id, release_type, artist, label):
		self.release_type = release_type
		self.release_id = release_id
		self.genres = []
		self.pline = pline	
		self.release_reference = release_reference
		self.cline = cline
		self.year = str(year)
		self.title = title
		self.artist = artist
		self.label = label
	
	def write(self):
		release = ET.Element("Release")
		self.__add_element(release, "ReleaseType", self.release_type)
		releaseId = ET.SubElement(release, "ReleaseId")
		releaseId.append(self.release_id.write())
		self.__add_element(release, "ReleaseReference", self.release_reference)
		release_details_by_territory = ET.SubElement(release, "ReleaseDetailsByTerritory")
		self.__write_titles(release, release_details_by_territory)
		ET.SubElement(release_details_by_territory, "TerritoryCode").text = "Worldwide"
		self.__write_genres(release_details_by_territory)
		pline = ET.SubElement(release_details_by_territory, "PLine")
		self.__add_element(pline, "Year", self.year)
		self.__add_element(pline, "PLineText", self.pline)
		cline = ET.SubElement(release_details_by_territory, "CLine")
		self.__add_element(cline, "Year", self.year)
		self.__add_element(cline, "CLineText", self.cline)
		self.__write_artist(release_details_by_territory)
		self.__add_element(release_details_by_territory, "LabelName", self.label)
		ET.SubElement(release, "ReleaseResourceReferenceList")
		return release

	def __add_element(self, parent, name, text):
		element = ET.SubElement(parent, name)
		element.text = text

	def __write_artist(self, release_details_by_territory):
		self.__add_element(release_details_by_territory, "DisplayArtistName", self.artist)
		artist = ET.SubElement(release_details_by_territory, "DisplayArtist")
		party_name = ET.SubElement(artist, "PartyName")
		self.__add_element(party_name, "FullName", self.artist)
		self.__add_element(artist, "ArtistRole", "MainArtist")

	def __write_genres(self, release_details_by_territory):
		for genre in self.genres:
			genreElement = ET.SubElement(release_details_by_territory, "Genre")
			ET.SubElement(genreElement, "GenreText").text = genre
	
	def __write_titles(self, release, release_details_by_territory):
		referenceTitle = ET.SubElement(release, "ReferenceTitle")
		self.__add_element(referenceTitle, "TitleText", self.title)
		for type in ["FormalTitle", "DisplayTitle", "GroupingTitle"]:
			self.__add_title(release_details_by_territory, type)
	
	def __add_title(self, release_details_by_territory, type):
		title = ET.SubElement(release_details_by_territory, "Title", {"TitleType": type})
		self.__add_element(title, "TitleText", self.title)
		
