*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_N003
    [Documentation]  测试SoC是否会对ACK包进行回复
    MCU_SYN
    Test_Start
    Test_Request_NoNAK_PKT
    Received_Test_NoNAK_With_ACK
    Send_ACK
    Received_Nothing_In_Time