*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE014
    [Documentation]  测试SoC在正常通信中，收到不正确的ACK时，可以丢弃，并对未进行ACK的包进行重发
    MCU_SYN
    Test_Start
    Test_Request_NoNAK_PKT
    Received_Test_NoNAK_With_ACK
    Send_BAD_PKT_INVALID_ACK
    Received_Test_NoNAK_With_ACK
    Send_ACK
    Received_Nothing_In_Time