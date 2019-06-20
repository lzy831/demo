#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
from collections import namedtuple
from icu_debug import *
# from icu_serial import *


class LinkSpec(object):

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
    cBIT_SYN = 7
    cBIT_ACK = 6
    cBIT_EAK = 5
    cBIT_RST = 4
    cBIT_NAK = 3
    cBIT_RES2 = 2
    cBIT_RES1 = 1
    cBIT_RES0 = 0


class LinkSynPayload(object):
    def __init__(self):
        pass

    def update_with_dict(**syn_dict):
        pass

    def to_bytes(self):
        pass


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
            skdebug(LinkSpec.cHFeild_RST+' exist')
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
        self.mStartOfPacket = header_dict.get('StartOfPacket', 0xAA55)
        self.mPacketLength = header_dict.get('PacketLength', 0)
        self.mControlByte = ControlByte(cb_dict=header_dict)
        skdebug('ControlByte:', bin(self.mControlByte.mValue))
        self.mPacketSeqNum = header_dict.get('PacketSeqNum', 0)
        self.mPacketAckNum = header_dict.get('PacketAckNum', 0)
        self.mSessionId = header_dict.get('SessionId', 0)
        self.mHeaderChecksum = header_dict.get('HeaderChecksum', 0)

        # data_without_checksum = struct.pack(LinkPacketHeaderWithoutChecksumFormat, StartOfPacket,
        #                                     PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId)
        # checksum = clac_checksum(data_without_checksum)

    def to_bytes(self):
        skdebug('to bytes')
        return struct.pack(LinkSpec.cLinkPacketHeaderFormat,
                            self.mStartOfPacket, self.mPacketLength, self.mControlByte.mValue,
                            self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)



class LinkPacket(object):

    def gen_std_rst_packet():
        header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_RST: 1})
        return LinkPacket(header_bytes=header.to_bytes())

    def __init__(self, packet_bytes=None, header_bytes=None, payload_bytes=None):
        if packet_bytes != None:
            self.update_packet_with_bytes(packet_bytes)
        elif header_bytes != None:
            self.update_header_with_bytes(header_bytes)
            if payload_bytes != None:
                self.update_payload_with_bytes(payload_bytes)

    def update_packet_with_bytes(self, packet_bytes: bytes):
        self.update_header_with_bytes(packet_bytes[:10])
        self.mPayloadBytes = packet_bytes[10:]
        self.mPayloadData = packet_bytes[10:-3]
        self.mPayloadChecksum = int(packet_bytes[-2:-1].hex())

    def update_header_with_bytes(self, header_bytes: bytes):
        self.mHeaderBytes = header_bytes
        self.mHeader = LinkPacketHeader(header_bytes=header_bytes)

    def update_header_with_dict(self, header_dict):
        if self.mHeader == None:
            self.mHeader = LinkPacketHeader(header_dict=header_dict)
        else:
            self.mHeader.update_with_dict(header_dict=header_dict)
        self.mHeaderBytes = self.mHeader.to_bytes()

    def update_payload_with_bytes(payload_bytes: bytes):
        self.mPayloadBytes = payload_bytes
        self.mPayloadData = payload_bytes[0:-2:1]
        self.mPayloadChecksum = int(packet_bytes[-2:-1].hex())

    def info_string(self):
        if hasattr(self,"mPayloadData"):
            payload_info = 'PD: {}  PC: 0x{:04X}'.format(self.mPayloadData.hex(), self.mPayloadChecksum)
        else:
            payload_info=''
        header_info = 'SOP: 0x{:04X}  PL: {:d}  '.format(self.mHeader.mStartOfPacket, self.mHeader.mPacketLength) +\
            'SYN: {:d}  ACK: {:d}  EAK: {:d}  RST: {:d}  '.format(self.mHeader.mControlByte.mSYN, self.mHeader.mControlByte.mACK, self.mHeader.mControlByte.mEAK, self.mHeader.mControlByte.mRST) +\
            'NAK: {:d}  RES2: {:d}  RES1: {:d}  RES0: {:d}  '.format(self.mHeader.mControlByte.mNAK + self.mHeader.mControlByte.mNAK, self.mHeader.mControlByte.mRES2, self.mHeader.mControlByte.mRES1, self.mHeader.mControlByte.mRES0) +\
            'PSN: {:d}  PAN: {:d}  SI: {:d}  HC: 0x{:04X}\n'.format(self.mHeader.mPacketSeqNum, self.mHeader.mPacketAckNum, self.mHeader.mSessionId, self.mHeader.mHeaderChecksum)
        return header_info+payload_info

    def to_bytes(self):
        if hasattr(self,"mPayloadBytes"):
            return self.mHeaderBytes+self.mPayloadBytes
        else:
            return self.mHeaderBytes


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


BIT_SYN = 7
BIT_ACK = 6
BIT_EAK = 5
BIT_RST = 4
BIT_NAK = 3
BIT_RES2 = 2
BIT_RES1 = 1
BIT_RES0 = 0
LINK_PKT_MAX_PSN = 255


LinkPacketSYNLength = 2
LinkPacketHeaderLength = 10
LinkPacketHeaderFormat = '>HHBBBBH'
LinkPacketHeaderWithoutChecksumFormat = '>HHBBBB'
LinkPacketHeaderField = 'StartOfPacket, PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId, HeaderChecksum'
LinkPacketHeaderTupleType = namedtuple(
    'LinkPacketHeaderTuple', LinkPacketHeaderField)

LinkSynPayloadLength = 12
LinkSynPayloadFormat = '>BBHHHBBH'
LinkSynPayloadWithoutCheckssumFormat = '>BBHHHBB'
LinkSynPayloadField = 'LinkVersion, MaxNumOfOutStdPkts, MaxRecvPktLen, RetransTimeout, CumAckTimeout, MaxNumOfRetrans, MaxCumAck, PayloadChecksum'
LinkSynPayloadTupleType = namedtuple(
    'LinkSynPayloadTuple', LinkSynPayloadField)

Valid_SYN_Header_Param = dict(
    SYN=1, ACK=0, EAK=0, RST=0, NAK=0, RES1=0, RES2=0, RES3=0,
    PacketLength=LinkPacketHeaderLength+LinkSynPayloadLength)
Valid_RST_Header_param = dict(
    SYN=0, ACK=0, EAK=0, RST=1, NAK=0, RES1=0, RES2=0, RES3=0,
    PacketLength=LinkPacketHeaderLength)
Valid_ACK_Header_Param = dict(
    ACK=1, EAK=0, RST=0, NAK=0, RES1=0, RES2=0, RES3=0,)


MCU_Default_SYN_Param = dict()
MCU_Negotiated_SYN_Param = dict()


def is_valid_packet_header(header_data: bytes):
    return True


def is_valid_syn_or_syn_ack_packet(header: LinkPacketHeaderTupleType):
    # skdebug('header.ControlByte:', bin(header.ControlByte))
    # skdebug('1<<BIT_SYN:', bin(1 << BIT_SYN))
    return header.ControlByte == 1 << BIT_SYN or header.ControlByte == (1 << BIT_SYN | 1 << BIT_ACK)


def is_reset_packet(packet: bytes):
    header_bytes = packet[:10]
    debug_header(header_bytes)
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_bytes))
    return header.ControlByte == 1 << BIT_RST


def get_syn_param(payload_bytes: bytes):
    skdebug('payload_bytes len:', len(payload_bytes))
    payload = LinkSynPayloadTupleType._make(
        struct.unpack(LinkSynPayloadFormat, payload_bytes))
    syn_param = dict(
        LinkVersion=payload.LinkVersion,
        MaxNumOfOutStdPkts=payload.MaxNumOfOutStdPkts,
        MaxRecvPktLen=payload.MaxRecvPktLen,
        RetransTimeout=payload.RetransTimeout,
        CumAckTimeout=payload.CumAckTimeout,
        MaxNumOfRetrans=payload.MaxNumOfRetrans,
        MaxCumAck=payload.MaxCumAck)
    return syn_param


def get_packet_param(packet: bytes):
    header_bytes = packet[:10]
    skdebug('header_bytes len:', len(header_bytes))
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_bytes))
    header_param = dict(PacketLength=header.PacketLength,
                        SYN=(header.ControlByte & 1 << BIT_SYN) >> BIT_SYN,
                        ACK=(header.ControlByte & 1 << BIT_ACK) >> BIT_ACK,
                        EAK=(header.ControlByte & 1 << BIT_EAK) >> BIT_EAK,
                        RST=(header.ControlByte & 1 << BIT_RST) >> BIT_RST,
                        NAK=(header.ControlByte & 1 << BIT_NAK) >> BIT_NAK,
                        PacketSeqNum=header.PacketSeqNum,
                        PacketAckNum=header.PacketAckNum,
                        SessionId=header.SessionId)
    skdebug(header_param)
    if is_valid_syn_or_syn_ack_packet(header):
        # skdebug('is valid syn packet')
        syn_payload_param = get_syn_param(packet[10:])
        return {**header_param, **syn_payload_param}
    else:
        skdebug('is not valid syn packet')
        return header_param


def get_payload_len_from_header(header_data: bytes):
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_data))
    return header.PacketLength-LinkPacketHeaderLength


def debug_header(header_data: bytes):
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_data))

    # print(header)
    skdebug(header)
    skdebug("ControlByte:", bin(header.ControlByte))

    # skdebug("StartOfPacket:", hex(header.StartOfPacket))
    # skdebug("PacketLength:", header.PacketLength)
    # skdebug("ControlByte:", format(header.ControlByte, 'b'))
    # skdebug("PacketSeqNum:", header.PacketSeqNum)
    # skdebug("PacketAckNum:", header.PacketAckNum)
    # skdebug("SessionId:", header.SessionId)
    # skdebug("HeaderChecksum:", hex(header.HeaderChecksum))


def debug_syn_payload(payload_data: bytes):
    skdebug('payload_data len', len(payload_data))
    payload = LinkSynPayloadTupleType._make(
        struct.unpack(LinkSynPayloadFormat, payload_data))
    skdebug(payload)


def clac_checksum(data_without_checksum: bytes):
    skdebug('clac_checksum begin, data:', data_without_checksum.hex())
    checksum = 0
    for value in data_without_checksum:
        checksum = checksum + value
        # skdebug('checksum', hex(checksum), 'value', value)
    return checksum


def generate_syn_payload_with_param(**param):
    skdebug('generate_syn_payload_with_param')
    skdebug('param:', param)
    # for name, value in param.items():
    #     skdebug('name:', name, 'value:', value)
    LinkVersion = int(param.get('LinkVersion', 0x1))
    MaxNumOfOutStdPkts = int(param.get('MaxNumOfOutStdPkts', 0))
    MaxRecvPktLen = int(param.get('MaxRecvPktLen', 0))
    RetransTimeout = int(param.get('RetransTimeout', 0))
    CumAckTimeout = int(param.get('CumAckTimeout', 0))
    MaxNumOfRetrans = int(param.get('MaxNumOfRetrans', 0))
    MaxCumAck = int(param.get('MaxCumAck', 0))

    # calc payload checksum
    data_without_checksum = struct.pack(LinkSynPayloadWithoutCheckssumFormat, LinkVersion, MaxNumOfOutStdPkts,
                                        MaxRecvPktLen, RetransTimeout, CumAckTimeout, MaxNumOfRetrans, MaxCumAck)
    checksum = clac_checksum(data_without_checksum)
    PayloadChecksum = int(param.get('PayloadChecksum', checksum))
    return struct.pack(
        LinkSynPayloadFormat, LinkVersion, MaxNumOfOutStdPkts, MaxRecvPktLen, RetransTimeout, CumAckTimeout,
        MaxNumOfRetrans, MaxCumAck, PayloadChecksum)


def generate_standard_SYN_ACK_packet(**param):
    global MCU_Default_SYN_Param
    syn_ack_param = dict()
    syn_ack_param['MaxNumOfOutStdPkts'] = int(MCU_Default_SYN_Param.get('MaxNumOfOutStdPkts', 4))
    syn_ack_param['MaxRecvPktLen'] = int(MCU_Default_SYN_Param.get('MaxRecvPktLen', 256))
    syn_ack_param['RetransTimeout'] = int(MCU_Default_SYN_Param.get('RetransTimeout', 400))
    syn_ack_param['CumAckTimeout'] = int(param.get('CumAckTimeout', 22))
    syn_ack_param['MaxNumOfRetrans'] = int(param.get('MaxNumOfRetrans', 10))
    syn_ack_param['MaxCumAck'] = int(param.get('MaxCumAck', 10))
    payload = generate_syn_payload_with_param(**syn_ack_param)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, ACK=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = int(param.get('PacketSeqNum', 0))
    header_param['PacketAckNum'] = int(param.get('PacketAckNum', 0))
    header = generate_header_with_param(**header_param)
    packet = header+payload
    return packet


def generate_negotiated_SYN_ACK_packet(**param):
    global MCU_Default_SYN_Param
    syn_ack_param = dict()
    syn_ack_param['MaxNumOfOutStdPkts'] = int(MCU_Default_SYN_Param.get('MaxNumOfOutStdPkts', 4))
    syn_ack_param['MaxRecvPktLen'] = int(MCU_Default_SYN_Param.get('MaxRecvPktLen', 256))
    syn_ack_param['RetransTimeout'] = int(MCU_Default_SYN_Param.get('RetransTimeout', 400))
    syn_ack_param['CumAckTimeout'] = int(param.get('CumAckTimeout', 22))
    # 修改可协商参数MaxNumOfRetrans值用以到达再次协商的目的
    # syn_ack_param['MaxNumOfRetrans'] = int(param.get('MaxNumOfRetrans', 10)) # + int(2)
    syn_ack_param['MaxCumAck'] = int(param.get('MaxCumAck', 10))
    payload = generate_syn_payload_with_param(**syn_ack_param)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, ACK=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = int(param.get('PacketSeqNum', 0))
    header_param['PacketAckNum'] = int(param.get('PacketSeqNum', 0))
    header = generate_header_with_param(**header_param)
    packet = header+payload
    return packet


def generate_nak_payload_with_param(**param):
    skdebug('generate_nak_payload_with_param')
    len = param.get('len', 10)
    data_without_checksum = bytearray()
    for i in range(len):
        data_without_checksum.append(i)
    skdebug('data_without_checksum:', data_without_checksum.hex())
    checksum = clac_checksum(data_without_checksum)
    payload = data_without_checksum + struct.pack('>H', checksum)
    skdebug('payload:', payload.hex())
    return payload


def generate_header_with_param(**param):
    skdebug('generate_syn_header_with_param')
    # header = get_default_header_bytes_array()
    StartOfPacket = param.get('StartOfPacket', 0xAA55)
    PacketLength = param.get('PacketLength', 0)

    # ControlByte = BitSet(8)
    # ControlByte.reset()
    # if param.get('SYN', 0) == 1:
    #     ControlByte.set(BIT_SYN)
    # if param.get('ACK', 0) == 1:
    #     ControlByte.set(BIT_ACK)
    # if param.get('EAK', 0) == 1:
    #     ControlByte.set(BIT_EAK)
    # if param.get('RST', 0) == 1:
    #     ControlByte.set(BIT_RST)
    # if param.get('NAK') == 1:
    #     ControlByte.set(BIT_NAK)
    # if param.get('RES1') == 1:
    #     ControlByte.set(BIT_RES2)
    # if param.get('RES2') == 1:
    #     ControlByte.set(BIT_RES1)
    # if param.get('RES3') == 1:
    #     ControlByte.set(BIT_RES0)
    ControlByte = 0
    if param.get('SYN', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_SYN)
    if param.get('ACK', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_ACK)
    if param.get('EAK', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_EAK)
    if param.get('RST', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_RST)
    if param.get('NAK') == 1:
        ControlByte = ControlByte | (1 << BIT_NAK)
    if param.get('RES1') == 1:
        ControlByte = ControlByte | (1 << BIT_RES2)
    if param.get('RES2') == 1:
        ControlByte = ControlByte | (1 << BIT_RES1)
    if param.get('RES3') == 1:
        ControlByte = ControlByte | (1 << BIT_RES0)

    skdebug('ControlByte:', bin(ControlByte))

    PacketSeqNum = param.get('PacketSeqNum', 0)
    PacketAckNum = param.get('PacketAckNum', 0)
    SessionId = param.get('SessionId', 0)

    data_without_checksum = struct.pack(LinkPacketHeaderWithoutChecksumFormat, StartOfPacket,
                                        PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId)
    checksum = clac_checksum(data_without_checksum)
    HeaderChecksum = param.get('HeaderChecksum', checksum)

    return struct.pack(
        LinkPacketHeaderFormat, StartOfPacket, PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId,
        HeaderChecksum)
