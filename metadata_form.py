#!/usr/bin/python3.3
import tkinter.ttk as tk
import tkinter.messagebox as mb
from DDEXUI.ddex.release import *
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.party import *
from DDEXUI.ddex.validate import Validate
from DDEXUI.party_repository import PartyRepository
from  datetime import datetime as datetime
import DDEXUI.ddex.deal as deal

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

	def create_deal(self):
		#massive hack sort out this ugly date parsing
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

class PartyWindow(tk.tkinter.Toplevel):
	def __init__(self, frame, party_type):
		#http://tkinter.unpythonic.net/wiki/ModalWindow	
		self.party_repository = PartyRepository()
		self.party_type = party_type
		tk.tkinter.Toplevel.__init__(self, frame)
#		self.geometry("400x300")
		self.transient(frame)
		self.focus_set()
		#self.grab_set()
		message = "Please enter your " + PartyType.reverse_mapping[self.party_type] + " ddex party details. You can apply for a ddex Party id for free at: http://ddex.net/content/implementation-licence-application-form"
		text = tk.tkinter.Label(self, height=5, text=message, wraplength=400)
		text.grid(row=0, column=0,columnspan=3)
		self.party_id = EntryInput(self, "Party Id", Validate().not_empty)
		self.party_name = EntryInput(self, "Party Name", Validate().not_empty)
		self.party_id.draw(2)
		self.party_name.draw(3)
		tk.Button(self, text="OK", command=self.save_and_close).grid(row=4, column=0)
		frame.wait_window(self)

	def save_and_close(self):
		if(self.party_id.on_validate() and self.party_name.on_validate()):
			party = Party(self.party_id.value(), self.party_name.value(), self.party_type)
			self.party_repository.write_party(party)
			self.destroy()

class Program:
	def __init__(self):
		self.party_repository = PartyRepository()
		self._release_builder = ReleaseBuilder()
		self.top = tk.tkinter.Tk()
		self.top.geometry("600x300")
		icon = tk.tkinter.PhotoImage(file="res/favicon.gif")
		self.top.tk.call("wm", "iconphoto", self.top._w, icon)
		self.top.title("Metadata Editor")
		self.fields = ([
			EntryInput(self.top, "Title", Validate().not_empty), 
			EntryInput(self.top, "UPC", Validate().upc), 
			EntryInput(self.top, "Year", Validate().year), 
			EntryInput(self.top, "C Line", Validate().not_empty),
			EntryInput(self.top, "P Line", Validate().not_empty),
			EntryInput(self.top, "Artist", Validate().not_empty),
			EntryInput(self.top, "Label", Validate().not_empty),
			OptionInput(self.top, "Type", 'Single', 'Album'),
			CheckboxInput(self.top, "Explicit")
		])
		self.add_deal_button = tk.Button(self.top, text="Add deal", command=self.create_deal)
		self.button = tk.Button(self.top, text="OK", command=self.create_ddex)

	def create_deal(self):
		deal_window = DealWindow(self.top)
		deal_window.wait_window()
		deal = deal_window.create_deal()
		self._release_builder.add_deal(deal)

	def create_ddex(self):
		self.__check_for_party(PartyType.MessageSender)
		self.__check_for_party(PartyType.MessageRecipient)
		if(self.all_release_fields_valid()):
			product_release = self.rehydrate_release()
			sender = self.party_repository.get_party(PartyType.MessageSender)
			recipient = self.party_repository.get_party(PartyType.MessageRecipient)
			DDEX(sender, recipient, [product_release]).write("/tmp/file.xml")
			mb.showinfo("DDEXUI", "your ddex file has been created")

	def all_release_fields_valid(self):
		all_valid = True
		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		return all_valid

	def rehydrate_release(self):
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

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()

	def __check_for_party(self, party_type):
		if(self.party_repository.get_party(party_type) is None):
			PartyWindow(self.top, party_type)

	def __check_for_recipient(self):
		if(self.party_repository.get_recipient_party() is None):
			pass

	def main(self):
		i = 0
		for row in self.fields:
			row.draw(i)
			i += 1
		self.button.grid(row=len(self.fields), column=0)
		self.add_deal_button.grid(row=len(self.fields)+1, column=0)
		self.__check_for_party(PartyType.MessageSender)
		self.top.mainloop()

class InputRow:
	def __init__(self, frame, title):
		self.frame = frame
		self.error_label = tk.tkinter.Label(self.frame, fg="red", width=50)
		self.v = tk.tkinter.StringVar()
		self.title = title
		self.input = None

	def value(self):
		return self.v.get()

	def on_validate(self):
		return True

	def draw(self, row):
		self.input.grid(row=row, column=1)
		self.error_label.grid(row=row, column=2)

class OptionInput(InputRow):
	def __init__(self, frame, title, *args):
		InputRow.__init__(self, frame, title)
		self.v.set(args[0])
		self.input = tk.OptionMenu(self.frame, self.v, args[0], *args)
		self.label = tk.Label(self.frame,text=title)

	def draw(self,row):
		InputRow.draw(self, row)
		self.label.grid(row=row, column=0)
	
class CheckboxInput(InputRow):
	def __init__(self, frame, title):
		InputRow.__init__(self, frame, title)
		self.v = tk.tkinter.BooleanVar()
		self.v.set(False)
		self.input = tk.Checkbutton(self.frame, variable=self.v, text=title)

class EntryInput(InputRow):
	def __init__(self, frame, title, validation_function):
		InputRow.__init__(self, frame, title)
		self.validation_function = validation_function
		self.label = tk.Label(self.frame,text=title)
		self.input = (tk.Entry(
			self.frame,
			width=20, 
			textvariable=self.v, 
			validate="focusout", 
			validatecommand=self.on_validate,
			invalidcommand=lambda: self.on_invalidate(self.validation_function(self.v.get())["error"])))
		self.v.set("2121211111141")

	def is_valid(self):
		return self.validation_function(self.v.get())["success"]	== True

	def value(self):
		return self.validation_function(self.v.get())["value"]


	def draw(self,row):
		InputRow.draw(self, row)
		self.label.grid(row=row, column=0,sticky=tk.tkinter.W) 

	def on_invalidate(self, message):
		self.error_label["text"] = message

	def on_validate(self):
		valid = self.is_valid()
		if(valid):
			self.error_label["text"] = ""
		return valid

	

Program().main()
