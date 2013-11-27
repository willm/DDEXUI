from DDEXUI.ddex.release import *

class ReleaseBuilder:
	def __init__(self):
		self._deals = []
		self._resources = []

	def title(self, title):
		self._title = title
		return self

	def c_line(self, cline):
		self._cline = cline
		return self 

	def p_line(self, pline):
		self._pline = pline
		return self 

	def year(self, year):
		self._year = year
		return self 
	
	def reference(self, reference):
		self._reference = reference
		return self
	
	def release_id(self, id_type, id_value):
		self._release_id = ReleaseId(id_type, id_value)
		return self

	def release_type(self, release_type):
		self._release_type = release_type
		return self

	def artist(self, artist):
		self._artist = artist
		return self

	def label(self, label):
		self._label = label
		return self

	def parental_warning(self, warning):
		self._warning = warning
		return self

	def add_deal(self, deal):
		self._deals.append(deal)
		return self

	def add_resource(self, resource_reference):
		self._resources.append(resource_reference)
		return self

	def build(self):
		release = (Release(self._title, 
			self._cline, 
			self._pline, 
			self._year, 
			self._reference, 
			self._release_id, 
			self._release_type,
			self._artist, 
			self._label,
			self._warning))

		for reference in self._resources:
			release.add_resource_reference(reference)
		for deal in self._deals:
			release.add_deal(deal)
		return release
