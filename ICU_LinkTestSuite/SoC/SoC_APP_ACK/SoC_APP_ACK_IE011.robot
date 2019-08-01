*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE011
    [Documentation]  测试SoC在正常通信中，收到PSN在OutOfRecvWin范围内的包时，是否可以直接丢弃。
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_PSN_PKT
    Received_Nothing_In_Time