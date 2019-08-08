#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import copy
from robot.api.deco import keyword
from icu_link_session import *
from icu_link_packet import *
from icu_serial_port import *
from icu_debug import *

##########################################################
# @keyword('Ba La Ba La')
# def example_keyword():
# 	skdebug('Hello, world!')
##########################################################


def Library_Open_Transport():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Open_Transport begin')
    session.OpenPort()


def Library_Close_Transport():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Close_Transport begin')
    session.ClosePort()


def Library_Reset_For_Soc():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Reset_For_Soc begin')
    session.Reset(role=LinkRole.SoC)


def Library_Reset_For_MCU():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Reset_For_MCU begin')
    session.Reset(role=LinkRole.MCU)


def Library_Update_SYN_Negotiable_Param():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Update_SYN_Negotiable_Param begin')
    session.UpdateSynNegotiableParam()


def Library_Update_Invalid_SYN_Negotiable_Param():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.UpdateSynNegotiableParam(rt=10)
    sk_library_api_end()


def Library_MCU_SYN():
    sk_library_api_begin()
    Library_Send_RST()
    Library_Received_Acceptable_SYN_In_Time()
    Library_Reply_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()
    Library_SYN_Complete()
    sk_library_api_end()


def Library_Wait():
    sk_library_api_begin()
    time.sleep(2)
    sk_library_api_end()
##############################################################################################################
##############################################################################################################


def Library_Send_RST():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.StateReset()
    session.SendRst()
    sk_library_api_end()


def Library_Send_Random_EAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendRandomEak()
    sk_library_api_end()


def Library_Send_SYN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendSyn()
    sk_library_api_end()


def Library_Send_SYN_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendSyn(skip_psn=1)
    sk_library_api_end()


def Library_Send_SYN_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendSynAck()
    sk_library_api_end()


def Library_Send_SYN_ACK_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendSynAck(skip_psn=1)
    sk_library_api_end()


def Library_Send_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendAck()
    sk_library_api_end()


def Library_Send_NAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendNak()
    sk_library_api_end()


def Library_Send_APP():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendApp()
    sk_library_api_end()


def Library_Send_EAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendEAK()
    sk_library_api_end()

##############################################################################################################
##############################################################################################################


def Library_Send_BAD_PKT_INVALID_SOP():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_SOP)
    sk_library_api_end()


def Library_Send_BAD_PKT_INVALID_CB():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_CB)
    sk_library_api_end()


def Library_Send_BAD_CB_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.BAD_CB)
    sk_library_api_end()


def Library_Send_BAD_PKT_EAK_INVALID_PL_LTA():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.EAK_INVALID_PL_LESS_THEN_ACTUAL)
    sk_library_api_end()


def Library_Send_BAD_PKT_EAK_INVALID_PL_MTA():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.EAK_INVALID_PL_MORE_THEN_ACTUAL)
    sk_library_api_end()


def Library_Send_BAD_PKT_INVALID_PL_MTA():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_PL_MORE_THEN_ACTUAL)
    sk_library_api_end()


def Library_Send_BAD_PKT_INVALID_PL_LTA():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_PL_LESS_THEN_ACTUAL)
    sk_library_api_end()


def Library_Send_BAD_PAN_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.BAD_PAN)
    sk_library_api_end()


def Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.PSN_OUT_OF_RECV_WIN)
    sk_library_api_end()


def Library_Send_BAD_PKT_WITH_NONEED_PAN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.WITH_NONEED_PAN)
    sk_library_api_end()


def Library_Send_BAD_PKT_INVALID_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_ACK)
    sk_library_api_end()


def Library_Send_BAD_PKT_INVALID_SESSION_ID():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INVALID_SESSION_ID)
    sk_library_api_end()


def Library_Send_BAD_PKT_Incorrect_HC():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INCORRECT_HC)
    sk_library_api_end()


def Library_Send_BAD_PKT_Incorrect_PC():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.INCORRECT_PC)
    sk_library_api_end()


def Library_Send_BAD_PKT_SYN_Invalid_Data():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.SYN_INVALID_DATA)
    sk_library_api_end()


def Library_Send_BAD_PKT_SYN_Invalid_Data_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.SYN_INVALID_DATA_SKIP_ONE_PSN)
    sk_library_api_end()


def Library_Send_BAD_PKT_SYN_ACK_Invalid_Data():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.SYN_ACK_INVALID_DATA)
    sk_library_api_end()


def Library_Send_Bad_Pkt_OverLength():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.OVER_MAX_LEN)
    sk_library_api_end()


def Library_Send_BAD_PKT_OVER_MAX_RECV_LEN_TEST_NONAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.OVER_MAX_RECV_LEN_TEST_NONAK)
    sk_library_api_end()


def Library_Send_BAD_PKT_RST_With_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(type=BadPktType.RST_WITH_PSN)
    sk_library_api_end()


def Library_Send_BAD_PKT_RST_With_PAN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(type=BadPktType.RST_WITH_PAN)
    sk_library_api_end()


def Library_Send_BAD_PKT_RST_With_INCORRECT_PL():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(type=BadPktType.RST_WITH_INCORRECT_PL)
    sk_library_api_end()


##############################################################################################################
##############################################################################################################


def Library_Received_Acceptable_SYN_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.CanAccpetSynParam(lsp):
        skdebug('not a acceptable syn param')
        raise RobotTestFlowException
    session.StashRemoteLinkParam(lsp.mMaxRecvPktLen, lsp.mMaxNumOfOutStdPkts)
    sk_library_api_end()


def Library_Received_Acceptable_SYN_ACK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN_ACK)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.CanAccpetSynParam(lsp):
        skdebug('not a acceptable syn param')
        raise RobotTestFlowException
    session.StashRemoteLinkParam(lsp.mMaxRecvPktLen, lsp.mMaxNumOfOutStdPkts)
    sk_library_api_end()


def Library_Received_Negotiable_SYN_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.IsNegotiableSynParam(lsp):
        skdebug('not a negotiable syn param')
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Repeat_SYN_In_Time():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Received_Repeat_SYN_In_Time begin')
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.IsRepeatSynParam(lsp):
        raise RobotTestFlowException


def Library_Reply_SYN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ReplySyn()
    sk_library_api_end()


def Library_Retransmit_SYN_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.RetransmitSynAck()
    sk_library_api_end()


def Library_Retransmit_Previous_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.RetransmitPreviousNoNAK()
    sk_library_api_end()


def Library_Retransmit_First_NoNAK_In_SentQ():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.RetransmitFirstNoNAKInSentQ()
    sk_library_api_end()


def Library_Retransmit_Third_NoNAK_In_SentQ():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.RetransmitThirdNoNAKInSentQ()
    sk_library_api_end()


def Library_Send_Negotiated_SYN_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ForceNegotiateSyn()
    sk_library_api_end()


def Library_Received_EAK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ReceiveOneSpecificPacket(PacketType.EAK)
    sk_library_api_end()


def Library_Received_ACK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.ACK)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Nothing_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.RecviveNothing(timeout=2)
    sk_library_api_end()


##############################################################################################################
##
##############################################################################################################


def Library_Test_Send_NoNAK_PKT_And_Received_ACK_In_LimitTime():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()

    sent_pkt = session.TestSendNoNAK()
    skdebug('send time:', sent_pkt.mSentTime)

    recv_pkt = session.ReceiveOneSpecificPacket(type=PacketType.ACK)
    if not session.IsValidPan(recv_pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    skdebug('recv time:', recv_pkt.mRecvTime)
    diff_time = (recv_pkt.mRecvTime - sent_pkt.mSentTime)*1000

    skdebug('diff time:', diff_time)
    limit = session.mCumAckTimeout
    skdebug('limit:', limit)
    if(diff_time > limit):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Send_OutSeq_NoNAK_Pkt_And_Received_EAK_In_LimitTime():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()

    sent_pkt = session.TestSendNoNAK(skip_psn=1)
    skdebug('send time:', sent_pkt.mSentTime)

    recv_pkt = session.ReceiveOneSpecificPacket(type=PacketType.EAK)
    if not session.IsValidPan(recv_pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    skdebug('recv time:', recv_pkt.mRecvTime)
    diff_time = (recv_pkt.mRecvTime - sent_pkt.mSentTime)*1000

    skdebug('diff time:', diff_time)
    limit = session.mCumAckTimeout
    skdebug('limit:', limit)
    if(diff_time > limit):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Send_NoNAK_Pkt_And_Received_EAK_In_LimitTime():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()

    sent_pkt = session.TestSendNoNAK()
    skdebug('send time:', sent_pkt.mSentTime)

    recv_pkt = session.ReceiveOneSpecificPacket(type=PacketType.EAK)
    if not session.IsValidPan(recv_pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    skdebug('recv time:', recv_pkt.mRecvTime)
    diff_time = (recv_pkt.mRecvTime - sent_pkt.mSentTime)*1000

    skdebug('diff time:', diff_time)
    limit = session.mCumAckTimeout
    skdebug('limit:', limit)
    if(diff_time > limit):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_MaxCumAckCount_Test_NoNAK():
    sk_library_api_begin()
    start_time = time.time()
    session: LinkSession = LinkSession.GetInstance()
    max_cum_ack = session.GetNegotiatedMaxCumAck()
    skdebug('need recv nonak count:', max_cum_ack)
    while max_cum_ack > 0:
        session.ReceiveOneSpecificPacket(type=PacketType.NoNAK)
        max_cum_ack = max_cum_ack - 1
        skdebug('need recv nonak count:', max_cum_ack)
    cost_time = time.time()-start_time
    if cost_time > 2:
        raise RobotTimeoutError
    sk_library_api_end()


def Library_Test_Received_Missing_NoNAK():
    sk_library_api_begin()
    start_time = time.time()
    session: LinkSession = LinkSession.GetInstance()
    sent_eak = session.GetSentEAKPkt()
    eak_payload = LinkEAKPayload(
        pan=sent_eak.pan(), payload_bytes=sent_eak.mPayloadBytes)
    psn_list = eak_payload.get_missing_psn_list()
    skdebug('psn_list:', psn_list)
    wait_psn_queue = collections.deque()
    for psn in psn_list:
        wait_psn_queue.append(psn)
    while len(wait_psn_queue) > 0:
        pkt = session.ReceiveOneSpecificPacket(type=PacketType.NoNAK)
        wait_psn_queue.remove(pkt.psn())
        skdebug('wait_psn_queue:', wait_psn_queue)
    cost_time = time.time()-start_time
    if cost_time > 2:
        raise RobotTimeoutError
    sk_library_api_end()


def Library_Test_Received_Missing_NoNAK_With_ACK():
    sk_library_api_begin()
    start_time = time.time()
    session: LinkSession = LinkSession.GetInstance()
    sent_eak = session.GetSentEAKPkt()
    eak_payload = LinkEAKPayload(
        pan=sent_eak.pan(), payload_bytes=sent_eak.mPayloadBytes)
    psn_list = eak_payload.get_missing_psn_list()
    skdebug('psn_list:', psn_list)
    wait_psn_queue = collections.deque()
    for psn in psn_list:
        wait_psn_queue.append(psn)
    while len(wait_psn_queue) > 0:
        pkt = session.ReceiveOneSpecificPacket(type=PacketType.NoNAK_ACK)
        if pkt.pan() != session.GetLastSentPSN():
            raise RobotTestFlowException
        wait_psn_queue.remove(pkt.psn())
        skdebug('wait_psn_queue:', wait_psn_queue)
    cost_time = time.time()-start_time
    if cost_time > 2:
        raise RobotTimeoutError
    sk_library_api_end()


def Library_SYN_Complete():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SynCompete()
    sk_library_api_end()


def Library_Test_Start():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestStart()
    pkt = session.ReceiveOneSpecificPacket(PacketType.ACK)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Send_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestSendNoNAK()
    sk_library_api_end()


def Library_Send_Test_NoNAK_Pkt_Out_Of_Recv_Win():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    first_psn_in_sendQ = session.GetFirstSentPSN()
    skdebug('first_psn_in_sendQ:', first_psn_in_sendQ)
    psn = (first_psn_in_sendQ+255-session.mState.mLocalMaxNumOfOutStdPkts) % 256
    skdebug('psn:', psn)
    session.TestSendNoNAKSpecifiedPSN(specified_psn=psn)
    sk_library_api_end()


def Library_Send_Test_Missing_NoNAK_Pkt_According_EAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt: LinkPacket = session.GetRecvEAKPkt()
    ekap = LinkEAKPayload(pan=pkt.pan(), payload_bytes=pkt.mPayloadBytes)
    l = ekap.get_missing_psn_list()
    skdebug('missing psn list:', l)
    session.TestSendRetransmitNoNAK(psn_list=l)
    sk_library_api_end()


def Library_Send_Test_NoNAK_Pkt_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestSendNoNAK(skip_psn=1)
    sk_library_api_end()


def Library_Send_Test_NoNAK_SendQ_First_PSN_Munis_One():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    first_psn_in_sendQ = session.GetFirstSentPSN()
    skdebug('first_psn_in_sendQ:', first_psn_in_sendQ)
    psn = (first_psn_in_sendQ+255) % 256
    skdebug('psn:', psn)
    session.TestSendNoNAKSpecifiedPSN(specified_psn=psn)
    sk_library_api_end()


def Library_Send_Test_MNOOSP_NoNAK_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    skdebug('LocalMaxNumOfOutStdPkts:', session.mState.mLocalMaxNumOfOutStdPkts)
    for i in range(1, session.mState.mLocalMaxNumOfOutStdPkts):
        skdebug('TestSendNoNAK send ndx:', i)
        session.TestSendNoNAK()
    sk_library_api_end()


def Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    skdebug('LocalMaxNumOfOutStdPkts:', session.mState.mLocalMaxNumOfOutStdPkts)
    session.TestSendNoNAK()
    skip_psn_flag = 1
    for i in range(1, session.mState.mLocalMaxNumOfOutStdPkts-1):
        skdebug('TestSendNoNAK send ndx:', i)
        if skip_psn_flag == 1:
            session.TestSendNoNAK(skip_psn=1)
            skip_psn_flag = 0
        else:
            session.TestSendNoNAK()
    sk_library_api_end()


def Library_Test_Send_MCA_NoNAK_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    skdebug('MaxCumAck:', session.mMaxCumAck)
    for i in range(0, session.mMaxCumAck):
        skdebug('TestSendNoNAK send ndx:', i)
        session.TestSendNoNAK()
    sk_library_api_end()

##############################################################################################################
# 请求测试数据包
##############################################################################################################


def Library_Request_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK()
    sk_library_api_end()


def Library_Request_Two_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK(count=2)
    sk_library_api_end()


def Library_Request_Three_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK(count=3)
    sk_library_api_end()


def Library_Request_MaxCumAckCount_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK(count=session.mState.mNegotiatedMaxCumAck)
    sk_library_api_end()


def Library_Request_MaxOutOfStdPkt_Add_Two_Test_NoNAK_Pkt():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK(count=session.mState.mRemoteMaxNumOfOutStdPkts+2)
    sk_library_api_end()


def Library_Request_Test_NoNAK_Pkt_Skip_One_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestRequestNoNAK(count=1, skip_psn=1)
    sk_library_api_end()

##############################################################################################################
# 接收测试NoNAK数据包
##############################################################################################################


def Library_Received_Test_NoNAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ReceiveOneSpecificPacket(PacketType.NoNAK)
    sk_library_api_end()


def Library_Received_Test_NoNAK_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.NoNAK_ACK)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Test_NoNAK_ACK_And_Drop():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(
        PacketType.NoNAK_ACK, auto_stash=False)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_MaxOutOfStdPkt_Test_NoNAK_And_Drop_First():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    need_recv_count = session.mState.mRemoteMaxNumOfOutStdPkts
    skdebug('need to recv packet count:', need_recv_count)
    session.ReceiveOneSpecificPacket(type=PacketType.NoNAK, auto_stash=False)
    need_recv_count = need_recv_count - 1
    while need_recv_count > 0:
        skdebug('need to recv packet count:', need_recv_count)
        session.ReceiveOneSpecificPacket(type=PacketType.NoNAK)
        need_recv_count = need_recv_count - 1
    sk_library_api_end()


def Library_Received_Twice_Test_NoNAK_ACK_In_LimitTime():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    first_pkt = session.ReceiveOneSpecificPacket(type=PacketType.NoNAK)
    second_pkt = session.ReceiveOneSpecificPacket(type=PacketType.NoNAK)
    skdebug('1th pkt recv time:', first_pkt.mRecvTime)
    skdebug('2th pkt recv time:', second_pkt.mRecvTime)
    diff_time = (second_pkt.mRecvTime - first_pkt.mRecvTime)*1000
    skdebug('diff time:', diff_time)
    limit = session.mRetransTimeout*1.1
    skdebug('limit:', limit)
    if(diff_time > limit):
        raise RobotTestFlowException
    sk_library_api_end()


##############################################################################################################
##############################################################################################################
if __name__ == "__main__":
    # test_syn_once_success()
    # test_syn_twice_success()
    # test_syn_once_insert_nak()
    # test_syn_twice_fail()
    pass
