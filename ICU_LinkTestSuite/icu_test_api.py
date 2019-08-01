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
# def send_syn_packet(**param):
#     for name, value in param.items():
#         skdebug('name:', name, 'value:', value)


class RobotTimeoutError(TimeoutError):
    ROBOT_CONTINUE_ON_FAILURE = True


##########################################################


# def Library_Flush_Transport():
#     flush_serial_transport()


# def Library_Reset_Transport():
#     reset_serial_transport()


# def Library_Send_RST_To_Remote():
#     skdebug('[Library] Send_RST_To_Remote')
#     global Valid_RST_Header_param
#     packet = generate_header_with_param(**Valid_RST_Header_param)
#     send_packet_to_remote(packet)


# def Library_Send_SYN_To_Soc(**param):
#     skdebug('[Library] Send_SYN_Packet_To_Soc')
#     payload = generate_syn_payload_with_param(**param)
#     skdebug('type(payload):', type(payload))
#     payload_len = len(payload)
#     skdebug('payload_len:', payload_len)
#     pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength

#     header_param = dict(SYN=1, PacketLength=pkt_len)
#     # get the PSN from icu_serial
#     header_param['PacketSeqNum'] = get_next_transport_psn()
#     header = generate_header_with_param(**header_param)
#     send_packet_to_remote(header+payload)


# def Library_Send_SYN_ACK_To_SoC(psn):
#     skdebug('[Library] Send_SYN_ACK_To_SoC')
#     global MCU_Negotiated_SYN_Param
#     param = copy.deepcopy(MCU_Negotiated_SYN_Param)
#     param['PacketAckNum'] = int(psn)
#     param['PacketSeqNum'] = get_next_transport_psn()
#     skdebug('MCU_Negotiated_SYN_Param', MCU_Negotiated_SYN_Param)
#     skdebug('param', param)
#     packet = generate_standard_SYN_ACK_packet(**param)
#     packet_param = get_packet_param(packet)
#     skdebug('send packet param:', packet_param)
#     send_packet_to_remote(packet)
#     return packet_param


# def Library_Reply_SYN_ACK_To_Remote(**param):
#     skdebug(sys._getframe().f_code.co_filename)
#     param['PacketAckNum'] = int(param.get('PacketSeqNum', 0))
#     param['PacketSeqNum'] = get_next_transport_psn()
#     packet = generate_standard_SYN_ACK_packet(**param)
#     packet_param = get_packet_param(packet)
#     skdebug('send packet param:', packet_param)
#     send_packet_to_remote(packet)
#     return packet_param


# def Library_Send_NAK_to_Soc(**param):
#     skdebug(sys._getframe().f_code.co_filename)
#     payload = generate_nak_payload_with_param(**param)
#     pkt_len = len(payload)+LinkPacketHeaderLength
#     header_param = dict(NAK=1, PacketLength=pkt_len)
#     header = generate_header_with_param(**header_param)
#     packet = header+payload
#     packet_param = get_packet_param(packet)
#     skdebug('send packet param:', packet_param)
#     send_packet_to_remote(packet)


# def Library_Get_PSN_From_Param(**param):
#     skdebug('[Library] Get_PSN_From_Param')
#     skdebug(sys._getframe().f_code.co_filename)
#     return param['PacketSeqNum']


# def Library_MCU_Can_Accept_SYN_Param(**param):
#     skdebug('[Library] MCU_Can_Accept_SYN_Param')
#     skdebug('syn_param:', param)
#     # for name, value in param.items():
#     #     skdebug('name:', name, 'value:', value)
#     return True


# def Library_Hold_On_A_While():
#     skdebug('[Library] Hold_On_A_While begin')
#     time.sleep(5)
#     skdebug('[Library] Hold_On_A_While end')


# def Library_Receive_SYN_ACK_In_Time(timeout=2, **param):
#     skdebug('[Library] Receive_SYN_ACK_In_Time')
#     start_time = time.time()
#     while True:
#         packet = recv_packet_from_remote()
#         if packet != None:
#             skdebug('received a packet')
#         else:
#             # skdebug('recv timeout and to retry')
#             pass

#         if(time.time()-start_time > float(timeout)):
#             skdebug('timeout')
#             return False
#     return True


# def Library_SYN_Negotiated_Param_Can_Match(**recv_param):
#     skdebug('[Library] SYN_Negotiated_Param_Can_Match')
#     global MCU_Negotiated_SYN_Param
#     skdebug(recv_param)
#     if(recv_param['LinkVersion'] == MCU_Negotiated_SYN_Param['LinkVersion'] and
#             recv_param['RetransTimeout'] == MCU_Negotiated_SYN_Param['RetransTimeout'] and
#             recv_param['CumAckTimeout'] == MCU_Negotiated_SYN_Param['CumAckTimeout'] and
#             recv_param['MaxNumOfRetrans'] == MCU_Negotiated_SYN_Param['MaxNumOfRetrans'] and
#             recv_param['MaxCumAck'] == MCU_Negotiated_SYN_Param['MaxCumAck']):
#         return True
#     return False


# def Library_Receive_SYN_In_Time(timeout=2):
#     skdebug('[Library] Recvive_SYN_In_Time')
#     global Valid_SYN_Header_Param
#     return received_specified_packet_in_time(timeout=2, **Valid_SYN_Header_Param)


# def Library_Received_ACK_In_Time(timeout=2, **param):
#     skdebug('[Library] Received_ACK_In_Time')
#     skdebug('param:', param)
#     global Valid_ACK_Header_Param
#     ack_param = {**Valid_ACK_Header_Param, **{'PacketAckNum': param.get('PacketSeqNum')}}
#     skdebug('Valid_ACK_Header_Param:', Valid_ACK_Header_Param)
#     skdebug('ack_param:', ack_param)
#     return received_specified_packet_in_time(timeout=2, **ack_param)


# def Library_Receive_Nothing_In_Time(timeout=2):
#     skdebug('[Library] Receive_Nothing_In_Time')
#     start_time = time.time()
#     while True:
#         packet = recv_packet_from_remote()
#         if packet != None:
#             return False
#         cost_time = time.time()-start_time
#         if(cost_time > float(timeout)):
#             skdebug('timeout cost_time:', cost_time)
#             skdebug('[Library] Receive_Nothing_In_Time Succeed')
#             return True


# def Library_Set_MCU_Default_Param(**param):
#     skdebug('[Library] Set_MCU_Default_Param')
#     global MCU_Default_SYN_Param
#     skdebug('param:', param)
#     MCU_Default_SYN_Param.clear()
#     MCU_Default_SYN_Param = {**param}
#     skdebug('MCU_Default_SYN_Param:', MCU_Default_SYN_Param)


# def Library_Set_MCU_Negotiated_Param(**param):
#     skdebug('[Library] Set_MCU_Negotiated_Param')
#     global MCU_Negotiated_SYN_Param
#     skdebug('param:', param)
#     MCU_Negotiated_SYN_Param.clear()
#     MCU_Negotiated_SYN_Param = {**param}
#     skdebug('MCU_Negotiated_SYN_Param:', MCU_Negotiated_SYN_Param)

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
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Update_Invalid_SYN_Negotiable_Param begin')
    session.UpdateSynNegotiableParam(rt=10)


def Library_Send_RST():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendRst()
    sk_library_api_end()


def Library_Send_Random_EAK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_EAK begin')
    session.SendRandomEak()


def Library_Send_SYN():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_SYN begin')
    session.SendSyn()


def Library_Send_SYN_ACK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_SYN_ACK begin')
    session.SendSynAck()


def Library_Send_ACK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_ACK begin')
    session.SendAck()


def Library_Send_NAK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_NAK begin')
    session.SendNak()


def Library_Send_APP():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_APP begin')
    session.SendApp()


def Library_Send_BAD_PKT_INVALID_SOP():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_SOP_PKT begin')
    session.SendBadPkt(BadPktType.BAD_SOP)


def Library_Send_BAD_CB_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_CB_PKT begin')
    session.SendBadPkt(BadPktType.BAD_CB)


def Library_Send_BAD_PL_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PL_PKT begin')
    session.SendBadPkt(BadPktType.BAD_PL)


def Library_Send_BAD_PL_2_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PL_2_PKT begin')
    session.SendBadPkt(BadPktType.BAD_PL_2)


def Library_Send_BAD_PAN_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PAN_PKT begin')
    session.SendBadPkt(BadPktType.BAD_PAN)


def Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PSN_PKT begin')
    session.SendBadPkt(BadPktType.PSN_OUT_OF_RECV_WIN)


def Library_Send_BAD_PKT_WITH_NONEED_PAN():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_WITH_NONEED_PAN_PKT begin')
    session.SendBadPkt(BadPktType.WITH_NONEED_PAN)


def Library_Send_BAD_PKT_INVALID_ACK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PKT_INVALID_ACK begin')
    session.SendBadPkt(BadPktType.INVALID_ACK)


def Library_Send_BAD_PKT_INVALID_SESSION_ID():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PKT_INVALID_SESSION_ID begin')
    session.SendBadPkt(BadPktType.INVALID_SESSION_ID)


def Library_Send_BAD_PKT_INCORRECT_HC():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PKT_INCORRECT_HC begin')
    session.SendBadPkt(BadPktType.INCORRECT_HC)


def Library_Send_BAD_PKT_INCORRECT_PC():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PKT_INCORRECT_PC begin')
    session.SendBadPkt(BadPktType.INCORRECT_PC)


def Library_Send_BAD_PKT_SYN_INVALID_DATA():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_BAD_PKT_SYN_INVALID_DATA begin')
    session.SendBadPkt(BadPktType.SYN_INVALID_DATA)


def Library_Send_OverLength_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Send_OverLength_PKT begin')
    session.SendBadPkt(BadPktType.OVER_MAX_LEN)


def Library_Send_BAD_PKT_OVER_MAX_RECV_LEN_TEST_NONAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.SendBadPkt(BadPktType.OVER_MAX_RECV_LEN_TEST_NONAK)
    sk_library_api_end()


def Library_Received_Acceptable_SYN_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.CanAccpetSynParam(lsp):
        skdebug('not a acceptable syn param')
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Acceptable_SYN_ACK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.SYN_ACK)
    lsp = LinkSynPayload(payload_bytes=pkt.mPayloadBytes)
    if not session.CanAccpetSynParam(lsp):
        skdebug('not a acceptable syn param')
        raise RobotTestFlowException
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
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Reply_SYN begin')
    session.ReplySyn()


def Library_Retransmit_SYN_ACK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Retransmit_SYN_ACK begin')
    session.RetransmitSynAck()


def Library_Retransmit_Previous_NoNAK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Retransmit_Previous_NoNAK begin')
    session.RetransmitPreviousNoNAK()


def Library_Retransmit_First_NoNAK_In_SentQ():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Retransmit_First_NoNAK_In_SentQ begin')
    session.RetransmitFirstNoNAKInSentQ()


def Library_Send_Negotiated_SYN_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ForceNegotiateSyn()
    sk_library_api_end()


def Library_Received_EAK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.EAK)
    eakp = LinkEAKPayload(payload_bytes=pkt.mPayloadBytes)
    sk_library_api_end()


def Library_Received_ACK_In_Time():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.ACK)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Nothing_In_Time():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Received_Nothing_In_Time begin')
    session.RecviveNothing(timeout=2)


def Library_Received_Test_NoNAK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.ReceiveOneSpecificPacket(PacketType.NoNAK)
    sk_library_api_end()


def Library_Received_Test_NoNAK_With_ACK():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    pkt = session.ReceiveOneSpecificPacket(PacketType.NoNAK_ACK)
    if not session.IsValidPan(pkt.mHeader.mPacketAckNum):
        raise RobotTestFlowException
    sk_library_api_end()


def Library_Received_Twice_Test_NoNAK_ACK_In_LimitTime():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    # session.RecviveTwiceTestNoNAKInTime()

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


def Library_Received_MaxCumAckCount_Test_NoNAK():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Received_MaxCumAckCount_NoNAK begin')
    session.RecviveMaxCumAckCountTestNoNAKWithAck(timeout=2)


def Library_SYN_Complete():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] SYN_Completed begin')
    session.SynCompete()


def Library_Test_Start():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Test_Start begin')
    session.TestStart()


def Library_Test_Send_NoNAK_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestSendNoNAK()
    sk_library_api_end()


def Library_Test_Send_NoNAK_PKT_SKIP_ONE_PSN():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    session.TestSendNoNAK(skip_psn=1)
    sk_library_api_end()


def Library_Test_Send_MNOOSP_NoNAK_PKT():
    sk_library_api_begin()
    session: LinkSession = LinkSession.GetInstance()
    skdebug('MaxCumAck:', session.mState.mRemoteMaxNumOfOutStdPkts)
    for i in range(0, session.mState.mRemoteMaxNumOfOutStdPkts):
        skdebug('TestSendNoNAK send ndx:', i)
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


def Library_Test_Request_NoNAK_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Test_Request_NoNAK_PKT begin')
    session.TestRequestNoNAK()


def Library_Test_Request_MaxCumAckCount_NoNAK_PKT():
    session: LinkSession = LinkSession.GetInstance()
    skdebug('[Library] Test_Request_MaxCumAckCount_NoNAK_PKT begin')
    session.TestRequestMaxCumAckCountNoNAK()


def Library_MCU_SYN():
    skdebug('[Library] MCU_SYN begin')
    Library_Send_RST()
    Library_Received_Acceptable_SYN_In_Time()
    Library_Reply_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()
    Library_SYN_Complete()
    skdebug('[Library] MCU_SYN end')

# def packet_param_match(expectation: dict, received: dict):
#     for key, value in expectation.items():
#         if key in received:
#             if int(value) == int(received.get(key)):
#                 pass
#             else:
#                 skdebug('mismatch:', key, value, received.get(key))
#                 return False
#         else:
#             pass
#     return True


# def received_specified_packet_in_time(timeout, **expectation_param):
#     skdebug('received_specified_packet_in_time')
#     skdebug('expectation_param:', expectation_param)
#     start_time = time.time()
#     while True:
#         packet = recv_packet_from_remote()
#         if packet != None:
#             skdebug('received a packet, get param and check')
#             pkt_param = get_packet_param(packet)
#             skdebug('received packet param:', pkt_param)
#             if packet_param_match(expectation_param, pkt_param):
#                 skdebug('packet match success')
#                 return pkt_param
#         cost_time = time.time()-start_time
#         if(cost_time > float(timeout)):
#             skdebug('timeout cost_time:', cost_time)
#             raise RobotTimeoutError
if __name__ == "__main__":
    # test_syn_once_success()
    # test_syn_twice_success()
    # test_syn_once_insert_nak()
    # test_syn_twice_fail()
    pass
