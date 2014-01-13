import xml.etree.cElementTree as ET
import datetime
from DDEXUI.ddex.message_header import MessageHeader
from DDEXUI.ddex.release import ReleaseIdType

def generate_batch_id(now=datetime.datetime.now):
    return now().strftime("%Y%m%d%H%M%S%f")[:-3]

class DDEX:

    def __init__(self, sender, recipient, releases=[], resources=[], update=False):
        self.update = update
        self.releases = releases
        self.resources = resources
        self.sender = sender
        self.recipient = recipient

    def write(self, file_name):
        root = ET.Element("ernm:NewReleaseMessage", {'MessageSchemaVersionId': 'ern/341', 'LanguageAndScriptCode': 'en', 'xs:schemaLocation': 'http://ddex.net/xml/ern/341 http://ddex.net/xml/ern/341/release-notification.xsd', 'xmlns:ernm': 'http://ddex.net/xml/ern/341', 'xmlns:xs':'http://www.w3.org/2001/XMLSchema-instance'})
        header = self.__write_message_header(root)
        root.append(header)
        
        update_indicator = ET.SubElement(root, "UpdateIndicator")
        if(self.update):
            update_indicator.text = "UpdateMessage"
        else:
            update_indicator.text = "OriginalMessage"

        resource_list = ET.SubElement(root, "ResourceList")
        for resource in self.resources:
            resource_list.append(resource.write())

        release_list = ET.SubElement(root, "ReleaseList")
        deal_list = ET.SubElement(root, "DealList")
        
        for release in self.releases:
            release_list.append(release.write())
            deal_list.append(release.write_deals())
        
        tree = ET.ElementTree(root)
        tree.write(file_name)
    
    def __write_message_header(self, root):
        return MessageHeader(self.sender, self.recipient).write();
