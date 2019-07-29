#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import struct
from enum import Enum
from icu_link_spec import *
from icu_debug import *
from icu_checksum import *


class BadPktType(Enum):
    BAD_SOP = 0
    BAD_PL = 1
    BAD_PAN = 2
    OVER_MAX_LEN = 3


class TestPktType(Enum):
    TEST_START = 0
    TEST_STOP = 1
    TEST_DATA_NONAK = 2
    TEST_REQUEST_NONAK = 3


class LinkSynPayload(object):
    def __init__(self, payload_bytes=None, payload_dict=None):
        if payload_bytes:
            self.update_with_bytes(payload_bytes)
        elif payload_dict:
            self.update_with_dict(payload_dict)

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


class ControlByte(object):
    def __init__(self, cb_int=None, cb_dict=None):
        if cb_int != None:
            self.update_with_integer(cb_int)
        elif cb_dict != None:
            self.update_with_dict(cb_dict)

    def update_with_integer(self, cb_int: int):
        self.mValue = cb_int
        self.mSYN = (cb_int & 1 << LinkSpec.cBIT_SYN) >> LinkSpec.cBIT_SYN
        self.mACK = (cb_int & 1 << LinkSpec.cBIT_ACK) >> LinkSpec.cBIT_ACK
        self.mEAK = (cb_int & 1 << LinkSpec.cBIT_EAK) >> LinkSpec.cBIT_EAK
        self.mRST = (cb_int & 1 << LinkSpec.cBIT_RST) >> LinkSpec.cBIT_RST
        self.mNAK = (cb_int & 1 << LinkSpec.cBIT_NAK) >> LinkSpec.cBIT_NAK
        self.mRES2 = (cb_int & 1 << LinkSpec.cBIT_RES2) >> LinkSpec.cBIT_RES2
        self.mRES1 = (cb_int & 1 << LinkSpec.cBIT_RES1) >> LinkSpec.cBIT_RES1
        self.mRES0 = (cb_int & 1 << LinkSpec.cBIT_RES0) >> LinkSpec.cBIT_RES0

    def update_with_dict(self, cb_dict: dict):
        skdebug('ControlByte update with dict')
        skdebug(cb_dict)
        self.mValue = 0
        if cb_dict.get(LinkSpec.cHFeild_SYN, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_SYN)
        if cb_dict.get(LinkSpec.cHFeild_ACK, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_ACK)
        if cb_dict.get(LinkSpec.cHFeild_EAK, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_EAK)
        if cb_dict.get(LinkSpec.cHFeild_RST, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_RST)
        if cb_dict.get(LinkSpec.cHFeild_NAK, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_NAK)
        if cb_dict.get(LinkSpec.cHFeild_RES2, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_RES2)
        if cb_dict.get(LinkSpec.cHFeild_RES1, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_RES1)
        if cb_dict.get(LinkSpec.cHFeild_RES0, 0) == 1:
            self.mValue = self.mValue | (1 << LinkSpec.cBIT_RES0)


class LinkPacketHeader(object):

    def __init__(self, header_bytes=None, header_dict=None):
        # skdebug('LinkPacketHeader construct')
        if header_bytes != None:
            # skdebug('header_bytes exist')
            self.update_with_bytes(header_bytes)
        elif header_dict != None:
            # skdebug('header_dict exist')
            self.update_with_dict(header_dict)

    def update_with_bytes(self, header_bytes: bytes):
        # skdebug('LinkPacketHeader update with bytes')
        self.mHeaderTuple = LinkSpec.cLinkPacketHeaderTupleType._make(struct.unpack(LinkSpec.cLinkPacketHeaderFormat, header_bytes))
        self.mStartOfPacket = self.mHeaderTuple.StartOfPacket
        self.mPacketLength = self.mHeaderTuple.PacketLength
        # skdebug('mPacketLength:', self.mPacketLength)
        self.mControlByte = ControlByte(cb_int=self.mHeaderTuple.ControlByte)
        self.mPacketSeqNum = self.mHeaderTuple.PacketSeqNum
        self.mPacketAckNum = self.mHeaderTuple.PacketAckNum
        self.mSessionId = self.mHeaderTuple.SessionId
        self.mHeaderChecksum = self.mHeaderTuple.HeaderChecksum

    def update_with_dict(self, header_dict: dict):
        # skdebug('LinkPacketHeader update with dict')
        self.mStartOfPacket = header_dict.get(LinkSpec.cHFeild_SOP, 0xAA55)
        self.mPacketLength = header_dict.get(LinkSpec.cHFeild_PL, 0)
        # skdebug('mPacketLength:', self.mPacketLength)
        self.mControlByte = ControlByte(cb_dict=header_dict)
        # skdebug('ControlByte:', bin(self.mControlByte.mValue))
        self.mPacketSeqNum = header_dict.get(LinkSpec.cHFeild_PSN, 0)
        self.mPacketAckNum = header_dict.get(LinkSpec.cHFeild_PAN, 0)
        self.mSessionId = header_dict.get(LinkSpec.cHFeild_SI, 0)
        self.update_checksum()

    def update_packet_length(self, len):
        self.mPacketLength = len
        self.update_checksum()

    def update_checksum(self):
        data_without_checksum = struct.pack(LinkSpec.cLinkPacketHeaderWithoutChecksumFormat,
                                            self.mStartOfPacket, self.mPacketLength, self.mControlByte.mValue,
                                            self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId)
        self.mHeaderChecksum = clac_checksum(data_without_checksum)

    def is_valid(self):
        """验证包头有效性"""
        return True

    def info_string(self):
        header_info = '\nHeader: {{SOP: 0x{:04X}  PL: {:d}  '.format(self.mStartOfPacket, self.mPacketLength) +\
            'SYN: {:d}  ACK: {:d}  EAK: {:d}  RST: {:d}  '.format(self.mControlByte.mSYN, self.mControlByte.mACK, self.mControlByte.mEAK, self.mControlByte.mRST) +\
            'NAK: {:d}  RES2: {:d}  RES1: {:d}  RES0: {:d}  '.format(self.mControlByte.mNAK + self.mControlByte.mNAK, self.mControlByte.mRES2, self.mControlByte.mRES1, self.mControlByte.mRES0) +\
            'PSN: {:d}  PAN: {:d}  SI: {:d}  HC: 0x{:04X}}}'.format(self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)
        return header_info

    def to_bytes(self):
        # skdebug('to bytes')
        return struct.pack(LinkSpec.cLinkPacketHeaderFormat,
                           self.mStartOfPacket, self.mPacketLength, self.mControlByte.mValue,
                           self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)


class LinkPacket(object):

    def gen_test_start_payload():
        pdata = bytearray(b'\x00')
        pdata += (bytes('SPICU-LinkTest!', encoding='ASCII'))
        skdebug('payload_data:', pdata)
        skdebug('payload_data:', pdata.hex())
        res = clac_checksum(pdata)
        return pdata + res.to_bytes(length=2, byteorder='big', signed=False)

    def gen_random_payload(size=1):
        skdebug('gen_random_payload size:', size)
        data = bytes.fromhex('000102030405060708090A0B0C0D0E0F')
        whole_data = bytearray()
        for i in range(size):
            whole_data += data
        skdebug('whole_data len:', len(whole_data))
        res = clac_checksum(whole_data)
        # skdebug('res:', res)
        # skdebug('res:', hex(res))
        # skdebug('res type:', type(res))
        # skdebug('res.to_bytes():', res.to_bytes(length=2,byteorder='big',signed=False))
        # skdebug('res.to_bytes() type:', type(res.to_bytes(length=2,byteorder='big',signed=False)))
        return whole_data + res.to_bytes(length=2, byteorder='big', signed=False)

    def gen_test_request_data_payload(count=2, maxsize=32):
        pdata = struct.pack(LinkSpec.cLinkTestSession_RequestData_Format,
                            LinkSpec.cTestSession_CmdID_RequestData, count, maxsize)
        res = clac_checksum(pdata)
        return pdata + res.to_bytes(length=2, byteorder='big', signed=False)

    def gen_std_rst_packet():
        return LinkPacket(header_bytes=LinkPacketHeader(header_dict={LinkSpec.cHFeild_RST: 1}).to_bytes())

    def gen_random_eak_packet(param_dict: dict):
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_EAK: 1,
            LinkSpec.cHFeild_ACK: 1,
            LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN]})
        pl_bytes = LinkPacket.gen_random_payload()
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def gen_random_app_packet(param_dict: dict):
        random_si = random.randint(1, 10)
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_SI: random_si,
            LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]})
        pl_bytes = LinkPacket.gen_random_payload()
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def gen_nak_packet():
        header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_NAK: 1})
        pl_bytes = LinkPacket.gen_random_payload()
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def gen_ack_packet(param_dict: dict):
        return LinkPacket(header_bytes=LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_ACK: 1,
            LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN]}).to_bytes())

    def gen_syn_packet(param_dict: dict):
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_SYN: 1,
            LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]})
        payload = LinkSynPayload(payload_dict=param_dict)
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=payload.to_bytes())

    def gen_syn_ack_packet(param_dict: dict):
        skdebug('gen_syn_ack_packet param_dict:', param_dict)
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
            LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            LinkSpec.cHFeild_SYN: 1, LinkSpec.cHFeild_ACK: 1})
        payload = LinkSynPayload(payload_dict=param_dict)
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=payload.to_bytes())

    def gen_bad_packet(type, param_dict: dict = None):
        if type == BadPktType.BAD_SOP:
            skdebug('BAD_SOP')
            random_sop = random.randint(0, 65535)
            header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_SOP: random_sop})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.BAD_PL:
            skdebug('BAD_PL')
            random_pl = random.randint(256, 65535)
            # skdebug('random_pl:', random_pl)
            header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_PL: random_pl})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_pl=False)
        elif type == BadPktType.BAD_PAN:
            skdebug('BAD_PAN')
            random_pan = random.randint(0, 255)
            # skdebug('random_pan:', random_pan)
            header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_PAN: random_pan})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.OVER_MAX_LEN:
            skdebug('OVER_MAX_LEN')
            header = LinkPacketHeader(header_dict={})
            pl_bytes = LinkPacket.gen_random_payload(size=int(param_dict[LinkSpec.cHFeild_MRPL] * 2/16))
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def gen_test_packet(type, req_pkt_count=1, param_dict: dict = None):
        if type == TestPktType.TEST_START:
            skdebug('TEST_START')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: 0x09,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]})
            pl_bytes = LinkPacket.gen_test_start_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == TestPktType.TEST_DATA_NONAK:
            skdebug('TEST_DATA_NONAK')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: 0x09,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == TestPktType.TEST_REQUEST_NONAK:
            skdebug('TEST_REQUEST_NONAK')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: 0x09,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]})
            pl_bytes = LinkPacket.gen_test_request_data_payload(count=req_pkt_count)
            skdebug('pl_bytes:', pl_bytes.hex())
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def __init__(self, packet_bytes=None, header_bytes=None, payload_bytes=None, auto_update_pl=True):
        if auto_update_pl:
            self.mAutoUpdatePL = True
        else:
            self.mAutoUpdatePL = False
        if packet_bytes != None:
            self.update_packet_with_bytes(packet_bytes)
        elif header_bytes != None:
            self.update_header_with_bytes(header_bytes)
            if payload_bytes != None:
                skdebug('payload_bytes:', payload_bytes)
                self.update_payload_with_bytes(payload_bytes)
                self.update_packet_length(len(header_bytes)+len(payload_bytes))
            else:
                self.update_packet_length(len(header_bytes))

    def update_packet_length(self, pkt_len):
        if self.mAutoUpdatePL:
            self.mHeader.update_packet_length(pkt_len)

    def update_packet_with_bytes(self, packet_bytes: bytes):
        self.update_header_with_bytes(packet_bytes[:10])
        self.mPayloadBytes = packet_bytes[10:]
        self.mPayloadData = packet_bytes[10:-2]
        self.mPayloadChecksum = int(packet_bytes[-2::1].hex(), base=16)

    def update_header_with_bytes(self, header_bytes: bytes):
        self.mHeader = LinkPacketHeader(header_bytes=header_bytes)

    # def update_header_with_dict(self, header_dict):
    #     if self.mHeader == None:
    #         self.mHeader = LinkPacketHeader(header_dict=header_dict)
    #     else:
    #         self.mHeader.update_with_dict(header_dict=header_dict)

    def update_payload_with_bytes(self, payload_bytes: bytes):
        self.mPayloadBytes = payload_bytes
        self.mPayloadData = payload_bytes[0:-2:1]
        self.mPayloadChecksum = int(payload_bytes[-2::1].hex(), base=16)

    def info_string(self):
        if hasattr(self, "mPayloadData"):
            skdebug('mPayloadChecksum:', hex(self.mPayloadChecksum))
            if self.is_syn_packet() or self.is_syn_ack_packet():
                payload_info = LinkSynPayload(payload_bytes=self.mPayloadBytes).info_string()
            elif self.is_eak_packet():
                pass
            else:
                payload_info = ' PD: {}  PC: 0x{:04X}'.format(self.mPayloadData.hex(), self.mPayloadChecksum)
        else:
            payload_info = ''
        return self.mHeader.info_string()+payload_info

    # def prepare_to_send(self, psn=0):
    #     """ 发送之前,重新计算包长,更新PL,PSN, 更新HC (特定paylaod的bytes数据，应该是在创建时就计算好Checksum的) """
    #     pl = LinkSpec.cLinkPacketHeaderLength
    #     if hasattr(self, "mPayloadBytes"):
    #         pl += len(self.mPayloadBytes)
    #     self.mHeader.update_with_dict({LinkSpec.cHFeild_PSN: psn, LinkSpec.cHFeild_PL: pl})
    #     self.mHeader.update_checksum()

    def to_bytes(self):
        if hasattr(self, "mPayloadBytes"):
            return self.mHeader.to_bytes()+self.mPayloadBytes
        else:
            return self.mHeader.to_bytes()

    def is_syn_packet(self):
        if self.mHeader.mControlByte.mSYN == 1 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 0 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0:
            return True
        return False

    def is_syn_ack_packet(self):
        if self.mHeader.mControlByte.mSYN == 1 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0:
            return True
        return False

    def is_ack_packet(self):
        if self.mHeader.mControlByte.mSYN == 0 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mPacketSeqNum == 0:  # ACK包PSN必须为0
            return True
        return False

    def is_nonak_ack_packet(self):
        if self.mHeader.mControlByte.mSYN == 0 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0:
            return True
        return False

    def is_nonak_packet(self):
        if self.is_syn_packet() or self.is_syn_ack_packet() or self.is_nonak_ack_packet():
            return True
        elif self.is_ack_packet():
            return False
        elif self.mHeader.mControlByte.mNAK == 0:
            return True

    def is_eak_packet(self):
        return False


if __name__ == "__main__":
    print('test begin')
    # packet_bytes = bytes.fromhex('aa550016c0472d00024901040100019000160c0300bc')
    # # print(type(packet_bytes.hex()))
    # # print(packet_bytes.hex())
    # packet = LinkPacket(packet_bytes=packet_bytes)

    # # print(type(packet.mHeaderChecksum))
    # # print('mPayloadData: {}'.format(packet.mPayloadData.hex()))
    # print(packet.info_string())
    # print('cLinkPacketHeaderField: ', LinkSpec.cLinkPacketHeaderField)

    # rst_pkt = LinkPacket.gen_std_rst_packet()
    # print('rst_pkt info: ', rst_pkt.info_string())
    # print('rst_pkt bytes: ', rst_pkt.to_bytes())
    # print('rst_pkt bytes: ', rst_pkt.to_bytes().hex())

    payload_bytes = LinkPacket.gen_random_payload()
    skdebug('payload_bytes:', payload_bytes)
    skdebug('payload_bytes:', payload_bytes.hex())
    print('test end')
