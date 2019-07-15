#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import logging
from enum import Enum
from icu_serial_port import SerialPort
from icu_link_packet import *
from icu_error import *


class LinkRole(Enum):
    UnKnown = 0
    MCU = 1
    SoC = 2


class LinkSession(object):
    def __init__(self, role):
        self.mSerialPort = SerialPort('COM1', 115200)
        self.mRole = role
        self.mPSN = random.randint(0, 255)
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

    def SendRst(self):
        rst_pkt = LinkPacket.gen_std_rst_packet()
        self.mSerialPort.SendPacket(rst_pkt.to_bytes())
        pass

    def SendSyn(self):
        pass

    def ReplySyn(self, syn_pkt_obj: LinkPacket):
        """根据SYN的参数来决定接受还是再次协商"""
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
        skdebug('Send SYN+ACK packet:', syn_ack_pkt.info_string())
        self.mSerialPort.SendPacket(syn_ack_pkt.to_bytes())

    def RecviveSyn(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_syn_packet():
                    skdebug('is syn packet')
                    return link_pkt_obj
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('timeout cost_time:', cost_time)
                raise RobotTimeoutError

    def RecviveSynAck(self, timeout=2):
        start_time = time.time()
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes)
                if link_pkt_obj.is_syn_ack_packet():
                    skdebug('is syn packet')
                    return link_pkt_obj
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('timeout cost_time:', cost_time)
                raise RobotTimeoutError

    def RecviveAck(self, timeout=2):
        pass


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