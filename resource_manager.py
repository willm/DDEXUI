from shutil import copyfile
from DDEXUI.file_parser import FileParser
from os import path, makedirs
from DDEXUI.ddex.resource import SoundRecording, Image

class ResourceManager:
	def __init__(self, file_parser ,batch_id, upc, root_folder='.'):
		self._batch_id = batch_id
		self._root_folder = root_folder
		self._upc = upc
		self._file_parser = file_parser
	
	def add_sound_recording(self, file_path, isrc, title):
		resources_directory = path.join(self._root_folder, self._batch_id, self._upc, 'resources')
		file_name = self.__file_name_from(isrc, file_path)
		moved_file_path = self.__copy_file(file_path, file_name)
		
		return SoundRecording('', isrc, title, self._file_parser.parse(moved_file_path), '')
	
	def add_image(self, file_path):
		file_name = self.__file_name_from(self._upc, file_path)
		moved_file_path = self.__copy_file(file_path, file_name)
		return Image('', self._upc, '', '')

	def __copy_file(self, src_file_path, dst_file_name):
		resources_directory = path.join(self._root_folder, self._batch_id, self._upc, 'resources')
		moved_file_path = path.join(resources_directory, dst_file_name)
		if(not path.isdir(resources_directory)):
			makedirs(resources_directory)
		copyfile(src_file_path, moved_file_path)
		return moved_file_path

	def __file_name_from(self, name, file_path):
		return name + '.' + FileParser.get_extension(file_path).lower()
