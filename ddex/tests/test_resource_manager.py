import unittest
from shutil import rmtree
from os import path
from tempfile import gettempdir
import uuid
from DDEXUI.file_parser import FileParser
from DDEXUI.ddex.resource import SoundRecording, Image
from DDEXUI.resource_manager import ResourceManager

class ResourceManagerSoundRecordingTests(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.upc = "49024343245"
		self.isrc = "FR343245"
		rmtree(self.upc, ignore_errors=True)
		self.root_folder = gettempdir()
		self.batch_id = str(uuid.uuid4())
		self.title = "the title"
		file_path = path.join('ddex','tests','resources','test.mp3')

		self.expected = SoundRecording('',self.isrc, self.title, FileParser().parse(file_path), '')

		self.subject = ResourceManager(FileParser(), self.batch_id, self.root_folder)

		self.resource = self.subject.add_sound_recording(self.upc, file_path, self.isrc, self.title)

	def test_should_copy_file_to_product_resources_folder(self):
		expected_path = path.join(self.root_folder, self.batch_id, self.upc, 'resources', self.isrc+'.mp3')
		self.assertTrue(path.isfile(expected_path))

	def test_should_create_resource_with_isrc(self):
		self.assertEqual(self.resource.isrc, self.expected.isrc)

	def test_should_create_resource_with_title(self):
		self.assertEqual(self.resource.title, self.expected.title)

	def test_should_create_resource_with_file(self):
		self.assertEqual(self.resource.file_metadata.md5, self.expected.file_metadata.md5)


class ResourceManagerImageTests(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.upc = "49024343245"
		self.isrc = "FR343245"
		rmtree(self.upc, ignore_errors=True)
		self.root_folder = gettempdir()
		self.batch_id = str(uuid.uuid4())
		self.title = "the title"
		file_path = path.join('ddex', 'tests', 'resources', 'test.jpg')

		self.expected = Image('', self.upc, FileParser().parse(file_path), '')

		self.subject = ResourceManager(FileParser(), self.batch_id, self.root_folder)

		self.resource = self.subject.add_image(self.upc, file_path)

	def test_should_copy_file_to_product_resources_folder(self):
		expected_path = path.join(self.root_folder, self.batch_id, self.upc, 'resources', self.upc+'.jpg')
		self.assertTrue(path.isfile(expected_path))

	def test_should_create_resource_with_upc(self):
		self.assertEqual(self.resource.id_value(), self.upc)

	def test_should_create_resource_with_file(self):
		self.assertEqual(self.resource.file_metadata.md5, self.expected.file_metadata.md5)
