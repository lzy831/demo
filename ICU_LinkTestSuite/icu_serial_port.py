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

    def open(self):
        if self.mSerialPortObj == None and self.mSendThread == None and self.mRecvThread == None:
            skdebug('serial port was not open')
            try:
                skdebug('create serial object and open serial', self.mPortNum, self.mBaudrate)
                mSerialPortObj = serial.Serial(self.mPortNum, self.mBaudrate, timeout=0.1, write_timeout=0.1)
            except serial.SerialException:
                raise serial.SerialException
            else:
                skdebug('serial port open succeed')
            self.mSendThreadStopFlag = False
            self.mSendQueue = queue.Queue(SerialPort.cSendQueueMaxSize)
            self.mSendThread = threading.Thread(target=self.send_func)
            self.mSendThread.start()
            self.mRecvThreadStopFlag = False
            self.mRecvQueue = queue.Queue(SerialPort.cRecvQueueMaxSize)
            self.mRecvThread = threading.Thread(target=self.recv_func)
            self.mRecvThread.start()
            skdebug('serial task and queue create succeed')
        else:
            skdebug('serial port was already open')

    def close(self):
        pass

    def send_func(self):
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
                    self.flush_recv_queue()

            except serial.SerialException:
                # skdebug('send_func serial close')
                return
            time.sleep(0.1)
        # SendQueue.task_done()
        skdebug('send_func exit')

    def recv_func(self):
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
                skdebug(LinkSpec.cLinkPacketSYNLength)

                sync_bytes = self.mSerialPortObj.read(LinkSpec.cLinkPacketSYNLength)
                if len(sync_bytes) != 2:
                    continue
                if not (sync_bytes[0] == 0xAA and sync_bytes[1] == 0x55):
                    # skdebug('not sync bytes')
                    continue
                skdebug('found sync bytes')

                header_body = self.mSerialPortObj.read(LinkSpec.cLinkPacketHeaderLength-LinkSpec.cLinkPacketSYNLength)
                assert len(header_body) == LinkSpec.cLinkPacketHeaderLength - LinkSpec.cLinkPacketSYNLength
                header_data = sync_bytes+header_body

                if not is_valid_packet_header(header_data):
                    skdebug('invalid header')
                    continue

                skdebug('!!!!!!!!!!!!!!!!!!!!!! recv a pkt:')
                debug_header(header_data)

                payload_data = bytes()
                payload_len = get_payload_len_from_header(header_data)
                if payload_len > 0:
                    payload_data = self.mSerialPortObj.read(payload_len)
                    assert len(payload_data) == payload_len
                    debug_syn_payload(payload_data)

                if not self.mRecvQueue.full():
                    self.mRecvQueue.put(header_data+payload_data)
                else:
                    skdebug('queue is full')
            except serial.SerialException:
                # skdebug('recv_func serial close')
                return

            # skdebug('sleep 10ms')
            # time.sleep(0.01)

        # RecvQueue.task_done()
        skdebug('recv_func exit')

    def flush_recv_queue(self):
        if self.mRecvQueue != None:
            while not self.mRecvQueue.empty():
                self.mRecvQueue.get()

    def send_packet(self, packet: bytes):
        if self.mSerialPort != None:
            skdebug('Send to Remote:', packet.hex())
            self.mSendQueue.put(packet, timeout=1)
            while not self.mSendQueue.empty():
                time.sleep(0.01)
        else:
            skdebug('serial not open')

    def recv_packet(self):
        if self.mSerialPort != None and self.mRecvQueue != None:
            try:
                packet = self.mRecvQueue.get(True, 0.1)
                # skdebug('type(packet):', type(packet))
                # skdebug('get a packet from queue:', packet.hex())
                return packet
            except queue.Empty as e:
                # skdebug('queue empty:', e)
                pass
        return None


if __name__ == "__main__":
    pass
