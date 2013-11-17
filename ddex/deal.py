import xml.etree.cElementTree as ET
import datetime as date

CommercialModals = ["PayAsYouGoModel", "SubscriptionModel"]
UseTypes = ["PermanentDownload", "OnDemandStream"]
Territories = ["UK", "FR", "DE", "US"]

class Deal:

	def __init__(self, commercial_model, use_type, territory, start_date, preorder_date=None, preorder_preview_date=None):
		self.start_date = start_date
		self.preorder_date = preorder_date
		self.preorder_preview_date = preorder_preview_date
		self.territory = territory
		self.commercial_model = commercial_model
		self.use_type = use_type

	def write(self):
		deal = ET.Element("Deal")
		terms = self.__append_element_with_text(deal, "DealTerms")
		self.__append_element_with_text(terms, "CommercialModelType", self.commercial_model)
		usage = self.__append_element_with_text(terms, "Usage")
		self.__append_element_with_text(usage, "UseType", self.use_type)
		self.__append_element_with_text(terms, "TerritoryCode", self.territory)
		if(self.preorder_date != None):
			self.__append_element_with_text(terms, "PreorderReleaseDate", self.preorder_date.isoformat())
		if(self.preorder_preview_date != None):
			self.__append_element_with_text(terms, "PreorderPreviewDate", self.preorder_preview_date.isoformat())
		validity_period = self.__append_element_with_text(terms, "ValidityPeriod")
		self.__append_element_with_text(validity_period, "StartDate", self.start_date.isoformat())
		return deal
		
	def __append_element_with_text(self, parent, name, text=""):
		el = ET.SubElement(parent, name)
		el.text = text
		return el
