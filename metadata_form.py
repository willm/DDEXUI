#!/usr/bin/python3.3
import tkinter.ttk as tk
import tkinter.messagebox as mb
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.party import *
from DDEXUI.ddex.validate import Validate
from DDEXUI.party_repository import PartyRepository
from DDEXUI.inputs import *
from DDEXUI.release_window import ProductReleaseWindow
from DDEXUI.batch_generator import BatchGenerator
from DDEXUI.ddex.ddex import generate_batch_id
from DDEXUI.tkinterutil import showerrorbox

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
		self._ddex_builders = []
		self.frame = tk.tkinter.Tk()
		self.frame.geometry("600x300")
		icon = tk.tkinter.PhotoImage(file="res/favicon.gif")
		self.frame.tk.call("wm", "iconphoto", self.frame._w, icon)
		self.frame.title("Metadata Editor")
		self.product_list = tk.tkinter.Listbox(self.frame)
		self.add_release_button = tk.Button(self.frame, text="Add Product", command=self.create_ddex)
		self.button = tk.Button(self.frame, text="OK", command=self.write_ddex)
		self._batch_generator = BatchGenerator("out", generate_batch_id) 

	@showerrorbox
	def write_ddex(self):
		self.__check_for_party(PartyType.MessageSender)
		self.__check_for_party(PartyType.MessageRecipient)
		sender = self.party_repository.get_party(PartyType.MessageSender)
		recipient = self.party_repository.get_party(PartyType.MessageRecipient)
		for builder in self._ddex_builders:
			ddex = builder.sender(sender).recipient(recipient)
		self._batch_generator.generate(self._ddex_builders)
		mb.showinfo("DDEXUI", "your ddex files have been created")

	@showerrorbox
	def create_ddex(self):
		release_window = ProductReleaseWindow(self.frame)
		release_window.wait_window()
		ddex_builder = release_window.create_ddex()
		self._ddex_builders.append(ddex_builder)
		self.product_list.insert(tk.tkinter.END, ddex_builder.get_upc())

	def __check_for_party(self, party_type):
		if(self.party_repository.get_party(party_type) is None):
			PartyWindow(self.frame, party_type)

	def main(self):
		self.product_list.grid(row=0, column=0)
		self.add_release_button.grid(row=1, column=0)
		self.button.grid(row=2, column=0)
		self.__check_for_party(PartyType.MessageSender)
		self.frame.mainloop()

Program().main()
