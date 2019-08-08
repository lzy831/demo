*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_FC004
    [Documentation]  测试SoC的超时重传时间是否准确
    MCU_SYN
    Test_Start
    Test_Request_NoNAK_PKT
    Received_Twice_Test_NoNAK_With_ACK_In_Time
    Send_ACK
    Received_Nothing_In_Time