import unittest
from os import path
from tempfile import gettempdir
from shutil import rmtree
import DDEXUI.ddex.tests.data as data
from DDEXUI.batch_generator import BatchGenerator

class BatchGeneratorTests(unittest.TestCase):
	def test_should_generate_a_batch_containing_each_product(self):
		static_batch_id = "batchID"
		root_folder = gettempdir()
		expected_batch_path = path.join(root_folder, static_batch_id)
		rmtree(expected_batch_path, ignore_errors=True)
		subject = BatchGenerator(root_folder, static_batch_id)
		builders = [
			data.valid_ddex_builder(),
			data.valid_ddex_builder()
		]

		subject.generate(builders)

		for builder in builders:
			upc = builder.get_upc()
			expected_path = path.join(expected_batch_path, upc, upc + ".xml")
			self.assertTrue(path.isfile(expected_path), expected_path + " does not exist")
		
