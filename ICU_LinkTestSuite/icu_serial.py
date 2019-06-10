#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import queue
import threading
import time
import random
from icu_link_packet import *
from icu_debug import *


SerialPort = None
SendQueueMaxSize = 100
RecvQueueMaxSize = 1000
SendThread = None
RecvThread = None
SendQueue = None
RecvQueue = None
SendThreadStopFlag = False
RecvThreadStopFlag = False
SendPSN = 0


def send_func():
    global SerialPort
    global SendPSN
    global SendQueue
    global RecvQueue
    skdebug('send_func begin')
    while True:
        if SendThreadStopFlag:
            skdebug('SendThreadStopFlag set')
            break
        if not SerialPort.writable():
            skdebug('SerialPort is not writable')
            break
        try:
            while not SendQueue.empty():
                packet = SendQueue.get()

                skdebug('send a packet')
                SerialPort.write(packet)
                SendPSN = SendPSN+1 % LINK_PKT_MAX_PSN

                
                # if is_reset_packet(packet):
                #     skdebug('send a reset packet, RecvQueue count:',
                #             RecvQueue.qsize())
                #     flush_recv_queue()

                # 试着每法送一个包就清空当前的接收队列
                flush_recv_queue()
                
        except serial.SerialException:
            # skdebug('send_func serial close')
            return
        time.sleep(0.1)
    # SendQueue.task_done()
    skdebug('send_func exit')


def recv_func():
    global SerialPort
    global RecvQueue
    skdebug('recv_func begin')
    while True:
        skdebug('recv_func loop')
        if RecvThreadStopFlag:
            skdebug('RecvThreadStopFlag set')
            break

        if not SerialPort.readable():
            skdebug('SerialPort is not readable')
            break

        try:
            skdebug('recv_func try to read')

            sync_bytes = SerialPort.read(LinkPacketSYNLength)
            if len(sync_bytes) != 2:
                continue
            if not (sync_bytes[0] == 0xAA and sync_bytes[1] == 0x55):
                # skdebug('not sync bytes')
                continue
            skdebug('found sync bytes')

            header_body = SerialPort.read(
                LinkPacketHeaderLength-LinkPacketSYNLength)
            assert len(header_body) == LinkPacketHeaderLength - \
                LinkPacketSYNLength
            header_data = sync_bytes+header_body

            if not is_valid_packet_header(header_data):
                skdebug('invalid header')
                continue

            skdebug('!!!!!!!!!!!!!!!!!!!!!! recv a pkt:')
            debug_header(header_data)

            payload_data = bytes()
            payload_len = get_payload_len_from_header(header_data)
            if payload_len > 0:
                payload_data = SerialPort.read(payload_len)
                assert len(payload_data) == payload_len
                debug_syn_payload(payload_data)

            if not RecvQueue.full():
                RecvQueue.put(header_data+payload_data)
            else:
                skdebug('queue is full')

        except serial.SerialException:
            # skdebug('recv_func serial close')
            return

        # skdebug('sleep 10ms')
        # time.sleep(0.01)

    # RecvQueue.task_done()
    skdebug('recv_func exit')


def open_serial_transport(port='COM1', baudrate=115200):
    global SerialPort
    global SendThread
    global RecvThread
    global SendQueue
    global RecvQueue
    global SendQueueMaxSize
    global RecvQueueMaxSize
    global SendThreadStopFlag
    global RecvThreadStopFlag
    global SendPSN

    if SerialPort == None and SendThread == None and RecvThread == None:

        skdebug('serial was not open')
        try:
            logger.info('create serial object and open serial', port, baudrate)
            SerialPort = serial.Serial(
                port, baudrate, timeout=0.1, write_timeout=0.1)
        except serial.SerialException:
            raise serial.SerialException
        else:
            skdebug('open serial ok')

        SendThreadStopFlag = False
        SendQueue = queue.Queue(SendQueueMaxSize)
        SendThread = threading.Thread(target=send_func)
        SendThread.start()

        RecvThreadStopFlag = False
        RecvQueue = queue.Queue(RecvQueueMaxSize)
        RecvThread = threading.Thread(target=recv_func)
        RecvThread.start()
    SendPSN = random.randint(0, 255)
    skdebug('serial task launch ok')


def close_serial_transport():
    global SerialPort
    global SendThread
    global RecvThread
    global SendQueue
    global RecvQueue
    global SendThreadStopFlag
    global RecvThreadStopFlag

    # skdebug('close serial transport begin, sleep 3s')
    # time.sleep(2)
    # skdebug('SendThread alive', SendThread.is_alive())
    # skdebug('RecvThread alive', RecvThread.is_alive())
    if SerialPort != None:

        # skdebug('SendThread alive', SendThread.is_alive())
        # skdebug('RecvThread alive', RecvThread.is_alive())
        # time.sleep(2)

        skdebug('ready to close thread')
        skdebug('SendThread alive', SendThread.is_alive())
        skdebug('RecvThread alive', RecvThread.is_alive())

        if RecvThread != None and RecvThread.is_alive():
            RecvThreadStopFlag = True
            RecvThread.join()
            skdebug('RecvThread join ok')
            skdebug('SendThread alive', SendThread.is_alive())
            skdebug('RecvThread alive', RecvThread.is_alive())

        if SendThread != None and SendThread.is_alive():
            SendThreadStopFlag = True
            SendThread.join()
            skdebug('SendThread join ok')
            skdebug('SendThread alive', SendThread.is_alive())
            skdebug('RecvThread alive', RecvThread.is_alive())

        skdebug('will close serial ok')
        SerialPort.close()
        skdebug('close serial ok')
        SendQueue = None
        RecvQueue = None
        SendThread = None
        RecvThread = None
        SerialPort = None
    skdebug('close serial transport ok')


def flush_serial_transport():
    global SendQueue
    global RecvQueue
    skdebug('transport flush begin')
    if SendQueue != None:
        while not SendQueue.empty():
            SendQueue.get()
    if RecvQueue != None:
        while not RecvQueue.empty():
            RecvQueue.get()
    skdebug('transport flush end')


def flush_recv_queue():
    global RecvQueue
    if RecvQueue != None:
        while not RecvQueue.empty():
            RecvQueue.get()


def reset_serial_transport():
    skdebug('transport reset begin')
    close_serial_transport()
    open_serial_transport()
    skdebug('transport reset end')


def get_next_transport_psn():
    return SendPSN


def send_packet_to_remote(packet: bytes):
    global SendQueue
    if SerialPort != None:
        skdebug('Send to Remote:', packet.hex())
        SendQueue.put(packet, timeout=1)
        while not SendQueue.empty():
            time.sleep(0.01)
    else:
        skdebug('serial not open')


def recv_packet_from_remote():
    global RecvQueue
    if SerialPort != None and RecvQueue != None:
        try:
            packet = RecvQueue.get(True, 0.1)
            # skdebug('type(packet):', type(packet))
            # skdebug('get a packet from queue:', packet.hex())
            return packet
        except queue.Empty as e:
            e
            # skdebug('queue empty:', e)
            pass
    return None


if __name__ == "__main__":
    open_serial_transport('COM1', 115200)
    time.sleep(5)
    close_serial_transport()
