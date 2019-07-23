#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import collections
import logging
import threading
from enum import Enum
from icu_serial_port import SerialPort
from icu_link_packet import *
from icu_error import *


class LinkRole(Enum):
    UnKnown = 0
    MCU = 1
    SoC = 2


class SessionState(object):
    def __init__(self):
        self.mSendQMaxSize = 1
        self.mRecvQMaxSize = 1
        self.mSendQueue = collections.deque(maxlen=1)
        self.mRecvQueue = collections.deque(maxlen=1)
        self.mNextSendPSN = random.randint(0, 255)

    def Update(self):
        pass

    def GetNextPSN(self, autoplus=True):
        np = self.mNextSendPSN
        if autoplus:
            self.mNextSendPSN = (self.mNextSendPSN + 1) % 255
        return np

    def IsValidPan(self, pan):
        for i in range(len(self.mSendQueue)):
            pkt: LinkPacket = self.mSendQueue[i]
            skdebug('IsValidPan, check psn', pkt.mHeader.mPacketSeqNum)
            if pkt.mHeader.mPacketSeqNum == pan:
                return True
        skdebug('IsValidPan, not a valid pan', pan)
        return False

    def StashSentPkt(self, packet):
        self.mSendQueue.append(packet)

    def StashRecvPkt(self, packet):
        self.mRecvQueue.append(packet)

    def GetLastSentPkt(self):
        return self.mSendQueue[-1]

    def GetLastRecvPkt(self):
        return self.mRecvQueue[-1]


class LinkSession(object):
    _instance_lock = threading.Lock()

    def __init__(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.Reset(role, port, rate)

    def Reset(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.mSerialPort = SerialPort(port, rate)
        self.mRole = role
        self.mPSN = random.randint(0, 255)
        self.UpdateSynDefaultParam()
        self.mState = SessionState()

    def SynCompeted(self):
        self.mState.Update()

    def UpdateSynDefaultParam(self):
        if self.mRole == LinkRole.MCU:
            self.mLinkVersion = 1
            self.mMaxNumOfOutStdPkts = 4
            self.mMaxRecvPktLen = 256
            self.mRetransTimeout = 400
            self.mCumAckTimeout = 22
            self.mMaxNumOfRetrans = 10
            self.mMaxCumAck = 3
        elif self.mRole == LinkRole.SoC:
            self.mLinkVersion = 1
            self.mMaxNumOfOutStdPkts = 5
            self.mMaxRecvPktLen = 2048
            self.mRetransTimeout = 400
            self.mCumAckTimeout = 22
            self.mMaxNumOfRetrans = 10
            self.mMaxCumAck = 3
        self.DebugLinkParam()

    def UpdateSynNegotiableParam(self, rt=500, cat=30, mnor=5, mca=4):
        if rt:
            self.mRetransTimeout = rt
        else:
            self.mRetransTimeout = random.randint(20, 65535)
        if cat:
            self.mCumAckTimeout = cat
        else:
            self.mCumAckTimeout = random.randint(10, self.mRetransTimeout/2)
        if mnor:
            self.mMaxNumOfRetrans = mnor
        else:
            self.mMaxNumOfRetrans = random.randint(1, 30)
        if mca:
            self.mMaxCumAck = mca
        else:
            self.mMaxCumAck = random.randint(0, 127)
        self.DebugLinkParam()

    def DebugLinkParam(self):
        link_param_string = 'RT: {:d}  CAT: {:d}  MNOR: {:d}  MCA: {:d}'.format(self.mRetransTimeout, self.mCumAckTimeout, self.mMaxNumOfRetrans, self.mMaxCumAck)
        skdebug('session default link param:', link_param_string)

    @classmethod
    def GetInstance(cls, *args, **kwargs):
        if not hasattr(LinkSession, "_instance"):
            with LinkSession._instance_lock:
                if not hasattr(LinkSession, "_instance"):
                    LinkSession._instance = LinkSession(*args, **kwargs)
                    # LinkSession._instance.OpenPort()
        return LinkSession._instance

    def OpenPort(self):
        self.mSerialPort.Open()

    def ClosePort(self):
        self.mSerialPort.Close()

    def CanAccpetSynParam(self, lsp_obj: LinkSynPayload):
        if lsp_obj.mRetransTimeout == self.mRetransTimeout and \
                lsp_obj.mCumAckTimeout == self.mCumAckTimeout and \
                lsp_obj.mMaxNumOfRetrans == self.mMaxNumOfRetrans and \
                lsp_obj.mMaxCumAck == self.mMaxCumAck:
            return True
        return False

    def IsNegotiableSynParam(self, lsp_obj: LinkSynPayload):
        return not self.CanAccpetSynParam(lsp_obj)

    def IsRepeatSynParam(self, lsp_obj: LinkSynPayload):
        pkt = self.mState.GetLastRecvPkt()
        if not LinkPacket.is_syn_packet(pkt):
            return False
        recvedLSP = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
        if lsp_obj.mRetransTimeout == recvedLSP.mRetransTimeout and \
                lsp_obj.mCumAckTimeout == recvedLSP.mCumAckTimeout and \
                lsp_obj.mMaxNumOfRetrans == recvedLSP.mMaxNumOfRetrans and \
                lsp_obj.mMaxCumAck == recvedLSP.mMaxCumAck:
            return True
        return False

    def SendPacket(self, packet):
        skdebug('SendPacket:', packet.info_string())
        self.mSerialPort.SendPacket(packet.to_bytes())

    def SendRst(self):
        rst_pkt = LinkPacket.gen_std_rst_packet()
        self.SendPacket(rst_pkt)

    def SendEak(self):
        eak_pkt = LinkPacket.gen_random_eak_packet()
        self.SendPacket(eak_pkt)

    def SendNak(self):
        nak_pkt = LinkPacket.gen_nak_packet()
        self.SendPacket(nak_pkt)

    def SendApp(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mState.GetNextPSN()
        }
        app_pkt = LinkPacket.gen_random_app_packet(param_dict)
        self.mState.StashSentPkt(app_pkt)
        self.SendPacket(app_pkt)

    def SendAck(self, syn_pkt_obj=None):
        if not syn_pkt_obj:
            skdebug('use stored syn pkt')
            pkt = self.mState.GetLastRecvPkt()
            if not LinkPacket.is_syn_packet(pkt):
                raise RobotTestFlowException
            syn_pkt_obj = pkt

        param_dict = {
            LinkSpec.cHFeild_PAN: syn_pkt_obj.mHeader.mPacketSeqNum,
        }
        ack_pkt = LinkPacket.gen_ack_packet(param_dict)
        self.SendPacket(ack_pkt)

    def SendSyn(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mState.GetNextPSN(),
            LinkSpec.cHFeild_LV: self.mLinkVersion,
            LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
            LinkSpec.cHFeild_RT: self.mRetransTimeout,
            LinkSpec.cHFeild_CAT: self.mCumAckTimeout,
            LinkSpec.cHFeild_MNOR: self.mMaxNumOfRetrans,
            LinkSpec.cHFeild_MCA: self.mMaxCumAck,
        }
        syn_pkt = LinkPacket.gen_syn_packet(param_dict)
        self.mState.StashSentPkt(syn_pkt)
        self.SendPacket(syn_pkt)

    def ReplySyn(self, syn_pkt_obj=None):
        """根据SYN的参数来决定接受还是再次协商"""
        if not syn_pkt_obj:
            skdebug('use stored syn pkt')
            pkt = self.mState.GetLastRecvPkt()
            if not LinkPacket.is_syn_packet(pkt):
                raise RobotTestFlowException
            syn_pkt_obj = pkt

        lsp_obj = LinkSynPayload(payload_bytes=syn_pkt_obj.mPayloadBytes)
        if self.CanAccpetSynParam(lsp_obj):
            """可以接受参数"""
            skdebug('accept syn param')
            param_dict = {
                LinkSpec.cHFeild_PSN: self.mState.GetNextPSN(),
                LinkSpec.cHFeild_PAN: syn_pkt_obj.mHeader.mPacketSeqNum,
                # 非协商部分采用己端参数
                LinkSpec.cHFeild_LV: self.mLinkVersion,
                LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
                LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
                # 可协商部分接收对端参数
                LinkSpec.cHFeild_RT: lsp_obj.mRetransTimeout,
                LinkSpec.cHFeild_CAT: lsp_obj.mCumAckTimeout,
                LinkSpec.cHFeild_MNOR: lsp_obj.mMaxNumOfRetrans,
                LinkSpec.cHFeild_MCA: lsp_obj.mMaxCumAck,
            }
        else:
            """不可以接受参数"""
            skdebug('negotiate syn param')
            param_dict = {
                LinkSpec.cHFeild_PSN: self.mState.GetNextPSN(),
                LinkSpec.cHFeild_PAN: syn_pkt_obj.mHeader.mPacketSeqNum,
                # 非协商部分采用己端参数
                LinkSpec.cHFeild_LV: self.mLinkVersion,
                LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
                LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
                # 可协商部分也采用己端参数
                LinkSpec.cHFeild_RT: self.mRetransTimeout,
                LinkSpec.cHFeild_CAT: self.mCumAckTimeout,
                LinkSpec.cHFeild_MNOR: self.mMaxNumOfRetrans,
                LinkSpec.cHFeild_MCA: self.mMaxCumAck,
            }
        syn_ack_pkt = LinkPacket.gen_syn_ack_packet(param_dict)
        self.mState.StashSentPkt(syn_ack_pkt)
        self.SendPacket(syn_ack_pkt)

    def RetransmitSynAck(self):
        pkt = self.mState.GetLastSentPkt()
        if not LinkPacket.is_syn_ack_packet(pkt):
            raise RobotTestFlowException
        else:
            self.SendPacket(pkt)

    def SendBadPkt(self, type):
        param_dict = {
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen
        }
        bad_pkt = LinkPacket.gen_bad_packet(type, param_dict)
        self.SendPacket(bad_pkt)

    def TestStart(self):
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_START)
        self.SendPacket(pkt)

    def TestSendNoNAK(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mState.GetNextPSN()
        }
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict)
        self.mState.StashSentPkt(pkt)
        self.SendPacket(pkt)

    def RecviveSyn(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('RecviveSyn received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_need_ack_packet():
                    self.mState.StashRecvPkt(link_pkt_obj)
                if link_pkt_obj.is_syn_packet():
                    skdebug('RecviveSyn recv packet is a syn packet:', link_pkt_obj.info_string())
                    return link_pkt_obj
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('RecviveSyn timeout cost_time:', cost_time)
                raise RobotTimeoutError

    def RecviveSynAck(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('RecviveSynAck received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_need_ack_packet():
                    self.mState.StashRecvPkt(link_pkt_obj)
                if link_pkt_obj.is_syn_ack_packet():
                    skdebug('RecviveSynAck recv packet is syn ack packet:', link_pkt_obj.info_string())
                    return link_pkt_obj
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('RecviveSynAck timeout cost_time:', cost_time)
                raise RobotTimeoutError

    def RecviveAck(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('RecviveAck received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_need_ack_packet():
                    self.mState.StashRecvPkt(link_pkt_obj)
                if link_pkt_obj.is_ack_packet():
                    skdebug('RecviveAck recv packet is ack packet:', link_pkt_obj.info_string())
                    if self.mState.IsValidPan(link_pkt_obj.mHeader.mPacketAckNum):
                        return link_pkt_obj
                else:
                    skdebug('RecviveAck recv packet is not ack packet', link_pkt_obj.info_string())
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('RecviveAck timeout cost_time:', cost_time)
                raise RobotTimeoutError

    def RecviveNothing(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('received a packet')
                raise RobotRecvInvalidData
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('timeout cost_time:', cost_time)
                return



if __name__ == "__main__":
    session = LinkSession(LinkRole.MCU)
    session.OpenPort()

    session.SendRst()
    skdebug('send rst ok')

    try:
        syn_pkt_obj = session.RecviveSyn()
        skdebug('recvd a syn pkt: ', syn_pkt_obj.info_string())

        session.ReplySyn(syn_pkt_obj)
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        session.ClosePort()
        quit()
    else:
        pass

    skdebug('sleep begin')
    time.sleep(1)
    skdebug('sleep end')
    session.ClosePort()
