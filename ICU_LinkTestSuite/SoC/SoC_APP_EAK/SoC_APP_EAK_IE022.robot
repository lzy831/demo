*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE022
    [Documentation]  测试SoC在正常通信中，接收到PayloadChecksum错误的包，是否影响对正常EAK包的响应及处理
    MCU_SYN
    Test_Start
    Test_Request_Two_NoNAK_PKT
    Received_Test_NoNAK_ACK_And_Drop
    Received_Test_NoNAK_ACK
    Send_BAD_PKT_INCORRECT_PC
    Send_EAK
    Test_Received_Missing_NoNAK
    Send_ACK
    Received_Nothing_In_Time