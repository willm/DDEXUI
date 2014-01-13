from DDEXUI.ddex.ddex_builder import DDEXBuilder

class ProductService:
    def __init__(self, product_release_builder, upc, coverart_path, track_builder_file_paths, is_update, resource_manager):
        self._product_release_builder = product_release_builder
        self.upc = upc
        self.coverart_path = coverart_path
        self.track_builder_file_paths = track_builder_file_paths
        self.is_update = is_update  
        self._resource_manager = resource_manager
        self.ddex_builder = DDEXBuilder()
        self.ddex_builder.update(self.is_update)

    def _add_image(self, upc):
        if(self.coverart_path != None):
            image = self._resource_manager.add_image(upc, self.coverart_path, "A0", "T0")
            self._product_release_builder.add_resource(image.resource_reference())
            self.ddex_builder.add_resource(image)

    def _add_audio_resources(self, upc, file_paths, builder):
        for path in file_paths:
            resource = self._resource_manager.add_sound_recording(upc, path, builder.get_isrc(), builder.get_title(), "A"+str(self.resource_count), "T"+str(self.resource_count))
            self.resource_count += 1
            builder.add_resource(resource.resource_reference())
            self._product_release_builder.add_resource(resource.resource_reference())
            self.ddex_builder.add_resource(resource)

    def create_ddex(self):
        self._add_image(self.upc)
        count = 1
        self.resource_count = 1
        for track in self.track_builder_file_paths:
            self._add_audio_resources(self.upc, track.paths, track.builder)
            self.ddex_builder.add_release(track.builder.reference("R" + str(count)).build())
            count += 1
        self.ddex_builder.add_release(self._product_release_builder.build())
        return self.ddex_builder
