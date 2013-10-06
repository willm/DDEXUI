import tkinter as tk

class Program:

	def __init__(self):
		self.values = {}
		self.top = tk.Tk()
		self.top.title("Metadata Editor")
		self.fields = ["Title", "Artist", "UPC", "Year", "C Line", "P Line"]

	def addEntry(self, row, title):
		text = tk.StringVar()
		self.values[title] = text
		entry = tk.Entry(self.top,width=10, textvariable=text).grid(row=row, column=0)
		label = tk.Label(self.top,text=title).grid(row=row, column=1)

	def doit(self):
		for key, value in self.values.items():
			print(key, value.get())

	def main(self):
		for i in range(0,len(self.fields)):
			self.addEntry(i, self.fields[i])
		tk.Button(self.top, text="OK", command=self.doit).grid(row=len(self.fields), column=0)
		self.top.mainloop()

Program().main()
