import struct
from icu_link_spec import *
from icu_debug import *
from icu_checksum import *


class LinkEAKPayload(object):
    def __init__(self, pan=0, payload_bytes=None, psn_list=None):
        self.mPAN = pan
        if payload_bytes:
            self.mPayloadDataBytes = payload_bytes
            self.mPayloadData = payload_bytes[0:-2:1]
            self.mPayloadChecksum = int(payload_bytes[-2::1].hex(), base=16)
            skdebug('LinkEAKPayload item count:', len(self.mPayloadData))
        elif psn_list:
            if len(psn_list) > 0:
                payload = bytearray()
                skdebug('payload:', payload.hex())
                for psn in psn_list:
                    skdebug('psn:', psn)
                    payload.append(psn)
                skdebug('payload:', payload.hex())
                self.mPayloadData = payload
                # skdebug('payload:', self.mPayloadData.hex())
                self.mPayloadChecksum = clac_checksum(self.mPayloadData)
                skdebug('checksum:',self.mPayloadChecksum)
                self.mPayloadDataBytes = self.mPayloadData + struct.pack('>H',self.mPayloadChecksum)

    def to_bytes(self):
        return self.mPayloadDataBytes

    def get_missing_psn_list(self):
        pan = self.mPAN
        skdebug('pan:', pan)
        first_eak_psn = self.mPayloadData[0]
        skdebug('first_eak_psn:', first_eak_psn)
        res = []
        if pan < first_eak_psn:
            for i in range(pan+1, first_eak_psn):
                res.append(i)
        elif pan > first_eak_psn:
            for i in range(pan+1, first_eak_psn+255):
                res.append(i % 256)
        return res

    def info_string(self):
        infostring = ' EAKP: '
        for i in range(0, len(self.mPayloadData)):
            infostring = infostring + '{:d} '.format(self.mPayloadData[i])
        return infostring
