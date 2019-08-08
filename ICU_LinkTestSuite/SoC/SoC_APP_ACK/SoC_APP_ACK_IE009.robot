*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE009
    [Documentation]  测试SoC在正常通信中，收到包长错误的包时（包长字段小于实际包长），是否可以直接丢弃。
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_PL_2_PKT
    Received_Nothing_In_Time