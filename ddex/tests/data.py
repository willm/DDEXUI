import random
from DDEXUI.ddex.ddex_builder import DDEXBuilder
from DDEXUI.ddex.release_builder import ReleaseBuilder
from DDEXUI.ddex.party import Party, PartyType
from DDEXUI.ddex.release import *
from DDEXUI.ddex.deal import *
from datetime import datetime


def valid_ddex_builder():
    upc = str(random.randrange(100000000000, 9999999999999))
    return (DDEXBuilder().sender(Party("XD234241EW1", "Hospital Records", PartyType.MessageSender))
            .update(False)
            .recipient(Party("RDG2342424ES", "Bobs Records", PartyType.MessageSender))
            .add_release(valid_product_release(upc)))
    

def valid_product_release(upc):
    return (ReleaseBuilder().title("Racing Green")
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
                .build())

def valid_track_release(isrc):
    return (ReleaseBuilder().title("Racing Green")
                .c_line("Copyright hospital records")
                .p_line("Published by Westbury Music")
                .year(2004)
                .reference("A0")
                .release_id(ReleaseIdType.Isrc, isrc)
                .release_type("Track")
                .artist("High Contrast")
                .label("Hospital Records")
                .parental_warning(False)
                .add_deal(Deal("PayAsYouGoModel", "PermanentDownload", "FR", datetime(2004, 9, 6)))
                .build())
