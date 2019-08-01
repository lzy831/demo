import struct
from icu_link_spec import *
from icu_debug import *
from icu_checksum import *

class LinkEAKPayload(object):
    def __init__(self, payload_bytes=None):
        self.mPayloadData = payload_bytes[0:-2:1]
        self.mPayloadChecksum = int(payload_bytes[-2::1].hex(), base=16)
        skdebug('LinkEAKPayload item count:', len(self.mPayloadData))

    def info_string(self):
        infostring = ' EAKP: '
        for i in range(0,len(self.mPayloadData)):
            infostring = infostring +'{:d} '.format(self.mPayloadData[i])
        return infostring
    
