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


def SoC_SYN_ONCE_N0001():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_N0001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_N0001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0001():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_SYN()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0003():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_NAK()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0003 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0004():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0004 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_ACK()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0004 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0005():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0005 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_Random_EAK()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0005 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0006():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0006 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0006 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_I0007():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0007 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_APP()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_I0007 succeed')
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


def SoC_SYN_TWICE_N0001():
    skdebug('~~~~~~~~~~ SoC_SYN_TWICE_N0001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Update_SYN_Negotiable_Param()
        Library_Send_RST()
        Library_Received_Negotiable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_Acceptable_SYN_ACK_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        skdebug('~~~~~~~~~~ SoC_SYN_TWICE_N0001 succeed')
        Library_Close_Transport()
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_TWICE_N0002():
    skdebug('~~~~~~~~~~ SoC_SYN_TWICE_N0002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Update_Invalid_SYN_Negotiable_Param()

        Library_Send_RST()
        Library_Received_Negotiable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_Repeat_SYN_In_Time()
        # 下面为正常2次握手流程
        Library_Update_SYN_Negotiable_Param()
        Library_Send_RST()
        Library_Received_Negotiable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_Acceptable_SYN_ACK_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()

        skdebug('~~~~~~~~~~ SoC_SYN_TWICE_N0002 succeed')
        Library_Close_Transport()
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


def SoC_SYN_ONCE_IE001():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_IE001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_BAD_PKT_INVALID_SOP()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_IE001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_IE002():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_IE002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_BAD_PL_PKT()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_IE002 succeed')
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


def SoC_SYN_ONCE_FC002():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_FC002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Retransmit_SYN_ACK()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_FC002 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_SYN_ONCE_FC003():
    skdebug('~~~~~~~~~~ SoC_SYN_ONCE_FC003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_OverLength_PKT()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Send_OverLength_PKT()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_SYN_ONCE_FC003 succeed')
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
def SoC_APP_RESET_N001():
    skdebug('~~~~~~~~~~ SoC_APP_RESET_N001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Send_RST()
        Library_Received_Acceptable_SYN_In_Time()
        Library_Reply_SYN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_RESET_N001 succeed')
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



if __name__ == "__main__":
    # SoC_SYN_ONCE_N0001()

    # SoC_SYN_ONCE_I0001()
    # SoC_SYN_ONCE_I0003()
    # SoC_SYN_ONCE_I0004()
    # SoC_SYN_ONCE_I0005()
    # SoC_SYN_ONCE_I0006()
    # SoC_SYN_ONCE_I0007()

    # SoC_SYN_TWICE_N0001()
    # SoC_SYN_TWICE_N0002()

    # SoC_SYN_ONCE_IE001()
    # SoC_SYN_ONCE_IE002()

    # SoC_SYN_ONCE_FC002() # fail
    # SoC_SYN_ONCE_FC003() # fail

    # SoC_APP_ACK_N001()
    # SoC_APP_ACK_N002()

    # SoC_APP_ACK_I0001() # fail
    # SoC_APP_ACK_I0002() # fail
    # SoC_APP_ACK_I0003() # fail
    # SoC_APP_ACK_I0004() # fail
    # SoC_APP_ACK_I0005()

    # SoC_APP_ACK_IE001() # fail
    # SoC_APP_ACK_IE002() # fail


    # SoC_APP_RESET_N001()

    pass
