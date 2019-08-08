*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE004
    [Documentation]  测试SoC在正常通信中，接收到ControlBytes错误的包，是否影响对正常EAK包的响应及处理
    MCU_SYN
    Test_Start
    Test_Request_TWO_NoNAK_PKT
    Received_Test_NoNAK_ACK_And_Drop
    Received_Test_NoNAK_ACK
    Send_BAD_PKT_INVALID_CB
    Send_EAK
    Test_Received_Missing_NoNAK
    Send_ACK
    Received_Nothing_In_Time