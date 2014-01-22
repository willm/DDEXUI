import tkinter.ttk as tk
from tkinter.filedialog import askopenfilename
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.validate import Validate
from DDEXUI.inputs import *
from DDEXUI.ddex.release import *
from DDEXUI.deal_window import DealWindow
from DDEXUI.file_parser import FileParser
from DDEXUI.tkinterutil import showerrorbox
from DDEXUI.resource_manager import ResourceManager
from DDEXUI.product_service import ProductService

class ReleaseWindow(tk.tkinter.Toplevel):
    def __init__(self, frame):
        tk.tkinter.Toplevel.__init__(self, frame)
        self._release_builder = ReleaseBuilder()
        self.fields = ([
            EntryInput(self, "Title", Validate().not_empty),
            EntryInput(self, "Year", Validate().year),
            EntryInput(self, "C Line", Validate().not_empty),
            EntryInput(self, "P Line", Validate().not_empty),
            EntryInput(self, "Artist", Validate().not_empty),
            EntryInput(self, "Label", Validate().not_empty),
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
    def __init__(self, frame, root_folder, batch_id):
        ReleaseWindow.__init__(self, frame)
        self.track_builder_file_paths = []
        self.image_path = None
        self._resource_manager = ResourceManager(FileParser(), batch_id, root_folder)
        self.fields.append(EntryInput(self, "UPC", Validate().upc))
        self.fields.append(OptionInput(self, "Type", 'Single', 'Album'))
        self.is_update_check_box = CheckboxInput(self, "Is Update")
        self.fields.append(self.is_update_check_box)
        self.total_fields = len(self.fields)
        self.draw_fields()
        self.add_deal_button = tk.Button(self, text="Add deal", command=self.create_deal)
        self.add_deal_button.grid(row=self.new_row(), column=0)
        self.add_track_button = tk.Button(self, text="Add Track", command=self.create_track)
        self.add_track_button.grid(row=self.new_row(), column=0)
        self.delete_track_button = tk.Button(self, text="Remove Track", state="disabled", command=self.remove_track)
        self.delete_track_button.grid(row=self.new_row(), column=0)
        self.add_img_button = tk.Button(self, text="Album Artwork", command=self.add_image).grid(row=self.new_row(), column=0)
        self.button = tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=self.new_row(), column=0)
        self.track_list = tk.tkinter.Listbox(self)
        self.track_list.bind('<Delete>', lambda x: self.remove_track())
        self.track_list.grid(row=self.new_row(), column=0)
        self.draw_tracks()

    def new_row(self):
        self.total_fields += 1
        return self.total_fields

    def add_image(self):
        self.image_path = askopenfilename(filetypes=[("JPG files", "*.jpg")])

    def draw_tracks(self):
        for track in self.track_builder_file_paths:
            self.track_list.insert(tk.tkinter.END, track.builder.get_title())

    def value_of(self, title):
        row = next(filter(lambda x: x.title == title, self.fields))
        return row.value()

    def __destroy_if_valid(self):
        if(self.all_release_fields_valid()):
            self.destroy()

    def _populate_product_release(self, upc):
        (self._release_builder.title(self.value_of("Title"))
                .c_line(self.value_of("C Line"))
                .p_line(self.value_of("P Line"))
                .year(self.value_of("Year"))
                .reference("R0")
                .release_id(ReleaseIdType.Upc, upc)
                .release_type(self.value_of("Type"))
                .artist(self.value_of("Artist"))
                .label(self.value_of("Label"))
                .parental_warning(self.value_of("Explicit")))

    def create_ddex(self):
        upc = self.value_of("UPC")
        self._populate_product_release(upc)
        product_service = (ProductService(self._release_builder,
            upc, self.image_path,
            self.track_builder_file_paths,
            self.is_update_check_box.value(),
            self._resource_manager))
        return product_service.create_ddex()

    @showerrorbox
    def create_track(self):
        track_window = TrackReleaseWindow(self)
        track_window.wait_window()
        track_builder_file_path = track_window.create_release()
        self.track_builder_file_paths.append(track_builder_file_path)
        self.track_list.insert(tk.tkinter.END, track_builder_file_path.builder.get_title())
        self.delete_track_button['state'] = 'enabled'

    @showerrorbox
    def remove_track(self):
        selected = self.track_list.curselection()
        if(self.track_list.size() == 0 or len(selected) == 0):
            return
        print(selected)
        self.track_list.delete(selected[0])
        self.track_builder_file_paths.pop(int(selected[0]))
        if(self.track_list.size() == 0):
            self.delete_track_button['state'] = 'disabled'

    def all_release_fields_valid(self):
        all_valid = True
        if(self.is_update_check_box.value() != True):
            all_valid = self.image_path is not None and self.image_path is not ""

        for row in self.fields:
            all_valid = all_valid and row.on_validate()
        return all_valid

class TrackReleaseWindow(ReleaseWindow):
    def __init__(self, frame):
        ReleaseWindow.__init__(self, frame)
        self._sound_file_paths = []
        self.fields.append(EntryInput(self, "ISRC", Validate().not_empty))
        total_fields = len(self.fields)
        self.draw_fields()
        self.add_sound_recording_button = tk.Button(self, text="Add Audio", command=self.add_audio).grid(row=total_fields+1, column=0)
        self.add_deal_button = tk.Button(self, text="Add deal", command=self.create_deal).grid(row=total_fields+2, column=0)
        self.button = tk.Button(self, text="OK", command=self.__destroy_if_valid).grid(row=total_fields+3, column=0)

    def add_audio(self):
        file_path = askopenfilename(filetypes=(("Audio files", "*.mp3"), ("Audio files", "*.flac")))
        if(file_path is not ""):
            self._sound_file_paths.append(file_path)

    def value_of(self, title):
        row = next(filter(lambda x: x.title == title, self.fields))
        return row.value()

    def __destroy_if_valid(self):
        if(self.all_release_fields_valid()):
            self.destroy()

    def create_release(self):
        builder = (self._release_builder.title(self.value_of("Title"))
                .c_line(self.value_of("C Line"))
                .p_line(self.value_of("P Line"))
                .year(self.value_of("Year"))
                .reference("R0")
                .release_id(ReleaseIdType.Isrc,self.value_of("ISRC"))
                .release_type("TrackRelease")
                .artist(self.value_of("Artist"))
                .label(self.value_of("Label"))
                .parental_warning(self.value_of("Explicit")))
        return TrackBuilderFilePath(self._sound_file_paths, builder)

    def all_release_fields_valid(self):
        all_valid = True
        for row in self.fields:
            all_valid = all_valid and row.on_validate()
        return all_valid

class TrackBuilderFilePath:
    def __init__(self, paths, builder):
        self.paths = paths
        self.builder = builder

