#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import logging
import threading
from enum import Enum

from icu_serial_port import SerialPort
from icu_link_session_state import*


class LinkRole(Enum):
    UnKnown = 0
    MCU = 1
    SoC = 2


class LinkSession(object):
    _instance_lock = threading.Lock()

    @classmethod
    def GetInstance(cls, *args, **kwargs):
        if not hasattr(LinkSession, "_instance"):
            with LinkSession._instance_lock:
                if not hasattr(LinkSession, "_instance"):
                    LinkSession._instance = LinkSession(*args, **kwargs)
                    # LinkSession._instance.OpenPort()
        return LinkSession._instance

    def __init__(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.Reset(role, port, rate)

    def Reset(self, role=LinkRole.MCU, port='COM1', rate=115200):
        self.mSerialPort = SerialPort(port, rate)
        self.mRole = role
        self.UpdateSynDefaultParam()
        self.mState = SessionState()

    def StateReset(self):
        self.UpdateSynDefaultParam()
        self.mState = SessionState()

    def UpdateSynDefaultParam(self):
        if self.mRole == LinkRole.MCU:
            self.mLinkVersion = 1
            self.mMaxNumOfOutStdPkts = 5
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

    def SynCompete(self):
        param_dict = {
            LinkSpec.cHFeild_LV: self.mLinkVersion,
            LinkSpec.cHFeild_RT: self.mRetransTimeout,
            LinkSpec.cHFeild_CAT: self.mCumAckTimeout,
            LinkSpec.cHFeild_MNOR: self.mMaxNumOfRetrans,
            LinkSpec.cHFeild_MCA: self.mMaxCumAck,
            LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen}
        self.mState.SynComplete(param_dict)

    def DebugLinkParam(self):
        link_param_string = 'RT: {:d}  CAT: {:d}  MNOR: {:d}  MCA: {:d}'.format(self.mRetransTimeout, self.mCumAckTimeout, self.mMaxNumOfRetrans, self.mMaxCumAck)
        skdebug('session default link param:', link_param_string)

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

    def StashRemoteLinkParam(self, max_recv_pkt_len, max_num_of_out_std_pkts):
        self.mState.StashRemoteLinkParam(
            max_recv_pkt_len, max_num_of_out_std_pkts)

    def GetNegotiatedMaxCumAck(self):
        return self.mState.mNegotiatedMaxCumAck

    def StashRecvEAKPkt(self, pkt):
        return self.mState.StashRecvEAKPkt(pkt)

    def GetRecvEAKPkt(self):
        return self.mState.GetRecvEAKPkt()

    def StashSentEAKPkt(self, pkt):
        return self.mState.StashSentEAKPkt(pkt)

    def GetSentEAKPkt(self):
        return self.mState.GetSentEAKPkt()

    def GetLastSentPSN(self):
        pkt = self.mState.GetLastPktFromSentQueue()
        return pkt.psn()

    def GetFirstSentPSN(self):
        pkt = self.mState.GetPktFromSentQueue()
        return pkt.psn()

    def GetLastInSequencePSN(self):
        return self.mState.GetLastInSequencePSN()

    def GetOutSequencePSN(self):
        return self.mState.GetOutSequencePSN()

    def GetRetransmitPkt(self, psn):
        return self.mState.GetRetransmitPkt(psn)

    def IsValidPan(self, pan):
        return self.mState.IsValidPan(pan)

    def IsNegotiableSynParam(self, lsp_obj: LinkSynPayload):
        return not self.CanAccpetSynParam(lsp_obj)

    def IsRepeatSynPacket(self, packet):
        last_recv_pkt = self.mState.GetLastRecvPkt()
        return packet.is_syn_packet() and last_recv_pkt and last_recv_pkt.psn() == packet.psn()

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

    def SendPacket(self, packet: LinkPacket):
        skdebug('SendPacket:', packet.info_string())
        t = self.mSerialPort.SendPacket(packet.to_bytes())
        packet.mSentTime = t
        return packet

    def SendRst(self):
        rst_pkt = LinkPacket.gen_std_rst_packet()
        return self.SendPacket(rst_pkt)

    def SendRandomEak(self, pan=None):
        if not pan:
            pkt = self.mState.GetLastRecvPkt()
            pan = pkt.mHeader.mPacketSeqNum
        param_dict = {
            LinkSpec.cHFeild_PAN: pan
        }
        eak_pkt = LinkPacket.gen_random_eak_packet(param_dict)
        return self.SendPacket(eak_pkt)

    def SendNak(self):
        nak_pkt = LinkPacket.gen_nak_packet()
        return self.SendPacket(nak_pkt)

    def SendApp(self):
        param_dict = {
            LinkSpec.cHFeild_PSN: self.mState.GetNextPSN()
        }
        app_pkt = LinkPacket.gen_random_app_packet(param_dict)
        self.mState.StashSentPkt(app_pkt)
        return self.SendPacket(app_pkt)

    def SendEAK(self):
        last_psn = self.GetLastInSequencePSN()
        psn_list = self.GetOutSequencePSN()
        skdebug('last_psn:', last_psn)
        skdebug('psn_list:', psn_list)
        pkt = LinkPacket.gen_eak_packet(last_psn, psn_list)
        self.StashSentEAKPkt(pkt)
        return self.SendPacket(pkt)

    def SendAck(self, pan=None):
        if not pan:
            pkt = self.mState.GetLastRecvPkt()
            pan = pkt.mHeader.mPacketSeqNum
        param_dict = {
            LinkSpec.cHFeild_PAN: pan,
        }
        ack_pkt = LinkPacket.gen_ack_packet(param_dict)
        return self.SendPacket(ack_pkt)

    def SendSyn(self, skip_psn=0):
        while skip_psn > 0:
            psn = self.mState.GetNextPSN()
            skdebug('skip psn:', psn)
            pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: psn})
            self.mState.StashSentPkt(pkt)
            skip_psn = skip_psn-1
        psn = self.mState.GetNextPSN()
        param_dict = {
            LinkSpec.cHFeild_PSN: psn,
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
        return self.SendPacket(syn_pkt)

    def SendSynAck(self, skip_psn=0):
        while skip_psn > 0:
            psn = self.mState.GetNextPSN()
            skdebug('skip psn:', psn)
            pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: psn})
            self.mState.StashSentPkt(pkt)
            skip_psn = skip_psn-1
        psn = self.mState.GetNextPSN()
        last_recv_pkt = self.mState.GetLastRecvPkt()
        skdebug('last recv packet psn:', last_recv_pkt.mHeader.mPacketSeqNum)
        param_dict = {
            LinkSpec.cHFeild_PSN: psn,
            LinkSpec.cHFeild_PAN: last_recv_pkt.mHeader.mPacketSeqNum,
            LinkSpec.cHFeild_LV: self.mLinkVersion,
            LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
            LinkSpec.cHFeild_RT: self.mRetransTimeout,
            LinkSpec.cHFeild_CAT: self.mCumAckTimeout,
            LinkSpec.cHFeild_MNOR: self.mMaxNumOfRetrans,
            LinkSpec.cHFeild_MCA: self.mMaxCumAck,
        }
        pkt = LinkPacket.gen_syn_ack_packet(param_dict)
        self.mState.StashSentPkt(pkt)
        return self.SendPacket(pkt)

    def ReplySyn(self, syn_pkt_obj=None):
        """根据SYN的参数来决定接受还是再次协商"""
        if not syn_pkt_obj:
            skdebug('use stored syn pkt')
            pkt = self.mState.GetLastRecvPkt()
            if LinkPacket.is_syn_packet(pkt) or LinkPacket.is_syn_ack_packet(pkt):
                syn_pkt_obj = pkt
            else:
                raise RobotTestFlowException

        lsp_obj = LinkSynPayload(payload_bytes=syn_pkt_obj.mPayloadBytes)

        self.mState.mRemoteMaxRecvPktLen = lsp_obj.mMaxRecvPktLen
        self.mState.mRemoteMaxNumOfOutStdPkts = lsp_obj.mMaxNumOfOutStdPkts

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
        return self.SendPacket(syn_ack_pkt)

    def RetransmitSynAck(self):
        pkt = self.mState.GetLastPktFromSentQueue()
        if not LinkPacket.is_syn_ack_packet(pkt):
            raise RobotTestFlowException
        else:
            return self.SendPacket(pkt)

    def RetransmitPreviousNoNAK(self):
        pkt = self.mState.GetLastPktFromSentQueue()
        return self.SendPacket(pkt)

    def RetransmitFirstNoNAKInSentQ(self):
        pkt = self.mState.GetPktFromSentQueue()
        return self.SendPacket(pkt)

    def RetransmitThirdNoNAKInSentQ(self):
        pkt = self.mState.GetPktFromSentQueue(index=2)
        return self.SendPacket(pkt)

    def SendBadPkt(self, type):
        # last_sent_pkt:LinkPacket = self.mState.GetLastPktFromSentQueue()
        last_recv_pkt: LinkPacket = self.mState.GetLastRecvPkt()

        if type == BadPktType.INVALID_SOP or \
                type == BadPktType.INVALID_SESSION_ID or \
                type == BadPktType.INVALID_CB or \
                type == BadPktType.INCORRECT_HC or \
                type == BadPktType.INCORRECT_PC or \
                type == BadPktType.INVALID_PL_MORE_THEN_ACTUAL or \
                type == BadPktType.INVALID_PL_LESS_THEN_ACTUAL or \
                type == BadPktType.RST_WITH_PSN or \
                type == BadPktType.RST_WITH_PAN or \
                type == BadPktType.RST_WITH_INCORRECT_PL or \
                type == BadPktType.OVER_MAX_LEN:
            psn = self.mState.GetNextPSN(autoplus=False)
        else:
            psn = self.mState.GetNextPSN()

        param_dict = {
            LinkSpec.cHFeild_MNOOSP: self.mMaxNumOfOutStdPkts,
            LinkSpec.cHFeild_RemoteMRPL: self.mState.mRemoteMaxRecvPktLen,
            LinkSpec.cHFeild_MRPL: self.mMaxRecvPktLen,
            LinkSpec.cHFeild_PSN: psn,
            LinkSpec.cHFeild_PAN: last_recv_pkt.mHeader.mPacketSeqNum
        }
        bad_pkt = LinkPacket.gen_bad_packet(type, param_dict)

        if type == BadPktType.WITH_NONEED_PAN or \
                type == BadPktType.SYN_INVALID_DATA:
            self.mState.StashSentPkt(bad_pkt)
        return self.SendPacket(bad_pkt)

    def TestStart(self):
        pdict = {
            LinkSpec.cHFeild_PSN: self.mState.GetNextPSN()
        }
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_START, param_dict=pdict)
        self.mState.StashSentPkt(pkt)
        return self.SendPacket(pkt)

    def SendTestNoNAK(self, skip_psn=0):
        while skip_psn > 0:
            psn = self.mState.GetNextPSN()
            skdebug('skip psn:', psn)
            pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: psn})
            self.mState.StashSentPkt(pkt)
            skip_psn = skip_psn-1
        psn = self.mState.GetNextPSN()
        skdebug('send psn:', psn)
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: psn})
        self.mState.StashSentPkt(pkt)
        return self.SendPacket(pkt)

    def TestSendNoNAKSpecifiedPSN(self, specified_psn=0):
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: specified_psn})
        return self.SendPacket(pkt)

    def RetransmitNoNAK(self, psn=None, pan=None, psn_list=None):
        if psn:
            pkt: LinkPacket = self.GetRetransmitPkt(psn)
            if pan:
                pkt.pan(pan)
            self.SendPacket(pkt)
        else:
            for psn in psn_list:
                pkt = self.GetRetransmitPkt(psn)
                self.SendPacket(pkt)

    def RequestTestNoNAK(self, count=1, max_size=32, psn=None, skip_psn=0):
        if not psn:
            while skip_psn > 0:
                psn = self.mState.GetNextPSN()
                skdebug('skip psn:', psn)
                pkt = LinkPacket.gen_test_packet(TestPktType.TEST_DATA_NONAK, param_dict={LinkSpec.cHFeild_PSN: psn})
                self.mState.StashSentPkt(pkt)
                skip_psn = skip_psn-1
            psn = self.mState.GetNextPSN()
        pdict = {
            LinkSpec.cHFeild_PSN: psn
        }
        skdebug('req_pkt_count:', count, 'req_pkt_maxsize:', max_size)
        pkt = LinkPacket.gen_test_packet(TestPktType.TEST_REQUEST_NONAK, req_pkt_count=count, req_pkt_maxsize=max_size,param_dict=pdict)
        self.mState.StashSentPkt(pkt)
        return self.SendPacket(pkt)

    # def TestRequestMaxCumAckCountNoNAK(self):
    #     pdict = {
    #         LinkSpec.cHFeild_PSN: self.mState.GetNextPSN()
    #     }
    #     pkt = LinkPacket.gen_test_packet(TestPktType.TEST_REQUEST_NONAK, req_pkt_count=self.mMaxCumAck, param_dict=pdict)
    #     self.mState.StashSentPkt(pkt)
    #     return self.SendPacket(pkt)

    def ReceiveOneSpecificPacket(self, type: PacketType, auto_stash=True, timeout=2):
        skdebug('type:', type)
        start_time = time.time()
        while True:
            pkt = self.mSerialPort.RecvPacket()

            # 优先检测是否超时
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('recv packet timeout, cost_time:', cost_time)
                raise RobotTimeoutError

            if pkt:
                if self.IsRepeatSynPacket(pkt):
                    skdebug('find repeat syn pkt, skip')
                    continue
                if PacketTypeMatch(pkt, type):
                    skdebug('recv a packet, type:', type, pkt.info_string())
                    if auto_stash:
                        if IsNoNakPacket(pkt):
                            self.mState.StashRecvPkt(pkt)
                        if IsEakPacket(pkt):
                            self.mState.StashRecvEAKPkt(pkt)
                    return pkt
                else:
                    skdebug('recv a packet, but type not match', pkt.info_string())
                    raise RobotTestFlowException

    def RecviveNothing(self, timeout=2):
        start_time = time.time()
        while True:
            pkt = self.mSerialPort.RecvPacket()
            if pkt:
                skdebug('received a packet', pkt.info_string())
                raise RobotRecvInvalidData
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('timeout cost_time:', cost_time)
                return

    def RecviveTwiceTestNoNAKInTime(self):
        timeout = float(self.mRetransTimeout/1000*1.1)
        skdebug('RecviveTwiceTestNoNAKInTime timeout:', timeout)
        recv_count = 0
        while True:
            pkt_bytes = self.mSerialPort.RecvPacket()
            if pkt_bytes != None:
                skdebug('received a packet')
                link_pkt_obj = LinkPacket(packet_bytes=pkt_bytes, recv_time=time.time())
                if link_pkt_obj.is_nonak_ack_packet():
                    self.mState.StashRecvPkt(link_pkt_obj)
                    skdebug('recv packet is a nonak+ack packet:', link_pkt_obj.info_string())
                    if recv_count == 0:
                        start_time = link_pkt_obj.mRecvTime
                        recv_count = 1
                    elif recv_count == 1:
                        cost_time = link_pkt_obj.mRecvTime - start_time
                        if(cost_time > float(timeout)):
                            skdebug('beyond mRetransTimeout, cost_time:', cost_time)
                            raise RobotTimeoutError
                        else:
                            skdebug('received retransmit packet in', cost_time, 'ms')
                            return link_pkt_obj
                else:
                    skdebug('recv packet is not a nonak+ack packet', link_pkt_obj.info_string())
            cost_time = time.time()-start_time
            if(cost_time > float(timeout)):
                skdebug('timeout cost_time:', cost_time)
                raise RobotTimeoutError


if __name__ == "__main__":
    session = LinkSession(LinkRole.MCU)
    session.OpenPort()

    session.SendRst()
    skdebug('send rst ok')

    try:
        syn_pkt_obj = session.ReceiveOneSpecificPacket(PacketType.SYN)
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
