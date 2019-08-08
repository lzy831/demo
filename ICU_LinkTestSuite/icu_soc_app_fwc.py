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


def SoC_APP_FWC_N001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

def SoC_APP_FWC_N002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_NoNAK_SendQ_First_PSN_Munis_One()
    Library_Received_ACK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_FWC_N003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_NoNAK_Pkt_Out_Of_Recv_Win()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

def SoC_APP_FWC_N004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Wait()
    Library_Retransmit_Third_NoNAK_In_SentQ()
    Library_Received_EAK_In_Time()


def SoC_APP_FWC_N005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_MaxOutOfStdPkt_Add_Two_Test_NoNAK_Pkt()
    Library_Received_MaxOutOfStdPkt_Test_NoNAK_And_Drop_First()
    Library_Send_EAK()
    Library_Received_Test_NoNAK()
    Library_Send_ACK()
    Library_Received_Test_NoNAK()
    Library_Received_Test_NoNAK()
    Library_Send_ACK()

##############################################################################################################
def SoC_APP_FWC_I001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_SYN()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()

def SoC_APP_FWC_I002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_SYN_ACK()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()

def SoC_APP_FWC_I003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_ACK()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()

def SoC_APP_FWC_I004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_EAK()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()


def SoC_APP_FWC_I005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_RST()
    Library_Received_Acceptable_SYN_In_Time()
    Library_Reply_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

##############################################################################################################
def SoC_APP_FWC_IE001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()

def SoC_APP_FWC_IE002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_BAD_PKT_INVALID_CB()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()


def SoC_APP_FWC_IE003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_BAD_PKT_RST_With_INCORRECT_PL()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()


def SoC_APP_FWC_IE004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_BAD_PKT_INVALID_PL_MTA()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()

def SoC_APP_FWC_IE005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_BAD_PKT_PSN_OUT_OF_RECV_WIN()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
##############################################################################################################
def SoC_APP_FWC_TEST():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        # SoC_APP_FWC_N001()
        # SoC_APP_FWC_N002()
        # SoC_APP_FWC_N003()
        # SoC_APP_FWC_N004()
        # SoC_APP_FWC_N005()
        ###############################
        # SoC_APP_FWC_I001()
        # SoC_APP_FWC_I002()
        # SoC_APP_FWC_I003()
        # SoC_APP_FWC_I004()
        # SoC_APP_FWC_I005()
        ###############################
        # SoC_APP_FWC_IE001()
        # SoC_APP_FWC_IE002()
        # SoC_APP_FWC_IE003()
        # SoC_APP_FWC_IE004()
        SoC_APP_FWC_IE005()
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
    SoC_APP_FWC_TEST()
    pass