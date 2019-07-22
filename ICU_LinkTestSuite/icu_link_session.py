#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
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


class LinkSession(object):
    _instance_lock = threading.Lock()

    def __init__(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.Reset(role, port, rate)

    def Reset(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.mSerialPort = SerialPort(port, rate)
        self.mRole = role
        self.mPSN = random.randint(0, 255)
        self.mRecvdSYN = None
        self.UpdateSynDefaultParam()

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
        if not self.mRecvdSYN:
            return False
        recvedLSP = LinkSynPayload(payload_bytes=self.mRecvdSYN.mPayloadBytes)
        if lsp_obj.mRetransTimeout == recvedLSP.mRetransTimeout and \
                lsp_obj.mCumAckTimeout == recvedLSP.mCumAckTimeout and \
                lsp_obj.mMaxNumOfRetrans == recvedLSP.mMaxNumOfRetrans and \
                lsp_obj.mMaxCumAck == recvedLSP.mMaxCumAck:
            return True
        return False

    def UpdatePSN(self):
        self.mPSN = (self.mPSN+1) % 256

    def SendPacket(self, packet, update_psn=True):
        skdebug('SendPacket:', packet.info_string())
        self.UpdatePSN()
        self.mSerialPort.SendPacket(packet.to_bytes())

    def SendRst(self):
        rst_pkt = LinkPacket.gen_std_rst_packet()
        self.SendPacket(rst_pkt, False)

    def SendEak(self):
        eak_pkt = LinkPacket.gen_random_eak_packet()
        self.SendPacket(eak_pkt, False)

    def SendNak(self):
        nak_pkt = LinkPacket.gen_nak_packet()
        self.SendPacket(nak_pkt, False)

    def SendApp(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mPSN
        }
        app_pkt = LinkPacket.gen_random_app_packet(param_dict)
        self.SendPacket(app_pkt)

    def SendAck(self, syn_pkt_obj=None):
        if not syn_pkt_obj:
            skdebug('use stored syn pkt')
            syn_pkt_obj = self.mRecvdSYN

        param_dict = {
            LinkSpec.cHFeild_PAN: syn_pkt_obj.mHeader.mPacketSeqNum,
        }
        ack_pkt = LinkPacket.gen_ack_packet(param_dict)
        self.SendPacket(ack_pkt, False)

    def SendSyn(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mPSN,
            LinkSpec.cHFeild_LV: self.mLinkVersion,
            LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
            LinkSpec.cHFeild_RT: self.mRetransTimeout,
            LinkSpec.cHFeild_CAT: self.mCumAckTimeout,
            LinkSpec.cHFeild_MNOR: self.mMaxNumOfRetrans,
            LinkSpec.cHFeild_MCA: self.mMaxCumAck,
        }
        syn_pkt = LinkPacket.gen_syn_packet(param_dict)
        self.SendPacket(syn_pkt)

    def ReplySyn(self, syn_pkt_obj=None):
        """根据SYN的参数来决定接受还是再次协商"""
        if not syn_pkt_obj:
            skdebug('use stored syn pkt')
            syn_pkt_obj = self.mRecvdSYN

        lsp_obj = LinkSynPayload(payload_bytes=syn_pkt_obj.mPayloadBytes)
        if self.CanAccpetSynParam(lsp_obj):
            """可以接受参数"""
            skdebug('accept syn param')
            param_dict = {
                LinkSpec.cHFeild_PSN: self.mPSN,
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
                LinkSpec.cHFeild_PSN: self.mPSN,
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
        self.SendPacket(syn_ack_pkt)

    def SendBadPkt(self,type):
        bad_pkt = LinkPacket.gen_bad_packet(type)
        self.SendPacket(bad_pkt)

    def StoreSyn(self, packet):
        self.mRecvdSYN = packet

    def RecviveSyn(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                # skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_syn_packet():
                    skdebug('recv packet is a syn packet:', link_pkt_obj.info_string())
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
                # skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_syn_ack_packet():
                    skdebug('recv packet is syn ack packet:', link_pkt_obj.info_string())
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
                skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_ack_packet():
                    skdebug('recv packet is ack packet:', link_pkt_obj.info_string())
                    return link_pkt_obj
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
