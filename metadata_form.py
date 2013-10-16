import tkinter.ttk as tk
from DDEXUI.ddex.productRelease import ProductRelease
from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.validate import Validate

class Program:

	def __init__(self):
		self.values = {}
		self.top = tk.tkinter.Tk()
		self.top.geometry("300x300")
		self.top.title("Metadata Editor")
		self.fields = ([
			InputRow(self.top, "Title", Validate().not_empty), 
			InputRow(self.top, "UPC", Validate().upc), 
			InputRow(self.top, "Year", Validate().year), 
			InputRow(self.top, "C Line", Validate().not_empty),
			InputRow(self.top, "P Line", Validate().not_empty)
		])

	def on_invalidate(self, row, message):
		tk.tkinter.Label(self.top, text=message, fg="red").grid(row=row, column=2)

	def on_validate(self):
		print("validating"+S)
		return S == "abc"

	def add_entry(self, row, title, validation_function):
		text = tk.tkinter.StringVar()
		self.values[title] = text
		entry = (tk.Entry(
			self.top,
			width=10, 
			textvariable=text, 
			validate="focusout", 
			validatecommand=lambda: validation_function(text.get())["success"] == True, 
			invalidcommand=lambda: self.on_invalidate(row, validation_function(text.get())["error"]))
		.grid(row=row, column=0))

		label = tk.Label(self.top,text=title).grid(row=row, column=1)

	def create_ddex(self):
		if(self.valid()):
			product_release = build_product_release()
			DDEX(product_release).write()

	def build_product_release(self):
		product_release = ProductRelease()
		product_release.product_name = self.value_of("Title")
		product_release.upc = self.value_of("UPC")
		product_release.cline = self.value_of("C Line")
		product_release.pline = self.value_of("P Line")
		product_release.year = self.value_of("Year")
		return product_release

	def valid(self):
		return True

	def value_of(self, key):
		return self.values[key].get()

	def main(self):
		i = 0
		for row in self.fields:
			row.draw(i)
			i += 1
		tk.Button(self.top, text="OK", command=self.create_ddex, state="disabled").grid(row=len(self.fields), column=0)
		self.top.mainloop()

class InputRow:
	def __init__(self, frame, title, validation_function):
		self.frame = frame
		self.validation_function = validation_function
		self.error_label = tk.tkinter.Label(self.frame, fg="red")
		self.text = tk.tkinter.StringVar()
		self.label = tk.Label(self.frame,text=title)
		self.entry = (tk.Entry(
			self.frame,
			width=10, 
			textvariable=self.text, 
			validate="focusout", 
			validatecommand=lambda: self.on_validate(self.text),
			invalidcommand=lambda: self.on_invalidate(self.validation_function(self.text.get())["error"])))

	def draw(self, row):
		self.error_label.grid(row=row, column=2)
		self.label.grid(row=row, column=1)
		self.entry.grid(row=row, column=0)

	def on_validate(self, text):
		valid = self.validation_function(text.get())["success"]	== True
		if(valid):
			self.error_label["text"] = ""
		return valid

	def on_invalidate(self, message):
		self.error_label["text"] = message

Program().main()
