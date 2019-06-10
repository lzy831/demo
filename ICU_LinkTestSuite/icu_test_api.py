#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from robot.api.deco import keyword
from icu_link_packet import *
from icu_serial import *
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
def Library_Open_Transport():
    logger.info('Library_Open_Transport')
    return open_serial_transport()


def Library_Close_Transport():
    logger.info('Library_Close_Transport')
    return close_serial_transport()


def Library_Flush_Transport():
    flush_serial_transport()


def Library_Reset_Transport():
    reset_serial_transport()


def Library_Send_RST_To_Remote():
    logger.info('Library_Send_RST_To_Remote')
    global Valid_RST_Header_param
    packet = generate_header_with_param(**Valid_RST_Header_param)
    send_packet_to_remote(packet)


def Library_Send_SYN_To_Soc(**param):
    logger.info('Library_Send_SYN_Packet_To_Soc')
    payload = generate_syn_payload_with_param(**param)
    skdebug('type(payload):', type(payload))
    payload_len = len(payload)
    skdebug('payload_len:', payload_len)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = get_next_transport_psn()
    header = generate_header_with_param(**header_param)
    send_packet_to_remote(header+payload)


def Library_Send_SYN_ACK_To_Soc(**param):
    logger.info('Library_Send_SYN_ACK_To_Remote')
    global MCU_Default_SYN_Param
    syn_ack_param = dict()
    syn_ack_param['MaxNumOfOutStdPkts'] = int(
        MCU_Default_SYN_Param.get('MaxNumOfOutStdPkts', 4))
    syn_ack_param['MaxRecvPktLen'] = int(
        MCU_Default_SYN_Param.get('MaxRecvPktLen', 256))
    syn_ack_param['RetransTimeout'] = int(
        MCU_Default_SYN_Param.get('RetransTimeout', 400))
    syn_ack_param['CumAckTimeout'] = int(param.get('CumAckTimeout', 22))
    syn_ack_param['MaxCumOfRetrans'] = int(param.get('MaxCumOfRetrans', 10))
    syn_ack_param['MaxCumAck'] = int(param.get('MaxCumAck', 10))
    payload = generate_syn_payload_with_param(**syn_ack_param)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, ACK=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = get_next_transport_psn()
    header_param['PacketAckNum'] = int(param.get('PacketSeqNum', 0))
    header = generate_header_with_param(**header_param)
    packet = header+payload

    packet_param = get_packet_param(packet)
    skdebug('send packet param:', packet_param)
    send_packet_to_remote(packet)
    return packet_param


def Library_Send_NAK_to_Soc(**param):
    logger.info('Library_Send_NAK_to_Soc')
    payload = generate_nak_payload_with_param(**param)
    pkt_len = len(payload)+LinkPacketHeaderLength
    header_param = dict(NAK=1, PacketLength=pkt_len)
    header = generate_header_with_param(**header_param)
    packet = header+payload
    packet_param = get_packet_param(packet)
    skdebug('send packet param:', packet_param)
    send_packet_to_remote(packet)


def Library_MCU_Can_Accept_SYN_Param(**param):
    skdebug('Library_MCU_Can_Accept_SYN_Param')
    skdebug('syn_param:', param)
    # for name, value in param.items():
    #     skdebug('name:', name, 'value:', value)
    return True


def Library_Hold_On_A_While():
    logger.info('Library_Hold_On_A_While begin')
    time.sleep(5)
    logger.info('Library_Hold_On_A_While end')


def Library_Receive_SYN_ACK_In_Time(timeout=2, **param):
    logger.info('Library_Receive_SYN_ACK_In_Time')
    start_time = time.time()
    while True:
        packet = recv_packet_from_remote()
        if packet != None:
            skdebug('received a packet')
        else:
            # skdebug('recv timeout and to retry')
            pass

        if(time.time()-start_time > float(timeout)):
            skdebug('timeout')
            return False
    return True


def Library_Receive_SYN_In_Time(timeout=2):
    logger.info('Library_Recvive_SYN_In_Time')
    global Valid_SYN_Header_Param
    return received_specified_packet_in_time(timeout=2, **Valid_SYN_Header_Param)


def Library_Receive_ACK_In_Time(timeout=2, **param):
    # logger.console('Library_Receive_ACK_In_Time')
    logger.info('Library_Receive_ACK_In_Time')
    skdebug('param:', param)
    global Valid_ACK_Header_Param
    ack_param = {**Valid_ACK_Header_Param, **
                 {'PacketAckNum': param.get('PacketSeqNum')}}
    skdebug('Valid_ACK_Header_Param:', Valid_ACK_Header_Param)
    skdebug('ack_param:', ack_param)
    received_specified_packet_in_time(timeout=2, **ack_param)


def Library_Receive_Nothing_In_Time(timeout=2):
    logger.info('Library_Receive_Nothing_In_Time')
    start_time = time.time()
    while True:
        packet = recv_packet_from_remote()
        if packet != None:
            return False
        cost_time = time.time()-start_time
        if(cost_time > float(timeout)):
            skdebug('timeout cost_time:', cost_time)
            return True


def Library_Set_MCU_Default_Param(**param):
    logger.info('Library_Set_MCU_Default_Param')
    global MCU_Default_SYN_Param
    skdebug('param:', param)
    MCU_Default_SYN_Param.clear()
    MCU_Default_SYN_Param = {**param}
    skdebug('MCU_Default_SYN_Param:', MCU_Default_SYN_Param)


def packet_param_match(expectation: dict, received: dict):
    for key, value in expectation.items():
        if key in received:
            if int(value) == int(received.get(key)):
                pass
            else:
                skdebug('mismatch:', key, value, received.get(key))
                return False
        else:
            pass
    return True


def received_specified_packet_in_time(timeout, **expectation_param):
    skdebug('received_specified_packet_in_time')
    skdebug('expectation_param:', expectation_param)
    start_time = time.time()
    while True:
        packet = recv_packet_from_remote()
        if packet != None:
            skdebug('received a packet, get param and check')
            pkt_param = get_packet_param(packet)
            skdebug('received packet param:', pkt_param)
            if packet_param_match(expectation_param, pkt_param):
                skdebug('packet match success')
                return pkt_param
        cost_time = time.time()-start_time
        if(cost_time > float(timeout)):
            skdebug('timeout cost_time:', cost_time)
            raise RobotTimeoutError


def test():
    global LINK_PKT_MAX_PSN
    skdebug(LINK_PKT_MAX_PSN)
    # Library_Open_Transport()
    # Library_Recvive_SYN_In_Time()
    # Library_Close_Transport()
    # Library_Send_SYN_Packet_To_Remote(MaxNumOfPkt=5,MaxRevPktLen=2048,RetransTimeout=400,CumAckTimeout=22,MaxCumOfRetrans=10,MaxCumAck=3)
    # Library_Recvive_SYN_Response_In_Time(3)
    # skdebug(get_default_header_bytes_array())
    # b = BitSet(8)
    # b.set(BIT_SYN)
    # b.set(BIT_ACK)
    # skdebug(b.size())
    # skdebug(b.binstr())
    # skdebug(b.to_integer())
