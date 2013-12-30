from shutil import copyfile
from DDEXUI.file_parser import FileParser
from os import path, makedirs
from DDEXUI.ddex.resource import SoundRecording

class ResourceManager:
	def __init__(self, file_parser ,batch_id, upc, root_folder='.'):
		self._batch_id = batch_id
		self._root_folder = root_folder
		self._upc = upc
		self._file_parser = file_parser
	
	def add_resource(self, file_path, isrc, title):
		resources_directory = path.join(self._root_folder, self._batch_id, self._upc, 'resources')
		file_name = isrc + '.' + FileParser.get_extension(file_path).lower()
		moved_file_path = path.join(resources_directory, file_name)
		if(not path.isdir(resources_directory)):
			makedirs(resources_directory)
		copyfile(file_path, moved_file_path)
		
		return SoundRecording('', isrc, title, self._file_parser.parse(moved_file_path), '')
