
from enum import Enum
import random


class LinkRole(Enum):
    UnKnown = 0
    MCU = 1
    SoC = 2


class LinkSession(object):
    def __init__(self, role):
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
        pass

    def ClosePort(self):
        pass

    def SendRst(self):
        pass

    def SendSyn(self):
        pass

    def RecviveSynAck(self, timeout=2):
        pass

    def RecviveAck(self, timeout=2):
        pass
