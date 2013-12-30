import unittest
from shutil import rmtree, copyfile
from os import path, getcwd, makedirs
from tempfile import gettempdir
import uuid
from DDEXUI.file_parser import FileParser

class ResourceManagerTests(unittest.TestCase):
	def setUp(self):
		self.upc = "49024343245"
		self.isrc = "FR343245"
		rmtree(self.upc, ignore_errors=True)
		self.root_folder = gettempdir()
		self.batch_id = str(uuid.uuid4())
		self.subject = ResourceManager(self.batch_id, self.upc, self.root_folder)
		self.subject.add_resource(path.join('ddex','tests','resources','test.mp3'), self.isrc)

	def test_should_copy_file_to_product_resources_folder(self):
		expected = path.join(self.root_folder, self.batch_id, self.upc, 'resources', self.isrc+'.mp3')
		self.assertTrue(path.isfile(expected))


class ResourceManager:
	def __init__(self, batch_id, upc, root_folder='.'):
		self.batch_id = batch_id
		self.root_folder = root_folder
		self.upc = upc
	
	def add_resource(self, file_path, isrc):
		resources_directory = path.join(self.root_folder, self.batch_id, self.upc, 'resources')
		if(not path.isdir(resources_directory)):
			makedirs(resources_directory)
		copyfile(file_path, path.join(resources_directory, isrc + '.' + FileParser.get_extension(file_path).lower()))
