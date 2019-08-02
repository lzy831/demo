import collections
import random

from icu_debug import *
from icu_error import *
from icu_link_packet import *


class SessionState(object):
    def __init__(self):
        self.mSendQMaxSize = 1
        self.mRecvQMaxSize = 1
        self.mSendQueue = collections.deque(maxlen=1)
        self.mRecvQueue = collections.deque(maxlen=1)
        self.mRecvOutSeqQueue = collections.deque()
        self.mNextSendPSN = random.randint(0, 255)
        self.mRecvEAK = None
        self.mSentEAK = None
        self.mRemoteMaxRecvPktLen = 128
        self.mRemoteMaxNumOfOutStdPkts = 4


    def Update(self, param_dict):

        # self.mLocalMaxNumOfOutStdPkts
        # self.mRemoteMaxNumOfOutStdPkts
        # self.mRemoteMaxRecvPktLen


        self.mLinkVersion = param_dict[LinkSpec.cHFeild_LV]
        self.mNegotiatedRetransTimeout = param_dict[LinkSpec.cHFeild_RT]
        self.mNegotiatedCumAckTimeout = param_dict[LinkSpec.cHFeild_CAT]
        self.mNegotiatedMaxNumOfRetrans = param_dict[LinkSpec.cHFeild_MNOR]
        self.mNegotiatedMaxCumAck = param_dict[LinkSpec.cHFeild_MCA]

        self.mSendQMaxSize = self.mLocalMaxNumOfOutStdPkts
        tmp = collections.deque(maxlen=self.mSendQMaxSize)
        while len(self.mSendQueue) > 0:
            pkt = self.mSendQueue.popleft()
            skdebug('sendQ popleft:', pkt.mHeader.mPacketSeqNum)
            tmp.append(pkt)
        self.mSendQueue = tmp

        self.mRecvQMaxSize = self.mNegotiatedMaxCumAck
        tmp = collections.deque(maxlen=self.mRecvQMaxSize)
        while len(self.mRecvQueue) > 0:
            pkt = self.mRecvQueue.popleft()
            skdebug('recvQ popleft:', pkt.mHeader.mPacketSeqNum)
            tmp.append(pkt)
        self.mRecvQueue = tmp
        skdebug('Update mSendQueue:', self.mSendQueue)
        skdebug('Update mRecvQueue:', self.mRecvQueue)
        self.mRecvOutSeqQueue.clear()
        pass

    def GetNextPSN(self, autoplus=True):
        np = self.mNextSendPSN
        skdebug('GetNextPSN np:', np)
        if autoplus:
            self.mNextSendPSN = (self.mNextSendPSN + 1) % 256
        return np

    def IsValidPan(self, pan):
        for i in range(len(self.mSendQueue)):
            pkt: LinkPacket = self.mSendQueue[i]
            skdebug('IsValidPan, check psn', pkt.mHeader.mPacketSeqNum)
            if pkt.mHeader.mPacketSeqNum == pan:
                return True
        skdebug('IsValidPan, not a valid pan', pan)
        return False

    def StashRecvPkt(self, packet: LinkPacket):
        if len(self.mRecvQueue) == 0 or packet.psn() == self.mRecvQueue[-1].psn()+1:
            self.mRecvQueue.append(packet)
            qs = ''
            for p in self.mRecvQueue:
                qs = qs + str(p.psn())+','
            skdebug('stash a in seq pkt, size:', len(self.mRecvQueue), '/', self.mRecvQueue.maxlen, ' > ', qs)
        else:
            self.mRecvOutSeqQueue.append(packet)
            qs = ''
            for p in self.mRecvOutSeqQueue:
                qs = qs + str(p.psn())+','
            skdebug('stash a out seq pkt, size:', len(self.mRecvOutSeqQueue), ' > ', qs)

    def StashSentPkt(self, packet: LinkPacket):
        # last_pkt:LinkPacket = self.mSendQueue[-1]
        # last_psn = last_pkt.mHeader.mPacketSeqNum
        # new_psn = packet.mHeader.mPacketSeqNum
        # if new_psn == last_psn+1:
        self.mSendQueue.append(packet)
        skdebug('StashSentPkt len:', len(self.mSendQueue))

    def GetRetransmitPkt(self, psn):
        for p in self.mSendQueue:
            if p.mHeader.mPacketSeqNum == psn:
                return p

    def StashRecvEAKPkt(self, packet):
        self.mRecvEAK = packet
        skdebug('stash recv eak')

    def GetRecvEAKPkt(self):
        return self.mRecvEAK
        skdebug('unstash recv eak')

    def StashSentEAKPkt(self, packet):
        self.mSentEAK = packet

    def GetSentEAKPkt(self):
        return self.mSentEAK

    def GetLastInSequencePSN(self):
        return self.mRecvQueue[-1].psn()

    def GetOutSequencePSN(self):
        res = []
        for p in self.mRecvOutSeqQueue:
            res.append(p.psn())
        return res

    def GetLastSentPkt(self):
        return self.mSendQueue[-1]

    def GetFistSentPkt(self):
        return self.mSendQueue[0]

    def GetLastRecvPkt(self):
        skdebug('GetLastRecvPkt mRecvQueue:', self.mRecvQueue)
        return self.mRecvQueue[-1]
