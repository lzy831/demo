*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_FC003
    [Documentation]  SoC在正常通信中,收到PSN位于RecvAckedWin最左边的数据包时，是否可以再次发送ACK
    MCU_SYN
    Test_Start
    Test_Send_MNOOSP_NoNAK_PKT
    Received_ACK_In_Time
    Retransmit_First_NoNAK_In_SentQ
    Received_ACK_In_Time
    Received_Nothing_In_Time