*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_N002
    [Documentation]  测试是否是累积回复ACK
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Received_Nothing_In_Time