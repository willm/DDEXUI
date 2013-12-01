import tkinter.ttk as tk

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
