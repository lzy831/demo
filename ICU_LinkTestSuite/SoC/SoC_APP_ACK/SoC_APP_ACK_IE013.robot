*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE013
    [Documentation]  测试SoC在正常通信中，收到携带非必须PAN值的数据包，是否可以正常进行ACK
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_PKT_WITH_NONEED_PAN
    Received_ACK_In_Time
    Received_Nothing_In_Time