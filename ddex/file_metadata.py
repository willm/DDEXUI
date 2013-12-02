class FileMetadata:
	def __init__(self, md5, name, extension):
		self.md5 = md5
		self.name = name
		self.extension = extension
		
class ImageFileMetadata:
	def __init__(self, md5, name, extension, width, height):
		FileMetadata.__init__(self, md5, name, extension)
		self.width = width
		self.height = height
		self.codec = "JPEG"

class AudioFileMetadata(FileMetadata):
	def __init__(self, duration, bit_rate, md5, name, extension):
		FileMetadata.__init__(self, md5, name, extension)
		self.duration = duration
		self.bit_rate = bit_rate
		self.codec = "MP3"
