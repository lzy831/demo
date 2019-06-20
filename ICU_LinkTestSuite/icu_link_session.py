#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from enum import Enum
from icu_serial_port import SerialPort


class LinkRole(Enum):
    UnKnown = 0
    MCU = 1
    SoC = 2


class LinkSession(object):
    def __init__(self, role):
        self.mSerialPort = SerialPort(1,115200)
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
        self.mSerialPort.open()

    def ClosePort(self):
        self.mSerialPort.close()

    def SendRst(self):
        self.mSerialPort.send_packet( )
        pass

    def SendSyn(self):

        pass

    def RecviveSynAck(self, timeout=2):
        pass

    def RecviveAck(self, timeout=2):
        pass
