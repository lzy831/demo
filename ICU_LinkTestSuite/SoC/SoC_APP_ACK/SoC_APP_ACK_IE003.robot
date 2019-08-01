*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE003
    [Documentation]  测试SoC在正常通信中，收到ControlByte错误的包，是否可以直接丢弃。
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_CB_PKT
    Received_Nothing_In_Time