import tkinter.ttk as tk
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.validate import Validate
from DDEXUI.inputs import *
from DDEXUI.ddex.release import *
from DDEXUI.deal_window import DealWindow

class ReleaseWindow(tk.tkinter.Toplevel):
	def __init__(self, frame):
		tk.tkinter.Toplevel.__init__(self, frame)
		self.fields = ([
			EntryInput(self, "Title", Validate().not_empty), 
			EntryInput(self, "Year", Validate().year), 
			EntryInput(self, "C Line", Validate().not_empty),
			EntryInput(self, "P Line", Validate().not_empty),
			EntryInput(self, "Artist", Validate().not_empty),
			EntryInput(self, "Label", Validate().not_empty),
			OptionInput(self, "Type", 'Single', 'Album'),
			CheckboxInput(self, "Explicit")
		])

	def draw_fields(self):
		for i in range(len(self.fields)):
			self.fields[i].draw(i)

	def create_deal(self):
		deal_window = DealWindow(self)
		deal_window.wait_window()
		deal = deal_window.create_deal()
		self._release_builder.add_deal(deal)

class ProductReleaseWindow(ReleaseWindow):
	def __init__(self, frame):	
		ReleaseWindow.__init__(self, frame)
		self._release_builder = ReleaseBuilder()
		self.fields.append(EntryInput(self, "UPC", Validate().upc))
		total_fields = len(self.fields)
		self.draw_fields()
		self.add_deal_button = tk.Button(self, text="Add deal", command=self.create_deal).grid(row=total_fields+1, column=0)
		self.button = tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=total_fields+2, column=0)

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()
		
	def __destroy_if_valid(self):
		if(self.all_release_fields_valid()):
			self.destroy()

	def create_release(self):
		return (self._release_builder.title(self.value_of("Title"))
				.c_line(self.value_of("C Line"))
				.p_line(self.value_of("P Line"))
				.year(self.value_of("Year"))
				.reference("R0")
				.release_id(ReleaseIdType.Upc,self.value_of("UPC"))
				.release_type(self.value_of("Type"))
				.artist(self.value_of("Artist"))
				.label(self.value_of("Label"))
				.parental_warning(self.value_of("Explicit"))
				.build())

	def all_release_fields_valid(self):
		all_valid = True
		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		return all_valid
