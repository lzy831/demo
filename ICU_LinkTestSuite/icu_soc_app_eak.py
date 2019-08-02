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

def SoC_APP_EAK_IE001():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Received_ACK_In_Time()
    Library_Test_Send_NoNAK_PKT()
    Library_Send_BAD_PKT_INVALID_SOP()
    Library_Test_Send_NoNAK_PKT_Skip_One_PSN()
    Library_Received_EAK_In_Time()
    Library_Test_Send_Missing_NoNAK_PKT_According_EAK()
    Library_Received_ACK_In_Time()
    Library_Received_Nothing_In_Time()

def SoC_APP_EAK_IE002():
    Library_MCU_SYN()
    Library_Test_Start()
    Library_Received_ACK_In_Time()
    Library_Test_Request_TWO_NoNAK_PKT()
    Library_Received_Test_NoNAK_ACK_And_Drop()
    Library_Received_Test_NoNAK_ACK()
    Library_Send_EAK()
    Library_Test_Received_Missing_NoNAK()

##############################################################################################################
def SoC_APP_EAK_TEST():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        # SoC_APP_EAK_IE001()
        SoC_APP_EAK_IE002()
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