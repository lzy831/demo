*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_N002
    [Documentation]  测试SoC接收到RWL-1位置(RecvWin最左边的PSN的前一个PSN)的NoNAK包时是否会立即发送ACK
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_Test_NoNAK_SendQ_First_PSN_Munis_One
    Received_ACK_In_Time
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time