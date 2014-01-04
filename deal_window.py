import DDEXUI.ddex.deal as deal
from DDEXUI.inputs import *
from DDEXUI.ddex.validate import Validate
from DDEXUI.tkinterutil import showerrorbox

class DealWindow(tk.tkinter.Toplevel):
	def __init__(self, frame):
		tk.tkinter.Toplevel.__init__(self, frame)
		self.title("Deal Editor")
		self.focus_set()
		self.fields = ([OptionInput(self, "Commercial Model", *deal.CommercialModals),
			OptionInput(self, "Use Type", *deal.UseTypes),
			OptionInput(self, "Territory", *deal.Territories),
			EntryInput(self, "Start Date", Validate().date),
			EntryInput(self, "Pre Order Date", Validate().date),
			EntryInput(self, "Pre Order Preview Date", Validate().date)])
		for i in range(len(self.fields)):
			self.fields[i].draw(i)
		tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=len(self.fields)+1, column=0)

	def __destroy_if_valid(self):
		if(self.all_release_fields_valid()):
			self.destroy()	

	@showerrorbox
	def create_deal(self):
		return (deal.Deal(self.value_of("Commercial Model"),
			self.value_of("Use Type"),
			self.value_of("Territory"),
			self.value_of("Start Date"),
			self.value_of("Pre Order Date"),
			self.value_of("Pre Order Preview Date")))

#todo: remove duplication of these 2 methods
	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()

	def all_release_fields_valid(self):
		all_valid = True
		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		return all_valid
