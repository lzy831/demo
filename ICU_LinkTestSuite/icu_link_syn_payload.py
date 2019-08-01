import struct
from icu_link_spec import *
from icu_debug import *
from icu_checksum import *

class LinkSynPayload(object):
    def __init__(self, payload_bytes=None, payload_dict=None):
        if payload_bytes:
            # skdebug('LinkSynPayload update_with_bytes')
            self.update_with_bytes(payload_bytes)
        elif payload_dict:
            # skdebug('LinkSynPayload update_with_dict')
            self.update_with_dict(payload_dict)
        else:
            skdebug('LinkSynPayload !!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            pass

    def update_with_dict(self, payload_dict: dict):
        self.mLinkVersion = payload_dict.get(LinkSpec.cHFeild_LV, 1)
        self.mMaxNumOfOutStdPkts = payload_dict.get(LinkSpec.cHFeild_MNOOSP, 0)
        self.mMaxRecvPktLen = payload_dict.get(LinkSpec.cHFeild_MRPL, 0)
        self.mRetransTimeout = payload_dict.get(LinkSpec.cHFeild_RT, 0)
        self.mCumAckTimeout = payload_dict.get(LinkSpec.cHFeild_CAT, 0)
        self.mMaxNumOfRetrans = payload_dict.get(LinkSpec.cHFeild_MNOR, 0)
        self.mMaxCumAck = payload_dict.get(LinkSpec.cHFeild_MCA, 0)
        data_without_checksum = struct.pack(LinkSpec.cLinkSynPayloadWithoutCheckssumFormat,
                                            self.mLinkVersion, self.mMaxNumOfOutStdPkts, self.mMaxRecvPktLen,
                                            self.mRetransTimeout, self.mCumAckTimeout, self.mMaxNumOfRetrans, self.mMaxCumAck)
        self.mPayloadChecksum = clac_checksum(data_without_checksum)
        # skdebug('data_without_checksum:', data_without_checksum)
        # skdebug('mPayloadChecksum:', hex(self.mPayloadChecksum))

    def update_with_bytes(self, payload_bytes: bytes):
        # skdebug('LinkSynPayload update_with_bytes', payload_bytes.hex())
        self.mPayloadTuple = LinkSpec.cLinkSynPayloadTupleType._make(struct.unpack(LinkSpec.cLinkSynPayloadFormat, payload_bytes))
        self.mLinkVersion = self.mPayloadTuple.LinkVersion
        self.mMaxNumOfOutStdPkts = self.mPayloadTuple.MaxNumOfOutStdPkts
        self.mMaxRecvPktLen = self.mPayloadTuple.MaxRecvPktLen
        self.mRetransTimeout = self.mPayloadTuple.RetransTimeout
        self.mCumAckTimeout = self.mPayloadTuple.CumAckTimeout
        self.mMaxNumOfRetrans = self.mPayloadTuple.MaxNumOfRetrans
        self.mMaxCumAck = self.mPayloadTuple.MaxCumAck
        self.mPayloadChecksum = self.mPayloadTuple.PayloadChecksum

    def to_bytes(self):
        return struct.pack(LinkSpec.cLinkSynPayloadFormat,
                           self.mLinkVersion, self.mMaxNumOfOutStdPkts, self.mMaxRecvPktLen,
                           self.mRetransTimeout, self.mCumAckTimeout, self.mMaxNumOfRetrans, self.mMaxCumAck, self.mPayloadChecksum)

    def info_string(self):
        return '\nLSP: {{LV: {:d}  MNOOSP: {:d}  MRPL: {:d}  RT: {:d}  CAT: {:d}  MNOR: {:d}  MAC: {:d}  PC: 0x{:04X}}}'.format(
            self.mLinkVersion, self.mMaxNumOfOutStdPkts, self.mMaxRecvPktLen, self.mRetransTimeout, self.mCumAckTimeout, self.mMaxNumOfRetrans, self.mMaxCumAck, self.mPayloadChecksum)
