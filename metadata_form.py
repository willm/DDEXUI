#!/usr/bin/python3.3
import tkinter.ttk as tk
import tkinter.messagebox as mb
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.party import *
from DDEXUI.ddex.validate import Validate
from DDEXUI.party_repository import PartyRepository
from DDEXUI.inputs import *
from DDEXUI.release_window import ProductReleaseWindow

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
		self._ddex_builder = DDEXBuilder()
		self.frame = tk.tkinter.Tk()
		self.frame.geometry("600x300")
		icon = tk.tkinter.PhotoImage(file="res/favicon.gif")
		self.frame.tk.call("wm", "iconphoto", self.frame._w, icon)
		self.frame.title("Metadata Editor")
		self.add_release_button = tk.Button(self.frame, text="Add Product", command=self.create_release)
		self.button = tk.Button(self.frame, text="OK", command=self.create_ddex)

	def create_ddex(self):
		self.__check_for_party(PartyType.MessageSender)
		self.__check_for_party(PartyType.MessageRecipient)
		sender = self.party_repository.get_party(PartyType.MessageSender)
		recipient = self.party_repository.get_party(PartyType.MessageRecipient)
		(self._ddex_builder.update(False)
			.sender(sender)
			.recipient(recipient)
			.build()
			.write("file.xml"))
		mb.showinfo("DDEXUI", "your ddex file has been created")

	def create_release(self):
		release_window = ProductReleaseWindow(self.frame)
		release_window.wait_window()
		product_release = release_window.create_release()
		self._ddex_builder.add_release(product_release)

	def __check_for_party(self, party_type):
		if(self.party_repository.get_party(party_type) is None):
			PartyWindow(self.frame, party_type)

	def __check_for_recipient(self):
		if(self.party_repository.get_recipient_party() is None):
			pass

	def main(self):
		self.add_release_button.grid(row=1, column=0)
		self.button.grid(row=0, column=0)
		self.__check_for_party(PartyType.MessageSender)
		self.frame.mainloop()

Program().main()
