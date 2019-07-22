#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import queue
import threading
import time
from icu_debug import *
from icu_link_packet import *


class SerialPort(object):
    cSendQueueMaxSize = 100
    cRecvQueueMaxSize = 1000

    def __init__(self, port, baudrate):
        self.mPortNum = port
        self.mBaudrate = baudrate
        self.mSerialPortObj = None

        self.mSendThread = None
        self.mSendThreadStopFlag = None
        self.mSendQueue = None

        self.mRecvThread = None
        self.mRecvThreadStopFlag = None
        self.mRecvQueue = None

    def Open(self):
        if self.mSerialPortObj == None and self.mSendThread == None and self.mRecvThread == None:
            skdebug('serial port was not open')
            try:
                skdebug('create serial object and open serial', self.mPortNum, self.mBaudrate)
                self.mSerialPortObj = serial.Serial(self.mPortNum, self.mBaudrate, timeout=0.1, write_timeout=0.1)
                skdebug('mSerialPortObj:', self.mSerialPortObj)
            except serial.SerialException:
                raise serial.SerialException
            else:
                skdebug('serial port open succeed')
            self.mSendThreadStopFlag = False
            self.mSendQueue = queue.Queue(SerialPort.cSendQueueMaxSize)
            self.mSendThread = threading.Thread(target=self.SendFunc)
            self.mSendThread.start()
            self.mRecvThreadStopFlag = False
            self.mRecvQueue = queue.Queue(SerialPort.cRecvQueueMaxSize)
            self.mRecvThread = threading.Thread(target=self.RecvFunc)
            self.mRecvThread.start()
            skdebug('serial task and queue create succeed')
        else:
            skdebug('serial port was already opened')

    def Close(self):
        if self.mSerialPortObj != None:
            # skdebug('SendThread alive', SendThread.is_alive())
            # skdebug('RecvThread alive', RecvThread.is_alive())
            # time.sleep(2)
            skdebug('ready to close thread')
            skdebug('SendThread alive', self.mSendThread.is_alive())
            skdebug('RecvThread alive', self.mRecvThread.is_alive())
            if self.mRecvThread != None and self.mRecvThread.is_alive():
                self.mRecvThreadStopFlag = True
                self.mRecvThread.join()
                skdebug('mRecvThread join ok')
                skdebug('mRecvThread alive', self.mRecvThread.is_alive())
                self.mRecvThread = None
            if self.mSendThread != None and self.mSendThread.is_alive():
                self.mSendThreadStopFlag = True
                self.mSendThread.join()
                skdebug('SendThread join ok')
                skdebug('SendThread alive', self.mSendThread.is_alive())
                self.mSendThread = None
            skdebug('will close serial')
            self.mSerialPortObj.close()
            self.mSerialPortObj = None
            skdebug('close serial ok')
            skdebug('close serial transport ok')
        else:
            skdebug('serial port was already closed')

    def SendFunc(self):
        # global LINK_PKT_MAX_PSN

        skdebug('send_func begin')
        while True:
            if self.mSendThreadStopFlag:
                skdebug('SendThreadStopFlag set')
                break
            if not self.mSerialPortObj.writable():
                skdebug('SerialPort is not writable')
                break
            try:
                while not self.mSendQueue.empty():
                    packet = self.mSendQueue.get()

                    skdebug('send a packet')
                    self.mSerialPortObj.write(packet)

                    # SendPSN = SendPSN+1 % LINK_PKT_MAX_PSN

                    # if is_reset_packet(packet):
                    #     skdebug('send a reset packet, RecvQueue count:',
                    #             RecvQueue.qsize())
                    #     flush_recv_queue()

                    # 试着每法送一个包就清空当前的接收队列
                    self.FlushRecvQueue()

            except serial.SerialException:
                # skdebug('send_func serial close')
                return
            time.sleep(0.01)
        # SendQueue.task_done()
        skdebug('send_func exit')

    def RecvFunc(self):
        # global LinkPacketSYNLength

        skdebug('recv_func begin')
        while True:
            skdebug('recv_func loop')
            if self.mRecvThreadStopFlag:
                skdebug('RecvThreadStopFlag set')
                break

            if not self.mSerialPortObj.readable():
                skdebug('SerialPort is not readable')
                break

            try:
                skdebug('recv_func try to read')
                # skdebug(LinkSpec.cLinkPacketSYNLength)

                sync_bytes = self.mSerialPortObj.read(LinkSpec.cLinkPacketSYNLength)
                if len(sync_bytes) != 2:
                    continue
                if not (sync_bytes[0] == 0xAA and sync_bytes[1] == 0x55):
                    # skdebug('not sync bytes')
                    continue
                skdebug('found sync bytes')

                header_body = self.mSerialPortObj.read(LinkSpec.cLinkPacketHeaderLength-LinkSpec.cLinkPacketSYNLength)
                assert len(header_body) == LinkSpec.cLinkPacketHeaderLength - LinkSpec.cLinkPacketSYNLength
                header_bytes = sync_bytes+header_body

                header_obj = LinkPacketHeader(header_bytes=header_bytes)
                if not header_obj.is_valid():
                    skdebug('invalid header')
                    continue

                skdebug('!!!!!!!!!!!!!!!!!!!!!! recv a pkt:')
                # skdebug('header info:', header_obj.info_string())

                payload_data = bytes()
                payload_len = header_obj.mPacketLength - LinkSpec.cLinkPacketHeaderLength
                if payload_len > 0:
                    payload_data = self.mSerialPortObj.read(payload_len)
                    assert len(payload_data) == payload_len
                    # debug_syn_payload(payload_data)

                if not self.mRecvQueue.full():
                    self.mRecvQueue.put(header_bytes+payload_data)
                else:
                    skdebug('queue is full')
            except serial.SerialException:
                skdebug('recv_func catch SerialException')
                return

            # skdebug('sleep 10ms')
            # time.sleep(0.01)

        # RecvQueue.task_done()
        skdebug('recv_func exit')

    def FlushRecvQueue(self):
        if self.mRecvQueue != None:
            while not self.mRecvQueue.empty():
                self.mRecvQueue.get()

    def SendPacket(self, packet: bytes):
        if self.mSerialPortObj != None:
            skdebug('Send to Remote:', packet.hex())
            self.mSendQueue.put(packet, timeout=1)
            while not self.mSendQueue.empty():
                time.sleep(0.01)
            skdebug('Send to Remote Done')
        else:
            skdebug('serial not open')

    def RecvPacket(self, timeout=0.1):
        skdebug('RecvPacket')
        if self.mSerialPortObj != None and self.mRecvQueue != None:
            try:
                packet = self.mRecvQueue.get(True, timeout)
                # skdebug('type(packet):', type(packet))
                skdebug('get a packet from queue:', packet.hex())
                return packet
            except queue.Empty as e:
                # skdebug('queue empty:', e)
                pass
        return None


if __name__ == "__main__":
    pass
