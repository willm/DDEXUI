import tkinter.ttk as tk
from DDEXUI.ddex.productRelease import ProductRelease
from DDEXUI.ddex.ddex import DDEX

class Program:

	def __init__(self):
		self.values = {}
		self.top = tk.tkinter.Tk()
		self.top.geometry("300x300")
		self.top.title("Metadata Editor")
		self.fields = ["Title", "UPC", "Year", "C Line", "P Line"]

	def on_invalidate(self, row):
		tk.tkinter.Label(self.top, text="wrong", fg="red").grid(row=row, column=2)

	def on_validate(self, S):
		print("validating"+S)
		return S == "abc"

	def add_entry(self, row, title):
		text = tk.tkinter.StringVar()
		self.values[title] = text
		vcmd = (self.top.register(self.on_validate), '%S')
		entry = tk.Entry(self.top,width=10, textvariable=text, validate="focusout", validatecommand=vcmd, invalidcommand=lambda: self.on_invalidate(row)).grid(row=row, column=0)
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
		for i in range(0,len(self.fields)):
			self.add_entry(i, self.fields[i])
		tk.Button(self.top, text="OK", command=self.create_ddex).grid(row=len(self.fields), column=0)
		self.top.mainloop()

Program().main()
