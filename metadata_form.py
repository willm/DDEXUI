import tkinter.ttk as tk
import tkinter.messagebox as mb
from DDEXUI.ddex.productRelease import ProductRelease
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.validate import Validate

class Program:

	def __init__(self):
		self.top = tk.tkinter.Tk()
		self.top.geometry("600x300")
		self.top.title("Metadata Editor")
		self.fields = ([
			InputRow(self.top, "Title", Validate().not_empty), 
			InputRow(self.top, "UPC", Validate().upc), 
			InputRow(self.top, "Year", Validate().year), 
			InputRow(self.top, "C Line", Validate().not_empty),
			InputRow(self.top, "P Line", Validate().not_empty)
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
		return (ProductRelease(
			self.value_of("Title"),
			self.value_of("UPC"),
			self.value_of("C Line"),
			self.value_of("P Line"),
			self.value_of("Year")))

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()

	def main(self):
		i = 0
		for row in self.fields:
			row.draw(i)
			i += 1
		self.button.grid(row=len(self.fields), column=0)
		self.top.mainloop()

class InputRow:
	def __init__(self, frame, title, validation_function):
		self.frame = frame
		self.validation_function = validation_function
		self.error_label = tk.tkinter.Label(self.frame, fg="red", width=50)
		self.text = tk.tkinter.StringVar()
		self.text.set("2121211111141")
		self.label = tk.Label(self.frame,text=title)
		self.title = title
		self.entry = (tk.Entry(
			self.frame,
			width=20, 
			textvariable=self.text, 
			validate="focusout", 
			validatecommand=self.on_validate,
			invalidcommand=lambda: self.on_invalidate(self.validation_function(self.text.get())["error"])))

	def draw(self, row):
		self.label.grid(row=row, column=0)
		self.entry.grid(row=row, column=1)
		self.error_label.grid(row=row, column=2)

	def on_validate(self):
		valid = self.is_valid()
		if(valid):
			self.error_label["text"] = ""
		return valid

	def is_valid(self):
		return self.validation_function(self.text.get())["success"]	== True

	def value(self):
		return self.validation_function(self.text.get())["value"]

	def on_invalidate(self, message):
		self.error_label["text"] = message

Program().main()
