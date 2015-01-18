from os import path
import os
from shutil import rmtree
from tempfile import gettempdir
import unittest
import uuid

from ddex.resource import SoundRecording, Image
from ddexui.file_parser import FileParser
from ddexui.resource_manager import ResourceManager


class ResourceManagerSoundRecordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.upc = "49024343245"
        self.isrc = "FR343245"
        rmtree(self.upc, ignore_errors=True)
        self.root_folder = gettempdir()
        self.batch_id = str(uuid.uuid4())
        self.title = "the title"
        
        file_path = path.join(os.path.dirname(__file__), 'resources', 'test.mp3')
        self.resource_reference = "A1"
        self.technical_resource_details_reference = "T1"

        self.expected = SoundRecording(self.resource_reference, self.isrc, self.title, FileParser().parse(file_path), self.technical_resource_details_reference)

        self.subject = ResourceManager(FileParser(), self.batch_id, self.root_folder)

        self.resource = self.subject.add_sound_recording(self.upc, file_path, self.isrc, self.title, self.resource_reference, self.technical_resource_details_reference)

    def test_should_copy_file_to_product_resources_folder(self):
        expected_path = path.join(self.root_folder, self.batch_id, self.upc, 'resources', "{}_{}.mp3".format(self.isrc, self.technical_resource_details_reference))
        self.assertTrue(path.isfile(expected_path), "expected {} to exist".format(expected_path))

    def test_should_create_resource_with_isrc(self):
        self.assertEqual(self.resource.isrc, self.expected.isrc)

    def test_should_create_resource_with_title(self):
        self.assertEqual(self.resource.title, self.expected.title)

    def test_should_create_resource_with_resource_reference(self):
        self.assertEqual(self.resource.resource_reference(), self.resource_reference)

    def test_should_create_resource_with_technical_resource_details_reference(self):
        self.assertEqual(self.resource.technical_resource_details_reference, self.technical_resource_details_reference)

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
        file_path = os.path.join(os.path.dirname(__file__), "resources", "test.jpg")
        self.resource_reference = "A2"
        self.technical_resource_details_reference = "T4"

        self.expected = Image(self.resource_reference, self.upc, FileParser().parse(file_path), '')

        self.subject = ResourceManager(FileParser(), self.batch_id, self.root_folder)

        self.resource = self.subject.add_image(self.upc, file_path, self.resource_reference, self.technical_resource_details_reference)

    def test_should_copy_file_to_product_resources_folder(self):
        expected_path = path.join(self.root_folder, self.batch_id, self.upc, 'resources', self.upc+'.jpg')
        self.assertTrue(path.isfile(expected_path))

    def test_should_create_resource_with_upc(self):
        self.assertEqual(self.resource.id_value(), self.upc)

    def test_should_create_resource_with_file(self):
        self.assertEqual(self.resource.file_metadata.md5, self.expected.file_metadata.md5)

    def test_should_create_resource_with_resource_reference(self):
        self.assertEqual(self.resource.resource_reference(), self.resource_reference)

    def test_should_create_resource_with_technical_resource_details_reference(self):
        self.assertEqual(self.resource.technical_resource_details_reference, self.technical_resource_details_reference)
