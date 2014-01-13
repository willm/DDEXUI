from DDEXUI.ddex.file_metadata import *
from mutagenx.mp3 import MP3
from PIL import Image
import hashlib
import os

class FileParser():

    def parse(self, file_path):
        hash = self.__get_hash(file_path)
        path = os.path.split(file_path)[1]
        extension = self.get_extension(file_path)

        if(extension == "MP3"):
            mp3 = MP3(file_path)
            return (AudioFileMetadata(self.__get_duration(mp3.info.length),
                self.__get_bitrate(mp3.info.bitrate),
                hash,
                path,
                extension))
        if(extension == "JPG"):
            img = Image.open(file_path)
            return ImageFileMetadata(hash, path, extension, img.size[0], img.size[1])

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

    @staticmethod
    def get_extension(file_path):
        return os.path.splitext(file_path)[1].replace(".","").upper()
