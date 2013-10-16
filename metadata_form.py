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
		self.fields = ({
			"Title" : Validate().not_empty, 
			"UPC": Validate().upc, 
			"Year": Validate().year, 
			"C Line": Validate().not_empty, 
			"P Line": Validate().not_empty
		})

	def on_invalidate(self, row):
		tk.tkinter.Label(self.top, text="wrong", fg="red").grid(row=row, column=2)

	def on_validate(self, S):
		print("validating"+S)
		return S == "abc"

	def add_entry(self, row, title):
		text = tk.tkinter.StringVar()
		self.values[title] = text
		entry = tk.Entry(self.top,width=10, textvariable=text, validate="focusout", validatecommand=lambda: self.on_validate(text.get()), invalidcommand=lambda: self.on_invalidate(row)) \
		.grid(row=row, column=0)
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
		for i in range(len(self.fields.keys())):
			self.add_entry(i, list(self.fields.keys())[i])
		tk.Button(self.top, text="OK", command=self.create_ddex, state="disabled").grid(row=len(self.fields), column=0)
		self.top.mainloop()

Program().main()
