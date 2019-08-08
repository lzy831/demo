*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_I005
    [Documentation]  测试SoC在正常通信中，收到RST包，是否可以重新开启同步流程
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Send_RST
    Test_Send_NoNAK_PKT_Skip_One_PSN
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time