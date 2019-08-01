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
def SoC_APP_EAK_IE001():
    sk_api_begin()
    try:
        Library_Reset_For_MCU()
        Library_Open_Transport()
        ###############################
        Library_MCU_SYN()
        Library_Test_Start()
        Library_Received_ACK_In_Time()
        Library_Test_Send_NoNAK_PKT()
        Library_Send_BAD_PKT_INVALID_SOP()
        Library_Test_Send_NoNAK_PKT()
        Library_Received_EAK_In_Time()
        # Library_Test_Send_One_Missing_NoNAK_PKT()
        # Library_Received_ACK_In_Time()
        # Library_Received_Nothing_In_Time()
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
    SoC_APP_EAK_IE001()
    pass