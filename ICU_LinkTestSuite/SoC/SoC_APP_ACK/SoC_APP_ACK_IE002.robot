*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE002
    [Documentation]  测试SoC在正常通信中，收到起始位错误的包是，是否可以直接丢弃。同时也测试了SoC的超时重发机制。
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Request_NoNAK_PKT
    Received_Test_NoNAK_With_ACK
    Send_BAD_SOP_PKT
    Received_Test_NoNAK_With_ACK
    Send_ACK
    Received_Nothing_In_Time