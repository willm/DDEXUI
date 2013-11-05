import xml.etree.cElementTree as ET

class Deal:

	def __init__(self, commercial_model):
		self.commercial_model = commercial_model

	def write(self):
		deal = ET.Element("Deal")
		terms = self.__append_element_with_text(deal, "DealTerms")
		self.__append_element_with_text(terms, "CommercialModelType", self.commercial_model)
		return deal
		
	def __append_element_with_text(self, parent, name, text=""):
		el = ET.SubElement(parent, name)
		el.text = text
		return el
