from os import makedirs
from os import path
from DDEXUI.ddex.ddex import generate_batch_id

class BatchGenerator:
	def __init__(self, root_folder, batch_id):
		self._batch_id = batch_id
		self._root_folder = root_folder

	def generate(self, builders):
		batch_path = path.join(self._root_folder, self._batch_id)
		for builder in builders:
			ddex = builder.build()
			product_path = path.join(batch_path, builder.get_upc())
			makedirs(product_path, exist_ok=True)
			ddex.write(path.join(product_path, builder.get_upc() + ".xml"))
