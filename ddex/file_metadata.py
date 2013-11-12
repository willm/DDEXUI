from mutagenx.mp3 import MP3
import hashlib
import os

class FileParser():

	def parse(self, file_path):
		mp3 = MP3(file_path)
		return (FileMetadata(self.__get_duration(mp3.info.length),
			self.__get_bitrate(mp3.info.bitrate),
			self.__get_hash(file_path),
			os.path.split(file_path)[1],
			self.__get_extension(file_path)))

	def __get_duration(self, total_seconds):
		minutes = int(total_seconds / 60)
		seconds = int(total_seconds % 60)
		return "PT" + str(minutes) + "M" + str(seconds) + ".000S"

	def __get_bitrate(self, bit_rate):
		return int(bit_rate / 1000)

	def __get_hash(self, file_path):
		hash = hashlib.md5()
		with open(file_path, 'rb') as resource:
			hash.update(resource.read())
		return hash.hexdigest()

	def __get_extension(self, file_path):
		return os.path.splitext(file_path)[1].replace(".","").upper()
		

class FileMetadata:
	def __init__(self, duration, bit_rate, md5, name, extension):
		self.duration = duration
		self.bit_rate = bit_rate
		self.codec = "MP3"
		self.md5 = md5
		self.name = name
		self.extension = extension
