*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_I002
    [Documentation]  测试SoC正常通信中，发送窗口被卡满时，收到序列内的SYN+ACK包不会影响到EAK的相关机制
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_SYN_ACK
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time