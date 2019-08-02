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
        Library_Received_Test_NoNAK_ACK()
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
        Library_Send_BAD_PKT_INVALID_SOP()
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
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_INVALID_SOP()
        Library_Received_Test_NoNAK_ACK()
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
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_CB_PKT()
        Library_Received_Nothing_In_Time()
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


def SoC_APP_ACK_IE004():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE004 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_CB_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE004 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE007():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE007 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PL_PKT()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE007 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE008():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE008 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PL_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE008 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE009():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE009 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PL_2_PKT()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE009 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE010():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE010 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PL_2_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE010 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE011():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE011 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE011 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE012():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE012 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE012 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_IE013():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE013 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_WITH_NONEED_PAN()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE013 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE014():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE014 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_INVALID_ACK()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE014 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE015():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE015 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_INVALID_SESSION_ID()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE015 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE016():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE016 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_INVALID_SESSION_ID()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE016 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE017():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE017 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_INCORRECT_HC()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE017 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE018():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE018 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_INCORRECT_HC()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE018 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE021():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE021 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_INCORRECT_PC()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE021 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE022():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE022 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_BAD_PKT_INCORRECT_PC()
        Library_Received_Test_NoNAK_ACK()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE022 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_IE023():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_IE023 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_SYN_INVALID_DATA()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_IE023 succeed')
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
def SoC_APP_ACK_FC001():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_FC001 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Send_BAD_PKT_OVER_MAX_RECV_LEN_TEST_NONAK()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_FC001 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_FC002():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_FC002 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Retransmit_Previous_NoNAK()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_FC002 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()

def SoC_APP_ACK_FC003():
    skdebug('~~~~~~~~~~ SoC_APP_ACK_FC003 begin')
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_MNOOSP_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Retransmit_First_NoNAK_In_SentQ()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
        Library_Close_Transport()
        skdebug('~~~~~~~~~~ SoC_APP_ACK_FC003 succeed')
    except BaseException as e:
        skdebug('catched a except, quit')
        logging.exception(e)
        Library_Close_Transport()
        quit()
    else:
        pass
    time.sleep(1)
    Library_Close_Transport()


def SoC_APP_ACK_FC004():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Request_NoNAK_PKT()
        Library_Received_Twice_Test_NoNAK_ACK_In_LimitTime()
        Library_Send_ACK()
        Library_Received_Nothing_In_Time()
        ###############################
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
    sk_api_end()


def SoC_APP_ACK_FC005():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT_And_Received_ACK_In_LimitTime()
        Library_Received_Nothing_In_Time()
        ###############################
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
    sk_api_end()

def SoC_APP_ACK_FC006():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_MCA_NoNAK_PKT()
        Library_Received_ACK_In_Time()
        Library_Received_Nothing_In_Time()
        ###############################
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
    sk_api_end()

##############################################################################################################
if __name__ == "__main__":
    # SoC_APP_ACK_N001()
    # SoC_APP_ACK_N002()
    # SoC_APP_ACK_N003()
    SoC_APP_ACK_N004()

    # SoC_APP_ACK_I0001() #ok
    # SoC_APP_ACK_I0002()

    # SoC_APP_ACK_IE001()
    # SoC_APP_ACK_IE002() #ok
    # SoC_APP_ACK_IE003()
    # SoC_APP_ACK_IE004()
    # SoC_APP_ACK_IE007()
    # SoC_APP_ACK_IE008()
    # SoC_APP_ACK_IE009()
    # SoC_APP_ACK_IE010()
    # SoC_APP_ACK_IE011()
    # SoC_APP_ACK_IE012()
    # SoC_APP_ACK_IE013()
    # SoC_APP_ACK_IE014()
    # SoC_APP_ACK_IE015()
    # SoC_APP_ACK_IE016()
    # SoC_APP_ACK_IE017()
    # SoC_APP_ACK_IE018()
    # SoC_APP_ACK_IE021()
    # SoC_APP_ACK_IE022()
    # SoC_APP_ACK_IE023()

    # SoC_APP_ACK_FC001()
    # SoC_APP_ACK_FC002()
    # SoC_APP_ACK_FC003()
    # SoC_APP_ACK_FC004()
    # SoC_APP_ACK_FC005()
    # SoC_APP_ACK_FC006()
    pass
