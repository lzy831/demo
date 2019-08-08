*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_I004
    [Documentation]  测试SoC正常通信中，发送窗口被卡满时，收到空EAK包，不会影响到EAK的相关机制
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_EAK
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time