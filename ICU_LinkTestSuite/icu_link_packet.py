#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
from collections import namedtuple
from icu_debug import *
from icu_checksum import *


class LinkSpec(object):
    cBIT_SYN = 7
    cBIT_ACK = 6
    cBIT_EAK = 5
    cBIT_RST = 4
    cBIT_NAK = 3
    cBIT_RES2 = 2
    cBIT_RES1 = 1
    cBIT_RES0 = 0

    cHFeild_SOP = 'StartOfPacket'
    cHFeild_PL = 'PacketLength'
    cHFeild_CB = 'ControlByte'
    cHFeild_SYN = 'SYN'
    cHFeild_ACK = 'ACK'
    cHFeild_EAK = 'EAK'
    cHFeild_RST = 'RST'
    cHFeild_NAK = 'NAK'
    cHFeild_RES2 = 'RES2'
    cHFeild_RES1 = 'RES1'
    cHFeild_RES0 = 'RES0'
    cHFeild_PSN = 'PacketSeqNum'
    cHFeild_PAN = 'PacketAckNum'
    cHFeild_SI = 'SessionId'
    cHFeild_HC = 'HeaderChecksum'

    cLinkPacketSYNLength = 2
    cLinkPacketHeaderLength = 10
    cLinkPacketHeaderFormat = '>HHBBBBH'
    cLinkPacketHeaderWithoutChecksumFormat = '>HHBBBB'
    # cLinkPacketHeaderField = 'StartOfPacket, PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId, HeaderChecksum'
    cLinkPacketHeaderField = cHFeild_SOP+' '+cHFeild_PL+' '+cHFeild_CB+' '+cHFeild_PSN+' '+cHFeild_PAN+' '+cHFeild_SI+' '+cHFeild_HC
    cLinkPacketHeaderTupleType = namedtuple('LinkPacketHeaderTuple', cLinkPacketHeaderField)

    cHFeild_LV = 'LinkVersion'
    cHFeild_MNOOSP = 'MaxNumOfOutStdPkts'
    cHFeild_MRPL = 'MaxRecvPktLen'
    cHFeild_RT = 'RetransTimeout'
    cHFeild_CAT = 'CumAckTimeout'
    cHFeild_MNOR = 'MaxNumOfRetrans'
    cHFeild_MCA = 'MaxCumAck'
    cHFeild_PC = 'PayloadChecksum'
    cLinkSynPayloadLength = 12
    cLinkSynPayloadFormat = '>BBHHHBBH'
    cLinkSynPayloadWithoutCheckssumFormat = '>BBHHHBB'
    cLinkSynPayloadField = cHFeild_LV+' '+cHFeild_MNOOSP+' '+cHFeild_MRPL+' '+cHFeild_RT+' '+cHFeild_CAT+' '+cHFeild_MNOR+' '+cHFeild_MCA+' '+cHFeild_PC
    cLinkSynPayloadTupleType = namedtuple('LinkSynPayloadTuple', cLinkSynPayloadField)


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
        skdebug('data_without_checksum:', data_without_checksum)
        skdebug('mPayloadChecksum:', hex(self.mPayloadChecksum))

    def update_with_bytes(self, payload_bytes: bytes):
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
        skdebug('LinkPacketHeader construct')
        if header_bytes != None:
            skdebug('header_bytes exist')
            self.update_with_bytes(header_bytes)
        elif header_dict != None:
            skdebug('header_dict exist')
            self.update_with_dict(header_dict)

    def update_with_bytes(self, header_bytes: bytes):
        self.mHeaderTuple = LinkSpec.cLinkPacketHeaderTupleType._make(struct.unpack(LinkSpec.cLinkPacketHeaderFormat, header_bytes))
        self.mStartOfPacket = self.mHeaderTuple.StartOfPacket
        self.mPacketLength = self.mHeaderTuple.PacketLength
        self.mControlByte = ControlByte(cb_int=self.mHeaderTuple.ControlByte)
        self.mPacketSeqNum = self.mHeaderTuple.PacketSeqNum
        self.mPacketAckNum = self.mHeaderTuple.PacketAckNum
        self.mSessionId = self.mHeaderTuple.SessionId
        self.mHeaderChecksum = self.mHeaderTuple.HeaderChecksum

    def update_with_dict(self, header_dict: dict):
        skdebug('update with dict')
        self.mStartOfPacket = header_dict.get(LinkSpec.cHFeild_SOP, 0xAA55)
        self.mPacketLength = header_dict.get(LinkSpec.cHFeild_PL, 0)
        self.mControlByte = ControlByte(cb_dict=header_dict)
        skdebug('ControlByte:', bin(self.mControlByte.mValue))
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
        header_info = 'SOP: 0x{:04X}  PL: {:d}  '.format(self.mStartOfPacket, self.mPacketLength) +\
            'SYN: {:d}  ACK: {:d}  EAK: {:d}  RST: {:d}  '.format(self.mControlByte.mSYN, self.mControlByte.mACK, self.mControlByte.mEAK, self.mControlByte.mRST) +\
            'NAK: {:d}  RES2: {:d}  RES1: {:d}  RES0: {:d}  '.format(self.mControlByte.mNAK + self.mControlByte.mNAK, self.mControlByte.mRES2, self.mControlByte.mRES1, self.mControlByte.mRES0) +\
            'PSN: {:d}  PAN: {:d}  SI: {:d}  HC: 0x{:04X} '.format(self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)
        return header_info

    def to_bytes(self):
        # skdebug('to bytes')
        return struct.pack(LinkSpec.cLinkPacketHeaderFormat,
                           self.mStartOfPacket, self.mPacketLength, self.mControlByte.mValue,
                           self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)


class LinkPacket(object):

    def gen_std_rst_packet():
        return LinkPacket(header_bytes=LinkPacketHeader(header_dict={LinkSpec.cHFeild_RST: 1}).to_bytes())

    def gen_syn_ack_packet(param_dict: dict):
        header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
                                               LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                                               LinkSpec.cHFeild_SYN: 1, LinkSpec.cHFeild_ACK: 1})
        payload = LinkSynPayload(payload_dict=param_dict)
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=payload.to_bytes())

    def __init__(self, packet_bytes=None, header_bytes=None, payload_bytes=None):
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
            payload_info = 'PD: {}  PC: 0x{:04X}'.format(self.mPayloadData.hex(), self.mPayloadChecksum)
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
                self.mHeader.mControlByte.mRST == 0:
            return True
        return False


if __name__ == "__main__":
    print('test begin')
    packet_bytes = bytes.fromhex('aa550016c0472d00024901040100019000160c0300bc')
    # print(type(packet_bytes.hex()))
    # print(packet_bytes.hex())
    packet = LinkPacket(packet_bytes=packet_bytes)

    # print(type(packet.mHeaderChecksum))
    # print('mPayloadData: {}'.format(packet.mPayloadData.hex()))
    print(packet.info_string())
    print('cLinkPacketHeaderField: ', LinkSpec.cLinkPacketHeaderField)

    rst_pkt = LinkPacket.gen_std_rst_packet()
    print('rst_pkt info: ', rst_pkt.info_string())
    print('rst_pkt bytes: ', rst_pkt.to_bytes())
    print('rst_pkt bytes: ', rst_pkt.to_bytes().hex())

    print('test end')
