*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE010
    [Documentation]  测试SoC在正常通信中，收到包长错误的包时（包长字段小于实际包长），是否可以直接丢弃。同时也测试了SoC的超时重发机制。
    MCU_SYN
    Test_Start
    Test_Request_NoNAK_PKT
    Received_Test_NoNAK_With_ACK
    Send_BAD_PL_2_PKT
    Received_Test_NoNAK_With_ACK
    Send_ACK
    Received_Nothing_In_Time