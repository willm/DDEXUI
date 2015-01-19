import xml.etree.cElementTree as ET
from abc import ABCMeta, abstractmethod


class Resource:

    __metaclass__ = ABCMeta

    def __init__(self, technical_resource_details_reference, id_attrs={}):
        self._id_attrs = id_attrs
        self._technical_resource_details_reference = technical_resource_details_reference

    @abstractmethod
    def write(self):
        resource = ET.Element(self.kind())
        self._append_element_with_text(resource, self.kind()+"Type", self.type())
        resource_id = self._append_element_with_text(resource, self.kind()+"Id")
        self._append_element_with_text(resource_id, self.id_type(), self.id_value(), self._id_attrs)
        self._append_element_with_text(resource, "ResourceReference", self.resource_reference())
        return resource

    @abstractmethod
    def _append_technical_details(self, resource, technical_resource_details_reference):
        details_by_territory = self._append_element_with_text(resource, self.kind()+"DetailsByTerritory")
        self._append_element_with_text(details_by_territory, "TerritoryCode", "Worldwide")
        technical_details = ET.SubElement(details_by_territory, "Technical"+self.kind()+"Details")
        self._append_element_with_text(technical_details, "TechnicalResourceDetailsReference", technical_resource_details_reference)
        return technical_details

    def _append_file(self, technical_details, file_metadata):
        file_element = ET.SubElement(technical_details, "File")
        self._append_element_with_text(file_element, "FileName", file_metadata.name)
        hash_sum = ET.SubElement(file_element, "HashSum")
        self._append_element_with_text(hash_sum, "HashSum", file_metadata.md5)
        self._append_element_with_text(hash_sum, "HashSumAlgorithmType", "MD5")
        
    @property
    @abstractmethod
    def kind(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def id_type(self):
        pass

    @property
    @abstractmethod
    def id_value(self):
        pass

    @property
    @abstractmethod
    def resource_reference(self):
        pass

    @property
    def technical_resource_details_reference(self):
        return self._technical_resource_details_reference

    def _append_element_with_text(self, parent, name, text="", attrs={}):
        el = ET.SubElement(parent, name, attrs)
        el.text = text
        return el


class Image(Resource):
    def __init__(self, resource_reference, id_value, file_metadata, technical_resource_details_reference):
        Resource.__init__(self, technical_resource_details_reference, {"Namespace": "DDEXUI"})
        self.__resource_reference = resource_reference
        self.__id_value = id_value
        self.file_metadata = file_metadata

    def write(self):
        resource = super(Image, self).write()
        self._append_technical_details(resource)
        return resource

    def _append_technical_details(self, resource):
        technical_details = super(Image, self)._append_technical_details(resource, self._technical_resource_details_reference)
        self._append_element_with_text(technical_details, "ImageCodecType", self.file_metadata.codec)
        self._append_element_with_text(technical_details, "ImageHeight", str(self.file_metadata.height))
        self._append_element_with_text(technical_details, "ImageWidth", str(self.file_metadata.width))
        self._append_file(technical_details, self.file_metadata)        

    def kind(self):
        return "Image"

    def type(self):
        return "FrontCoverImage"
    
    def id_value(self):
        return self.__id_value
    
    def id_type(self):
        return "ProprietaryId"
    
    def resource_reference(self):
        return self.__resource_reference

class SoundRecording(Resource):
    def __init__(self, resource_reference, isrc, title, file_metadata, technical_resource_details_reference):
        Resource.__init__(self, technical_resource_details_reference)
        self.title = title
        self.__resource_reference = resource_reference
        self.isrc = isrc
        self.file_metadata = file_metadata

    def write(self):
        sound_recording = super(SoundRecording, self).write()
        title = self._append_element_with_text(sound_recording, "ReferenceTitle")
        self._append_element_with_text(title, "TitleText", self.title)

        self._append_element_with_text(sound_recording, "Duration", self.file_metadata.duration)

        self._append_technical_details(sound_recording)
        return sound_recording

    def _append_technical_details(self, resource):
        technical_details = super(SoundRecording, self)._append_technical_details(resource, self._technical_resource_details_reference)
        self._append_element_with_text(technical_details, "AudioCodecType", self.file_metadata.codec)
        self._append_file(technical_details, self.file_metadata)
    
    def kind(self):
        return "SoundRecording"

    def type(self):
        return "MusicalWorkSoundRecording"
    
    def id_value(self):
        return self.isrc
    
    def id_type(self):
        return "ISRC"
    
    def resource_reference(self):
        return self.__resource_reference
