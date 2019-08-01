*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_FC002
    [Documentation]  SoC在正常通信中,收到PSN位于RecvAckedWin内的数据包时，是否可以再次发送ACK
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Retransmit_Previous_NoNAK
    Received_ACK_In_Time
    Received_Nothing_In_Time