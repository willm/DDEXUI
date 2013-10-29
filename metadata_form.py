import tkinter.ttk as tk
import tkinter.messagebox as mb
from DDEXUI.ddex.release import Release, ReleaseId
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.validate import Validate
from DDEXUI.party_repository import PartyRepository

class PartyWindow(tk.tkinter.Toplevel):
	def __init__(self, frame):
		#http://tkinter.unpythonic.net/wiki/ModalWindow	
		tk.tkinter.Toplevel.__init__(self, frame)
		self.transient(frame)
		self.focus_set()
		self.grab_set()
		frame.wait_window(self)

class Program:

	def __init__(self):
		self.party_repository = PartyRepository()
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
		self.button = tk.Button(self.top, text="OK", command=self.create_ddex)

	def create_ddex(self):
		all_valid = True
		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		if(all_valid):
			product_release = self.build_product_release()
			DDEX(product_release).write()
			mb.showinfo("DDEXUI", "your ddex file has been created")

	def build_product_release(self):
		return (Release(
			self.value_of("Title"),
			self.value_of("C Line"),
			self.value_of("P Line"),
			self.value_of("Year"),
			"R0",
			ReleaseId(1,self.value_of("UPC")),
			self.value_of("Type"),
			self.value_of("Artist"),
			self.value_of("Label"),
			self.value_of("Explicit")))

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()

	def main(self):
		i = 0
		for row in self.fields:
			row.draw(i)
			i += 1
		self.button.grid(row=len(self.fields), column=0)
		if(self.party_repository.get_party() is None):
			PartyWindow(self.top)
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

	def draw(self,row):
		InputRow.draw(self, row)
		self.label.grid(row=row, column=0)

	def on_invalidate(self, message):
		self.error_label["text"] = message

	def on_validate(self):
		valid = self.is_valid()
		if(valid):
			self.error_label["text"] = ""
		return valid

	

Program().main()
