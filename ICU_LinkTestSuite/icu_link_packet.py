#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import struct
from enum import Enum
from icu_link_spec import *
from icu_debug import *
from icu_checksum import *
from icu_link_syn_payload import *
from icu_link_eak_payload import *


class PacketType(Enum):
    SYN = 0
    SYN_ACK = 1
    ACK = 2
    EAK = 3
    NAK = 4
    NoNAK = 5
    NoNAK_ACK = 6


class BadPktType(Enum):
    INVALID_SOP = 0
    INVALID_PL_MORE_THEN_ACTUAL = 1
    INVALID_PL_LESS_THEN_ACTUAL = 2
    BAD_PAN = 3
    BAD_CB = 4
    OVER_MAX_LEN = 5
    PSN_OUT_OF_RECV_WIN = 6  # PSN位于OutOfRecvWin范围内的数据包
    WITH_NONEED_PAN = 7  # TestSession数据包,携带非必须PAN字段
    INVALID_ACK = 8  # 包含错误PAN的ACK包
    INVALID_SESSION_ID = 9  # SessionID字段不合法的数据包
    INCORRECT_HC = 10  # HeaderChecksum字段不正确的数据包
    INCORRECT_PC = 11  # PayloadChecksum字段不正确的数据包
    SYN_INVALID_DATA = 12  # 携带非法字段的SYN包
    OVER_MAX_RECV_LEN_TEST_NONAK = 13  # 超过最大处理长度的测试数据包
    INVALID_CB = 14
    EAK_INVALID_PL_MORE_THEN_ACTUAL = 15
    EAK_INVALID_PL_LESS_THEN_ACTUAL = 16
    RST_WITH_PSN = 17
    RST_WITH_PAN = 18
    RST_WITH_INCORRECT_PL = 19
    SYN_ACK_INVALID_DATA = 20
    SYN_INVALID_DATA_SKIP_ONE_PSN = 21

class TestPktType(Enum):
    TEST_START = 0
    TEST_STOP = 1
    TEST_DATA_NONAK = 2
    TEST_REQUEST_NONAK = 3


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

    def __init__(self, header_bytes=None, header_dict=None, update_checksum=True):
        # skdebug('LinkPacketHeader construct')
        if header_bytes != None:
            # skdebug('header_bytes exist')
            self.update_with_bytes(header_bytes)
        elif header_dict != None:
            # skdebug('header_dict exist')
            self.update_with_dict(header_dict, update_checksum=update_checksum)

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

    def update_with_dict(self, header_dict: dict, update_checksum=True):
        # skdebug('LinkPacketHeader update with dict')
        self.mStartOfPacket = header_dict.get(LinkSpec.cHFeild_SOP, 0xAA55)
        self.mPacketLength = header_dict.get(LinkSpec.cHFeild_PL, 0)
        # skdebug('mPacketLength:', self.mPacketLength)
        self.mControlByte = ControlByte(cb_dict=header_dict)
        # skdebug('ControlByte:', bin(self.mControlByte.mValue))
        self.mPacketSeqNum = header_dict.get(LinkSpec.cHFeild_PSN, 0)
        self.mPacketAckNum = header_dict.get(LinkSpec.cHFeild_PAN, 0)
        self.mSessionId = header_dict.get(LinkSpec.cHFeild_SI, 0)
        self.mHeaderChecksum = header_dict.get(LinkSpec.cHFeild_HC, 0)
        if update_checksum:
            self.update_checksum()

    def update_packet_length(self, len, auto_update_hc=True):
        self.mPacketLength = len
        if auto_update_hc:
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
        return struct.pack(LinkSpec.cLinkPacketHeaderFormat,
                           self.mStartOfPacket, self.mPacketLength, self.mControlByte.mValue,
                           self.mPacketSeqNum, self.mPacketAckNum, self.mSessionId, self.mHeaderChecksum)


class LinkPacket(object):

    def __init__(self, packet_bytes=None, header_bytes=None, payload_bytes=None,
                 auto_update_pl=True, auto_update_hc=True, recv_time=None):
        if auto_update_pl:
            self.mAutoUpdatePL = True
        else:
            self.mAutoUpdatePL = False

        if recv_time:
            self.mRecvTime = recv_time

        if packet_bytes != None:
            self.update_packet_with_bytes(packet_bytes)
        elif header_bytes != None:
            self.update_header_with_bytes(header_bytes)
            if payload_bytes != None:
                skdebug('payload_bytes:', payload_bytes.hex())
                self.update_payload_with_bytes(payload_bytes)
                self.update_packet_length(len(header_bytes)+len(payload_bytes), auto_update_hc)
            else:
                self.update_packet_length(len(header_bytes), auto_update_hc)

    def psn(self):
        return self.mHeader.mPacketSeqNum

    def pan(self):
        return self.mHeader.mPacketAckNum

    def max_cum_ack(self):
        return self

    def gen_test_start_payload():
        pdata = bytearray(b'\x00')
        pdata += (bytes('SPICU-LinkTest!', encoding='ASCII'))
        skdebug('payload_data:', pdata)
        skdebug('payload_data:', pdata.hex())
        res = clac_checksum(pdata)
        return pdata + res.to_bytes(length=2, byteorder='big', signed=False)

    def gen_random_payload(chunk_size=1, auto_update_pc=True):
        skdebug('gen_random_payload chunk_size:', chunk_size)
        data = bytes.fromhex('000102030405060708090A0B0C0D0E0F')
        whole_data = bytearray()
        for i in range(chunk_size):
            whole_data += data
        skdebug('whole_data len:', len(whole_data))
        if auto_update_pc:
            res = clac_checksum(whole_data)
        else:
            res = int(0xF5F5)
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

    def gen_eak_packet(pan, outseq_psn_list: list):
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_ACK: 1,
            LinkSpec.cHFeild_EAK: 1,
            LinkSpec.cHFeild_PAN: pan})
        if len(outseq_psn_list):
            payload = LinkEAKPayload(pan=pan, psn_list=outseq_psn_list)
            skdebug('payload bytes:', payload.to_bytes().hex())
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=payload.to_bytes())
        else:
            return LinkPacket(header_bytes=header.to_bytes())

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
        # skdebug('gen_syn_ack_packet param_dict:', param_dict)
        header = LinkPacketHeader(header_dict={
            LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
            LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            LinkSpec.cHFeild_SYN: 1, LinkSpec.cHFeild_ACK: 1})
        payload = LinkSynPayload(payload_dict=param_dict)
        return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=payload.to_bytes())

    def gen_bad_packet(type, param_dict: dict = None):
        if type == BadPktType.INVALID_SOP:
            skdebug('INVALID_SOP')
            random_sop = random.randint(0, 65535)
            header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_SOP: random_sop})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.INVALID_PL_MORE_THEN_ACTUAL:
            skdebug('INVALID_PL_MORE_THEN_ACTUAL')
            random_pl = random.randint(256, 1024)
            # skdebug('random_pl:', random_pl)
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PL: random_pl,
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_pl=False)
        elif type == BadPktType.INVALID_PL_LESS_THEN_ACTUAL:
            skdebug('INVALID_PL_LESS_THEN_ACTUAL')  # 包长字段 < 实际payload
            random_pl = 16
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PL: random_pl
            })
            pl_bytes = LinkPacket.gen_random_payload(chunk_size=2)
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_pl=False)
        elif type == BadPktType.BAD_PAN:
            skdebug('BAD_PAN')
            random_pan = random.randint(0, 255)
            # skdebug('random_pan:', random_pan)
            header = LinkPacketHeader(header_dict={LinkSpec.cHFeild_PAN: random_pan})
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.BAD_CB:
            skdebug('BAD_CB')
            # 这里需求修改测试不同的错误ControlBytes
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SYN: 1,
                LinkSpec.cHFeild_RST: 1, })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.INVALID_CB:
            skdebug('INVALID_CB')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_SYN: 1,
                LinkSpec.cHFeild_EAK: 1
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.OVER_MAX_LEN:
            skdebug('OVER_MAX_LEN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
            })
            pl_bytes = LinkPacket.gen_random_payload(chunk_size=int(param_dict[LinkSpec.cHFeild_RemoteMRPL]/16+1))
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.PSN_OUT_OF_RECV_WIN:
            skdebug('PSN_OUT_OF_RECV_WIN')
            bad_psn = (param_dict[LinkSpec.cHFeild_PSN] + param_dict[LinkSpec.cHFeild_MNOOSP]+1) % 256
            skdebug('previous sent psn:', param_dict[LinkSpec.cHFeild_PSN])
            skdebug('bad psn:', bad_psn)
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PSN: bad_psn
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.WITH_NONEED_PAN:
            skdebug('WITH_NONEED_PAN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN]
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.INVALID_ACK:
            skdebug('INVALID_ACK')
            bad_pan = (param_dict[LinkSpec.cHFeild_PAN] + 50) % 256
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PAN: bad_pan
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.INVALID_SESSION_ID:
            skdebug('INVALID_SESSION_ID')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: 0xF1,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.INCORRECT_HC:
            skdebug('INCORRECT_HC')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_HC: 0xF5F5
            }, update_checksum=False)
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_hc=False)
        elif type == BadPktType.INCORRECT_PC:
            skdebug('INCORRECT_PC')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            })
            pl_bytes = LinkPacket.gen_random_payload(auto_update_pc=False)
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.SYN_INVALID_DATA:
            skdebug('SYN_INVALID_DATA')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_SYN: 1
            })
            lsp_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=lsp_bytes)
        elif type == BadPktType.SYN_INVALID_DATA_SKIP_ONE_PSN:
            skdebug('SYN_INVALID_DATA_SKIP_ONE_PSN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]+1,
                LinkSpec.cHFeild_SYN: 1
            })
            lsp_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=lsp_bytes)
        elif type == BadPktType.SYN_ACK_INVALID_DATA:
            skdebug('SYN_ACK_INVALID_DATA')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
                LinkSpec.cHFeild_SYN: 1,
                LinkSpec.cHFeild_ACK: 1,
            })
            lsp_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=lsp_bytes)
        elif type == BadPktType.OVER_MAX_RECV_LEN_TEST_NONAK:
            skdebug('OVER_MAX_RECV_LEN_TEST_NONAK')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            })
            pl_bytes = LinkPacket.gen_random_payload(chunk_size=int(param_dict[LinkSpec.cHFeild_RemoteMRPL]/16+1))
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == BadPktType.EAK_INVALID_PL_MORE_THEN_ACTUAL:
            skdebug('EAK_INVALID_PL_MORE_THEN_ACTUAL')
            random_pl = random.randint(256, 65535)
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_ACK: 1,
                LinkSpec.cHFeild_EAK: 1,
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
                LinkSpec.cHFeild_PL: random_pl,
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_pl=False)
        elif type == BadPktType.EAK_INVALID_PL_LESS_THEN_ACTUAL:
            skdebug('EAK_INVALID_PL_LESS_THEN_ACTUAL')
            random_pl = 16
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
                LinkSpec.cHFeild_PL: random_pl
            })
            pl_bytes = LinkPacket.gen_random_payload(chunk_size=2)
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes, auto_update_pl=False)
        elif type == BadPktType.RST_WITH_PSN:
            skdebug('RST_WITH_PSN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_RST: 1,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN],
            })
            return LinkPacket(header_bytes=header.to_bytes())
        elif type == BadPktType.RST_WITH_PAN:
            skdebug('RST_WITH_PAN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_RST: 1,
                LinkSpec.cHFeild_PAN: param_dict[LinkSpec.cHFeild_PAN],
            })
            return LinkPacket(header_bytes=header.to_bytes())
        elif type == BadPktType.RST_WITH_INCORRECT_PL:
            skdebug('RST_WITH_PAN')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_RST: 1,
                LinkSpec.cHFeild_PL: 0xFF,
            })
            return LinkPacket(header_bytes=header.to_bytes(),auto_update_pl=False)
        




    def gen_test_packet(type, req_pkt_count=1, param_dict: dict = None):
        if type == TestPktType.TEST_START:
            skdebug('TEST_START')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]
            })
            pl_bytes = LinkPacket.gen_test_start_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == TestPktType.TEST_DATA_NONAK:
            skdebug('TEST_DATA_NONAK')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]
            })
            pl_bytes = LinkPacket.gen_random_payload()
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)
        elif type == TestPktType.TEST_REQUEST_NONAK:
            skdebug('TEST_REQUEST_NONAK')
            header = LinkPacketHeader(header_dict={
                LinkSpec.cHFeild_SI: LinkSpec.cSessionID_TestSession,
                LinkSpec.cHFeild_PSN: param_dict[LinkSpec.cHFeild_PSN]
            })
            pl_bytes = LinkPacket.gen_test_request_data_payload(count=req_pkt_count)
            skdebug('pl_bytes:', pl_bytes.hex())
            return LinkPacket(header_bytes=header.to_bytes(), payload_bytes=pl_bytes)

    def update_packet_length(self, pkt_len, auto_update_hc):
        if self.mAutoUpdatePL:
            self.mHeader.update_packet_length(pkt_len, auto_update_hc)

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
            # skdebug('mPayloadChecksum:', hex(self.mPayloadChecksum))
            if self.is_syn_packet() or self.is_syn_ack_packet():
                payload_info = LinkSynPayload(payload_bytes=self.mPayloadBytes).info_string()
            elif self.is_eak_packet():
                payload_info = LinkEAKPayload(payload_bytes=self.mPayloadBytes).info_string()
            else:
                payload_info = ' PD: 0x{}  PC: 0x{:04X}'.format(self.mPayloadData.hex(), self.mPayloadChecksum)
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
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mSessionId == 0 and \
                self.mHeader.mPacketLength == 22:
            return True
        return False

    def is_syn_ack_packet(self):
        if self.mHeader.mControlByte.mSYN == 1 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mSessionId == 0 and \
                self.mHeader.mPacketLength == 22:
            return True
        return False

    def is_ack_packet(self):
        if self.mHeader.mControlByte.mSYN == 0 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mSessionId == 0 and \
                self.mHeader.mPacketSeqNum == 0:  # ACK包PSN必须为0
            return True
        return False

    def is_eak_packet(self):
        if self.mHeader.mControlByte.mSYN == 0 and \
                self.mHeader.mControlByte.mEAK == 1 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mSessionId == 0 and \
                self.mHeader.mPacketLength > 12:
            return True
        return False

    def is_nonak_ack_packet(self):
        # 携带ACK信息的NoNak数据包
        if self.mHeader.mControlByte.mSYN == 0 and \
                self.mHeader.mControlByte.mEAK == 0 and \
                self.mHeader.mControlByte.mACK == 1 and \
                self.mHeader.mControlByte.mNAK == 0 and \
                self.mHeader.mControlByte.mRST == 0 and \
                self.mHeader.mPacketLength > 12:
            return True
        return False

    def is_nonak_packet(self):
        if self.is_syn_packet() or self.is_syn_ack_packet() or self.is_nonak_ack_packet():
            return True
        elif self.is_ack_packet() or self.is_eak_packet():
            return False
        elif self.mHeader.mControlByte.mNAK == 0:
            return True


def PacketTypeMatch(packet: LinkPacket, type: PacketType):
    if type == PacketType.SYN:
        return packet.is_syn_packet()
    elif type == PacketType.SYN_ACK:
        return packet.is_syn_ack_packet()
    elif type == PacketType.ACK:
        return packet.is_ack_packet()
    elif type == PacketType.NoNAK:
        return packet.is_nonak_packet()
    elif type == PacketType.NoNAK_ACK:
        return packet.is_nonak_ack_packet()
    elif type == PacketType.EAK:
        return packet.is_eak_packet()
    return False


def IsNoNakPacket(packet: LinkPacket):
    return packet.is_nonak_packet() or packet.is_nonak_ack_packet()


def IsEakPacket(packet: LinkPacket):
    return packet.is_eak_packet()


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
