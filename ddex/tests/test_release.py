import unittest
#todo figure out how to mock things
from DDEXUI.ddex.release import *
import xml.etree.cElementTree as ET

class Test(unittest.TestCase):
	def setUp(self):
		self.name = "Bob"
		self.upc = "0132384103241"
		self.cline = "Copyright brillient music"
		self.pline = "Published by brillient music"
		self.year = 2013
		self.release_reference = "R0"
		self.release_type = "Single"
		self.artist_name = "Marty McFly and the hoverboards"
		self.genres = ["Rock", "Pop"]
		self.label = "Tru Thoughts"
		self.explicit = True
		self.release = (Release(
				self.name, 
				self.cline, 
				self.pline, 
				self.year, 
				self.release_reference, 
				ReleaseId(1, self.upc), 
				self.release_type, 
				self.artist_name,
				self.label,
				self.explicit)
		)
		self.release.genres = self.genres

		self.element = self.release.write()

	def test_all_genres_should_be_written(self):
		genre_elements = self.element.findall("./ReleaseDetailsByTerritory/Genre/GenreText")
		genres = list(map(lambda el: el.text, genre_elements))
		self.assertEqual(["Rock","Pop"], genres)

	def test_title_text_should_be_written(self):
		self.assertEqual(self.name, self.element.find("./ReferenceTitle/TitleText").text)
		self.assertEqual(self.name, self.element.find("./ReleaseDetailsByTerritory/Title[@TitleType='FormalTitle']/TitleText").text)
		self.assertEqual(self.name, self.element.find("./ReleaseDetailsByTerritory/Title[@TitleType='GroupingTitle']/TitleText").text)
		self.assertEqual(self.name, self.element.find("./ReleaseDetailsByTerritory/Title[@TitleType='DisplayTitle']/TitleText").text)

	def test_upc_should_be_written(self):
		self.assertEqual(self.upc, self.element.find("./ReleaseId/ICPN").text)

	def test_release_reference_should_be_set(self):
		self.assertEqual(self.release_reference, self.element.find("./ReleaseReference").text)
	
	def test_release_refernce_territory_code_should_be_worldwide(self):
		self.assertEqual("Worldwide",self.element.find("./ReleaseDetailsByTerritory/TerritoryCode").text)

	def test_pline_should_be_written(self):
		self.assertEqual(self.pline,self.element.find("./ReleaseDetailsByTerritory/PLine/PLineText").text)

	def test_cline_should_be_written(self):
		self.assertEqual(self.cline,self.element.find("./ReleaseDetailsByTerritory/CLine/CLineText").text)

	def test_year_should_be_written(self):
		self.assertEqual(str(2013), self.element.find("./ReleaseDetailsByTerritory/CLine/Year").text)
		self.assertEqual(str(2013), self.element.find("./ReleaseDetailsByTerritory/PLine/Year").text)

	def test_release_type_should_be_written(self):
		self.assertEqual(self.release_type, self.element.find("./ReleaseType").text)
	
	def test_label_should_be_written(self):
		self.assertEqual(self.label, self.element.find("./ReleaseDetailsByTerritory/LabelName").text)

	def test_artist_name_should_be_written(self):
		self.assertEqual(self.artist_name, self.element.find("./ReleaseDetailsByTerritory/DisplayArtistName").text)
		self.assertEqual(self.artist_name, self.element.find("./ReleaseDetailsByTerritory/DisplayArtist/PartyName/FullName").text)
		
	def test_artist_role_should_be_written(self):
		self.assertEqual("MainArtist", self.element.find("./ReleaseDetailsByTerritory/DisplayArtist/ArtistRole").text)
		
	def test_parental_warning_should_be_written_as_explicit(self):
		path = "./ReleaseDetailsByTerritory/ParentalWarningType"
		self.assertEqual("Explicit", self.element.find(path).text)
		element = polite_release = Release("","","",1,"",ReleaseId(1,"000000000000"),"","","",False).write()
		self.assertEqual("NotExplicit", element.find(path).text)

