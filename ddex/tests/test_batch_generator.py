import unittest
from DDEXUI.ddex.ddex import generate_batch_id
from os import path
from tempfile import gettempdir
from shutil import rmtree
from os import makedirs
import DDEXUI.ddex.tests.data as data

class BatchGeneratorTests(unittest.TestCase):
	def test_should_generate_a_batch_containing_each_product(self):
		static_batch_id = "batchID"
		root_folder = gettempdir()
		expected_batch_path = path.join(root_folder, static_batch_id)
		rmtree(expected_batch_path, ignore_errors=True)
		subject = BatchGenerator(root_folder, lambda: static_batch_id)
		builders = (dict([
			data.valid_ddex_builder(),
			data.valid_ddex_builder()
		]))

		subject.generate(builders.values())

		for upc in builders.keys():
			expected_path = path.join(expected_batch_path, upc, upc + ".xml")
			self.assertTrue(path.isfile(expected_path), expected_path + " does not exist")
		
class BatchGenerator:
	def __init__(self, root_folder, id_genereator=generate_batch_id):
		self._id_generator = id_genereator
		self._root_folder = root_folder

	def generate(self, builders):
		batch_path = path.join(self._root_folder, self._id_generator())
		for builder in builders:
			ddex = builder.build()
			product_path = path.join(batch_path, ddex.product_release_id())
			makedirs(product_path, exist_ok=True)
			ddex.write(path.join(product_path, ddex.product_release_id() + ".xml"))
