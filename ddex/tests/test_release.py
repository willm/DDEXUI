import unittest
#todo figure out how to mock things
from ddex.release import *
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
        self.assertEqual(self.pline,self.element.find("./PLine/PLineText").text)

    def test_cline_should_be_written(self):
        self.assertEqual(self.cline,self.element.find("./CLine/CLineText").text)

    def test_year_should_be_written(self):
        self.assertEqual(str(2013), self.element.find("./CLine/Year").text)
        self.assertEqual(str(2013), self.element.find("./PLine/Year").text)

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

    def test_should_write_deals(self):
        self.release.add_deal(MockDeal())
        self.release.add_deal(MockDeal())
        release_deal = self.release.write_deals()
        self.assertEqual(release_deal.find("./DealReleaseReference").text, self.release_reference)
        self.assertEqual(len(release_deal.findall("./Deal")), 2)

    def test_should_write_resource_references(self):
        ref = "A0"
        self.release.add_resource_reference(ref)
        element = self.release.write()
        resource_refs = element.findall("./ReleaseResourceReferenceList/ReleaseResourceReference")

        self.assertEqual(len(resource_refs), 1)
        self.assertEqual(resource_refs[0].text, ref)
        resource_group_content_items = element.findall("./ReleaseDetailsByTerritory/ResourceGroup/ResourceGroupContentItem")
        self.assertEqual(len(resource_group_content_items), 1)
        content_item = resource_group_content_items[0]
        self.assertEqual(content_item.find("./SequenceNumber").text, "1")
        self.assertEqual(content_item.find("./ResourceType").text, "SoundRecording")
        self.assertEqual(content_item.find("./ReleaseResourceReference").text, ref)
        
class MockDeal:
    def write(self):
        return ET.Element("Deal")
