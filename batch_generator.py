
from os import makedirs
from os import path
from DDEXUI.ddex.ddex import generate_batch_id

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
