*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE017
    [Documentation]  测试SoC在正常通信中，收到HeaderChecksum错误的包，是否可以直接丢弃。
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_PKT_INCORRECT_HC
    Received_Nothing_In_Time