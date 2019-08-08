*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_I005
    [Documentation]  测试SoC正常通信中，发送窗口被卡满时，收到空RST包，不会重新开启同步
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time