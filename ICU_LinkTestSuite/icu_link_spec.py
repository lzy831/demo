#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple

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



    cTestSession_CmdID_RequestData = 0x2

    cHFeild_TestCommondID = 'TestCmdID'
    cHFeild_NoNakCount = 'NoNakCount'
    cHFeild_NoNakPayloadMaxSize = 'NoNakPayloadMaxSize'

    cLinkTestSession_RequestData_Format = '>BBH'
    cLinkTestSession_RequestData_Field = cHFeild_TestCommondID+' '+cHFeild_NoNakCount+' '+cLinkTestSession_RequestData_Format
    cLinkTestSession_RequestData_TupleType = namedtuple('TestSessionRequestDataTuple', cLinkTestSession_RequestData_Field)