#!/usr/bin/python3.3
import os
import sys

from ddex import generate_batch_id
from ddex.party import PartyType, Party
from ddex.validate import Validate
from ddexui.batch_generator import BatchGenerator
from ddexui.inputs import EntryInput
from ddexui.party_repository import PartyRepository
from ddexui.release_window import ProductReleaseWindow
from ddexui.tkinterutil import showerrorbox


try:
    import Tkinter as tkinter
    from Tkinter import Toplevel, Label
    import ttk as tk
    import tkMessageBox as mb
except ImportError as e:
    print "IMPORT ERROR" + str(e)
    import tkinter
    from tkinter import Toplevel, Label
    import tkinter.ttk as tk
    import tkinter.messagebox as mb

class PartyWindow(Toplevel):
    def __init__(self, frame, party_type):
        #http://tkinter.unpythonic.net/wiki/ModalWindow 
        self.party_repository = PartyRepository()
        self.party_type = party_type
        Toplevel.__init__(self, frame)
#       self.geometry("400x300")
        self.transient(frame)
        self.focus_set()
        #self.grab_set()
        message = "Please enter your " + PartyType.reverse_mapping[self.party_type] + " ddex party details. You can apply for a ddex Party id for free at: http://ddex.net/content/implementation-licence-application-form"
        text = Label(self, height=5, text=message, wraplength=400)
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
        self.frame = tkinter.Tk()
        self.frame.geometry("600x300")
        icon = tkinter.PhotoImage(file=self.get_icon())
        self.frame.tk.call("wm", "iconphoto", self.frame._w, icon)
        self.frame.title("Metadata Editor")
        self.product_list = tkinter.Listbox(self.frame)
        self.product_list.bind('<Delete>', lambda x: self.remove_product())
        self._root_folder = "out"
        self.add_release_button = tk.Button(self.frame, text="Add Product", command=self.create_ddex)
        self.button = tk.Button(self.frame, text="OK", command=self.write_ddex)
        self.remove_button = tk.Button(self.frame, text="Remove", command=self.remove_product, state="disabled")
        self._batch_id = generate_batch_id()
        self._batch_generator = BatchGenerator(self._root_folder, self._batch_id)

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

    def get_icon(self):
        if getattr(sys, 'frozen', False):
            resources = os.path.join(os.path.dirname(sys.executable), 'res')
        else:
            resources = os.path.join(os.path.dirname(__file__), 'res')
        return os.path.join(resources, 'favicon.gif')

    @showerrorbox
    def create_ddex(self):
        release_window = ProductReleaseWindow(self.frame, self._root_folder, self._batch_id)
        release_window.wait_window()
        ddex_builder = release_window.create_ddex()
        self._ddex_builders.append(ddex_builder)
        self.product_list.insert(tkinter.END, ddex_builder.get_upc())
        self.remove_button['state'] = 'enabled'

    @showerrorbox
    def remove_product(self):
        selected = self.product_list.curselection()
        if(self.product_list.size() == 0 or len(selected) == 0):
            return
        self.product_list.delete(selected[0])
        self._ddex_builders.pop(int(selected[0]))
        if(self.product_list.size() == 0):
            self.remove_button['state'] = 'disabled'

    def __check_for_party(self, party_type):
        if(self.party_repository.get_party(party_type) is None):
            PartyWindow(self.frame, party_type)

    def main(self):
        self.product_list.grid(row=0, column=0)
        self.add_release_button.grid(row=1, column=0)
        self.remove_button.grid(row=2, column=0)
        self.button.grid(row=3, column=0)
        self.__check_for_party(PartyType.MessageSender)
        self.frame.mainloop()

Program().main()
