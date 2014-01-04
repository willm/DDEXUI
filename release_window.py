import tkinter.ttk as tk
from tkinter.filedialog import LoadFileDialog
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.validate import Validate
from DDEXUI.ddex.resource import Image, SoundRecording
from DDEXUI.inputs import *
from DDEXUI.ddex.release import *
from DDEXUI.deal_window import DealWindow
from DDEXUI.file_parser import FileParser
from DDEXUI.tkinterutil import showerrorbox

class ReleaseWindow(tk.tkinter.Toplevel):
	def __init__(self, frame):
		tk.tkinter.Toplevel.__init__(self, frame)
		self.fields = ([
			EntryInput(self, "Title", Validate().not_empty), 
			EntryInput(self, "Year", Validate().year), 
			EntryInput(self, "C Line", Validate().not_empty),
			EntryInput(self, "P Line", Validate().not_empty),
			EntryInput(self, "Artist", Validate().not_empty),
			EntryInput(self, "Label", Validate().not_empty),
			OptionInput(self, "Type", 'Single', 'Album'),
			CheckboxInput(self, "Explicit")
		])

	def draw_fields(self):
		for i in range(len(self.fields)):
			self.fields[i].draw(i)

	def create_deal(self):
		deal_window = DealWindow(self)
		deal_window.wait_window()
		deal = deal_window.create_deal()
		self._release_builder.add_deal(deal)

class ProductReleaseWindow(ReleaseWindow):
	def __init__(self, frame):	
		ReleaseWindow.__init__(self, frame)
		self.ddex_builder = DDEXBuilder()
		self._release_builder = ReleaseBuilder()
		self.tracks = []
		self.image = None
		self.fields.append(EntryInput(self, "UPC", Validate().upc))
		self.is_update_check_box = CheckboxInput(self, "Is Update")
		self.fields.append(self.is_update_check_box)
		total_fields = len(self.fields)
		self.draw_fields() 
		self.add_deal_button = tk.Button(self, text="Add deal", command=self.create_deal).grid(row=total_fields+1, column=0)
		self.add_track_button = tk.Button(self, text="Add Track", command=self.create_track).grid(row=total_fields+2, column=0)
		self.add_img_button = tk.Button(self, text="Album Artwork", command=self.add_image).grid(row=total_fields+3, column=0)
		self.button = tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=total_fields+4, column=0)
		self.track_list = tk.tkinter.Listbox(self)
		self.track_list.grid(row=total_fields+5, column=0)
		self.draw_tracks()

	@showerrorbox
	def add_image(self):
		file_dialog = LoadFileDialog(self)
		img_file = file_dialog.go(pattern="*.jpg")
		file_metadata = FileParser().parse(img_file)
		self.image = Image('A1', 'xx', file_metadata, "T1")

	def draw_tracks(self):
		for track in self.tracks:
			self.track_list.insert(tk.tkinter.END, track.title)

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title, self.fields))
		return row.value()
		
	def __destroy_if_valid(self):
		if(self.all_release_fields_valid()):
			self.destroy()

	def create_ddex(self):
		product_release = (self._release_builder.title(self.value_of("Title"))
				.c_line(self.value_of("C Line"))
				.p_line(self.value_of("P Line"))
				.year(self.value_of("Year"))
				.reference("R0")
				.release_id(ReleaseIdType.Upc,self.value_of("UPC"))
				.release_type(self.value_of("Type"))
				.artist(self.value_of("Artist"))
				.label(self.value_of("Label"))
				.parental_warning(self.value_of("Explicit")))
		if(self.image != None):
			product_release.add_resource(self.image.resource_reference())
			self.ddex_builder.add_resource(self.image)
		product_release = product_release.build()
		self.ddex_builder.update(self.is_update_check_box.value())
		self.ddex_builder.add_release(product_release)
		for track in self.tracks:
			self.ddex_builder.add_release(track)
		return self.ddex_builder

	@showerrorbox
	def create_track(self):
		track_window = TrackReleaseWindow(self)
		track_window.wait_window()
		track = track_window.create_release()
		self.tracks.append(track)
		self.track_list.insert(tk.tkinter.END, track.title)

	def all_release_fields_valid(self):
		all_valid = True
		if(self.is_update_check_box.value() != True):
			all_valid = self.image != None

		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		return all_valid

class TrackReleaseWindow(ReleaseWindow):
	def __init__(self, frame):	
		ReleaseWindow.__init__(self, frame)
		self._release_builder = ReleaseBuilder()
		self.fields.append(EntryInput(self, "ISRC", Validate().not_empty))
		total_fields = len(self.fields)
		self.draw_fields()
		self.add_sound_recording_button = tk.Button(self, text="Add Audio", command=self.add_audio).grid(row=total_fields+1, column=0)
		self.add_deal_button = tk.Button(self, text="Add deal", command=self.create_deal).grid(row=total_fields+2, column=0)
		self.button = tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=total_fields+3, column=0)

	def add_audio(self):
		pass

	def value_of(self, title):
		row = next(filter(lambda x: x.title == title,self.fields))
		return row.value()

	def __destroy_if_valid(self):
		if(self.all_release_fields_valid()):
			self.destroy()

	def create_release(self):
		return (self._release_builder.title(self.value_of("Title"))
				.c_line(self.value_of("C Line"))
				.p_line(self.value_of("P Line"))
				.year(self.value_of("Year"))
				.reference("R0")
				.release_id(ReleaseIdType.Isrc,self.value_of("ISRC"))
				.release_type(self.value_of("Type"))
				.artist(self.value_of("Artist"))
				.label(self.value_of("Label"))
				.parental_warning(self.value_of("Explicit"))
				.build())

	def all_release_fields_valid(self):
		all_valid = True
		for row in self.fields:
			all_valid = all_valid and row.on_validate()
		return all_valid
