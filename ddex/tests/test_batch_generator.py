import unittest
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.party import PartyType
from DDEXUI.ddex.release import *
from DDEXUI.ddex.deal import *
from DDEXUI.ddex.ddex import generate_batch_id
from datetime import datetime
from DDEXUI.ddex.party import Party
import random
from os import path
from tempfile import gettempdir
from shutil import rmtree
from os import makedirs

class BatchGeneratorTests(unittest.TestCase):
	def test_should_generate_a_batch_containing_each_product(self):
		static_batch_id = "batchID"
		root_folder = gettempdir()
		expected_batch_path = path.join(root_folder, static_batch_id)
		rmtree(expected_batch_path, ignore_errors=True)
		subject = BatchGenerator(root_folder, lambda: static_batch_id)
		builders = (dict([
			valid_builder(),
			valid_builder()
		]))

		subject.generate(builders.values())

		for upc in builders.keys():
			expected_path = path.join(expected_batch_path, upc, upc + ".xml")
			self.assertTrue(path.isfile(expected_path), expected_path + " does not exist")


def valid_builder():
	upc = str(random.randrange(100000000000, 9999999999999))
	return ((upc, DDEXBuilder().sender(Party("XD234241EW1", "Hospital Records", PartyType.MessageSender))
			.update(False)
			.recipient(Party("RDG2342424ES", "Bobs Records", PartyType.MessageSender))
			.add_release(ReleaseBuilder().title("Racing Green")
				.c_line("Copyright hospital records")
				.p_line("Published by Westbury Music")
				.year(2004)
				.reference("A0")
				.release_id(ReleaseIdType.Upc, upc)
				.release_type("Single")#ReleaseType.Single)	
				.artist("High Contrast")
				.label("Hospital Records")
				.parental_warning(False)
				.add_deal(Deal("PayAsYouGoModel", "PermanentDownload", "FR", datetime(2004, 9, 6)))
				.build()))
	)

		
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
