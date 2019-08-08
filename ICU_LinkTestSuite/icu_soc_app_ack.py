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
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_N002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_N003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_N004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_MaxCumAckCount_Test_NoNAK_Pkt()
    Library_Received_MaxCumAckCount_Test_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


##############################################################################################################


def SoC_APP_ACK_I0001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_I0002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_SYN_ACK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_I0003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()  # 这里会收到SoC的新的SYN包


def SoC_APP_ACK_I0004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_Random_EAK()
    Library_Received_Nothing_In_Time()  # 这里会收到SoC的新的SYN包


def SoC_APP_ACK_I0005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_RST()
    Library_Received_Acceptable_SYN_In_Time()
    Library_Reply_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

##############################################################################################################


def SoC_APP_ACK_IE001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_CB_PKT()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_CB_PKT()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE007():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_INVALID_PL_MTA()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE008():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_PL_MTA()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE009():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_INVALID_PL_LTA()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE010():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_PL_LTA()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE011():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE012():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE013():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_WITH_NONEED_PAN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE014():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_ACK()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE015():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_INVALID_SESSION_ID()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE016():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_SESSION_ID()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE017():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_Incorrect_HC()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE018():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_Incorrect_HC()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE021():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_Incorrect_PC()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE022():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_Incorrect_PC()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_IE023():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Send_BAD_PKT_SYN_Invalid_Data()
    Library_Received_Nothing_In_Time()


##############################################################################################################
def SoC_APP_ACK_FC001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_BAD_PKT_OVER_MAX_RECV_LEN_TEST_NONAK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_FC002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Retransmit_Previous_NoNAK_Pkt()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_FC003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_PKT()
    Library_Received_ACK_In_Time()
    Library_Retransmit_First_NoNAK_In_SentQ()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_FC004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt()
    Library_Received_Twice_Test_NoNAK_ACK_In_LimitTime()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_FC005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Test_Send_NoNAK_PKT_And_Received_ACK_In_LimitTime()
    Library_Received_Nothing_In_Time()


def SoC_APP_ACK_FC006():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Test_Send_MCA_NoNAK_PKT()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


##############################################################################################################
if __name__ == "__main__":
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        # SoC_APP_ACK_N001()
        # SoC_APP_ACK_N002()
        # SoC_APP_ACK_N003()
        # SoC_APP_ACK_N004()
        #########################
        # SoC_APP_ACK_I0001()
        # SoC_APP_ACK_I0002()
        #########################
        # SoC_APP_ACK_IE001()
        # SoC_APP_ACK_IE002()
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
        SoC_APP_ACK_IE023()
        #########################
        # SoC_APP_ACK_FC001()
        # SoC_APP_ACK_FC002()
        # SoC_APP_ACK_FC003()
        # SoC_APP_ACK_FC004()
        # SoC_APP_ACK_FC005()
        # SoC_APP_ACK_FC006()
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
