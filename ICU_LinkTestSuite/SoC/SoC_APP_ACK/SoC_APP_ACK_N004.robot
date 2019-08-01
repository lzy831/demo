*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_N004
    [Documentation]  测试SoC在未收到ACK之前，是否会把需要发送的NoNAK包都发送出来
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Request_MaxCumAckCount_NoNAK_PKT
    Received_MaxCumAckCount_Test_NoNAK
    Send_ACK
    Received_Nothing_In_Time