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
from icu_test_api import *
from icu_debug import *


##############################################################################################################
def SoC_APP_ACK_N001():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_N001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_N001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_N002():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_N002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Test_Send_NoNAK_PKT()
        Library_Test_Send_NoNAK_PKT()
        Library_Test_Send_NoNAK_PKT()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_N002 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_N003():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_N003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_With_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_N003 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_N004():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_N004 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_MaxCumAckCount_NoNAK_PKT()
        Library_Received_MaxCumAckCount_Test_NoNAK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_N004 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

##############################################################################################################


def SoC_APP_ACK_I0001():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_I0001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_I0001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_I0002():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_I0002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_SYN_ACK()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_I0002 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_I0003():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_I0003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()  # 这里会收到SoC的新的SYN包
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_I0003 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_I0004():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_I0004 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_Random_EAK()
        Library_Received_Nothing_In_Time()  # 这里会收到SoC的新的SYN包
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_I0004 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_I0005():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_I0005 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_I0005 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

##############################################################################################################


def SoC_APP_ACK_IE001():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_SOP_PKT()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE002():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_With_ACK()
        Library_Send_BAD_SOP_PKT()
        Library_Received_Test_NoNAK_With_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE002 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE003():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()

        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE003 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


if __name__ == "__main__":
    # SoC_APP_ACK_N001()
    # SoC_APP_ACK_N002()
    # SoC_APP_ACK_N003()
    # SoC_APP_ACK_N004()

    # SoC_APP_ACK_I0001() #ok
    SoC_APP_ACK_I0002()


    # SoC_APP_ACK_IE001()
    # SoC_APP_ACK_IE002() #ok
    # SoC_APP_ACK_IE003()
    pass
