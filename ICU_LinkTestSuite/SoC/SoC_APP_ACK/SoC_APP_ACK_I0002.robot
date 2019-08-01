*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_I0002
    [Documentation]  测试SoC在正常通信中，收到SYN+ACK包，是否可以正确返回ACK

    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_SYN_ACK
    Received_ACK_In_Time
    Received_Nothing_In_Time