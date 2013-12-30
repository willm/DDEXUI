import unittest
from shutil import rmtree, copyfile
from os import path, getcwd, makedirs
from tempfile import gettempdir
import uuid
from DDEXUI.file_parser import FileParser
from DDEXUI.ddex.file_metadata import FileMetadata
from DDEXUI.ddex.resource import SoundRecording

class ResourceManagerTests(unittest.TestCase):
	def setUp(self):
		self.upc = "49024343245"
		self.isrc = "FR343245"
		rmtree(self.upc, ignore_errors=True)
		self.root_folder = gettempdir()
		self.batch_id = str(uuid.uuid4())
		self.title = "the title"
		file_path = path.join('ddex','tests','resources','test.mp3')
		

		self.expected = SoundRecording('',self.isrc, self.title, FileParser().parse(file_path), '')

		self.subject = ResourceManager(FileParser(), self.batch_id, self.upc, self.root_folder)

		self.resource = self.subject.add_resource(file_path, self.isrc, self.title)

	def test_should_copy_file_to_product_resources_folder(self):
		expected_path = path.join(self.root_folder, self.batch_id, self.upc, 'resources', self.isrc+'.mp3')
		self.assertTrue(path.isfile(expected_path))

	def test_should_create_resource_with_isrc(self):
		self.assertEqual(self.resource.isrc, self.expected.isrc)

	def test_should_create_resource_with_title(self):
		self.assertEqual(self.resource.title, self.expected.title)

	def test_should_create_resource_with_title(self):
		self.assertEqual(self.resource.title, self.expected.title)

	def test_should_create_resource_with_file(self):
		self.assertEqual(self.resource.file_metadata.md5, self.expected.file_metadata.md5)

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
