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


def SoC_APP_EAK_N001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_N002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Three_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_N003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()

##############################################################################################################


def SoC_APP_EAK_I001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_SYN_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_I002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_SYN_ACK_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_I003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_ACK()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_I005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_RST()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_Acceptable_SYN_In_Time()
    Library_Reply_SYN()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


##############################################################################################################
def SoC_APP_EAK_IE001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_INVALID_CB()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_INVALID_CB()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE005():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_RST_With_INCORRECT_PL()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


# def SoC_APP_EAK_IE006():
#     Library_MCU_SYN()
#     Library_Test_Start()
#     Library_Request_Two_Test_NoNAK_Pkt()
#     Library_Received_Test_NoNAK_ACK_And_Drop()
#     Library_Received_Test_NoNAK_ACK()
#     Library_Send_BAD_PKT_INVALID_PL_MTA()
#     Library_Send_EAK()
#     Library_Test_Received_Missing_NoNAK()
#     Library_Send_ACK()
#     Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE007():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_INVALID_PL_MTA()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE008():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_EAK_INVALID_PL_MTA()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE009():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_INVALID_PL_LTA()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE010():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_EAK_INVALID_PL_LTA()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE011():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_RST_With_PSN()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE012():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_RST_With_PSN()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE013():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_RST_With_PAN()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE014():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_RST_With_PAN()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE015():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_INVALID_SESSION_ID()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE017():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_Incorrect_HC()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE018():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_Incorrect_HC()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE019():
    pass


def SoC_APP_EAK_IE020():
    pass


def SoC_APP_EAK_IE021():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_BAD_PKT_Incorrect_PC()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_IE022():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Request_Two_Test_NoNAK_Pkt()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_BAD_PKT_Incorrect_PC()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()
    Library_Send_ACK()
    Library_Received_Nothing_In_Time()

def SoC_APP_EAK_IE023():
    # Library_MCU_SYN()
    # Library_Test_Start()
    # Library_Send_Test_NoNAK_Pkt()
    # Library_Send_BAD_PKT_SYN_Invalid_Data_Skip_One_PSN()
    # Library_Received_EAK_In_Time()
    # 有问题
    # Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    # Library_Received_ACK_In_Time()
    # Library_Received_Nothing_In_Time()
    pass

def SoC_APP_EAK_IE024():
    # Library_MCU_SYN()
    # Library_Test_Start()
    # Library_Request_Two_Test_NoNAK_Pkt()
    # Library_Received_Test_NoNAK_ACK_And_Drop()
    # Library_Received_Test_NoNAK_ACK()
    # Library_Send_BAD_PKT_SYN_Invalid_Data()
    # Library_Send_EAK()
    # Library_Test_Received_Missing_NoNAK_With_ACK()
    # Library_Send_ACK()
    # Library_Received_Nothing_In_Time()
    pass

def SoC_APP_EAK_IE025():
    # Library_MCU_SYN()
    # Library_Test_Start()
    # Library_Request_Two_Test_NoNAK_Pkt()
    # Library_Received_Test_NoNAK_ACK()
    # Library_Received_Test_NoNAK_ACK()
    # Library_Send_BAD_PKT_SYN_ACK_Invalid_Data()
    # Library_Received_Test_NoNAK_ACK()
    # Library_Received_Nothing_In_Time()
    pass

def SoC_APP_EAK_IE026():
    pass
##############################################################################################################


def SoC_APP_EAK_FC001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Bad_Pkt_OverLength()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

def SoC_APP_EAK_FC002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Retransmit_Previous_NoNAK_Pkt()
    Library_Received_EAK_In_Time()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()


def SoC_APP_EAK_FC003():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt()
    Library_Send_OutSeq_NoNAK_Pkt_And_Received_EAK_In_LimitTime()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

def SoC_APP_EAK_FC004():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Send_Test_NoNAK_Pkt_Skip_One_PSN()
    Library_Send_NoNAK_Pkt_And_Received_EAK_In_LimitTime()
    Library_Send_Test_Missing_NoNAK_Pkt_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

##############################################################################################################


def SoC_APP_EAK_TEST():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        SoC_APP_EAK_N001()
        # SoC_APP_EAK_N002()
        # SoC_APP_EAK_N003()
        ###############################
        # SoC_APP_EAK_I001()
        # SoC_APP_EAK_I002()
        # SoC_APP_EAK_I003()
        # SoC_APP_EAK_I005()
        ###############################
        # SoC_APP_EAK_IE001()
        # SoC_APP_EAK_IE002()
        # SoC_APP_EAK_IE003()
        # SoC_APP_EAK_IE004()
        # SoC_APP_EAK_IE005()
        # SoC_APP_EAK_IE006()
        # SoC_APP_EAK_IE007()
        # SoC_APP_EAK_IE008()
        # SoC_APP_EAK_IE009()
        # SoC_APP_EAK_IE010()
        # SoC_APP_EAK_IE011()
        # SoC_APP_EAK_IE012()
        # SoC_APP_EAK_IE013()
        # SoC_APP_EAK_IE014()
        # SoC_APP_EAK_IE015()
        # SoC_APP_EAK_IE017()
        # SoC_APP_EAK_IE018()
        # SoC_APP_EAK_IE021()
        # SoC_APP_EAK_IE022()
        # SoC_APP_EAK_IE023()
        # SoC_APP_EAK_IE024()
        # SoC_APP_EAK_IE025()
        ###############################
        # SoC_APP_EAK_FC001()
        # SoC_APP_EAK_FC002()
        # SoC_APP_EAK_FC003()
        # SoC_APP_EAK_FC004()
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
    SoC_APP_EAK_TEST()
    pass
