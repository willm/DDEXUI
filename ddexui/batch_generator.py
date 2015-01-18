import os
from os import path
from ddex import generate_batch_id

class BatchGenerator:
    def __init__(self, root_folder, batch_id):
        self._batch_id = batch_id
        self._root_folder = root_folder

    def generate(self, builders):
        batch_path = path.join(self._root_folder, self._batch_id)
        for builder in builders:
            ddex = builder.build()
            product_path = path.join(batch_path, builder.get_upc())
            # Could use exist_ok in python 3+ but not available in 27
            try: 
                os.makedirs(product_path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            ddex.write(path.join(product_path, builder.get_upc() + ".xml"))
