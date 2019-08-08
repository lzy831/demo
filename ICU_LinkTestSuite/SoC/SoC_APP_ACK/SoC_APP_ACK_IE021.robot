*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE021
    [Documentation]  测试SoC在正常通信中，收到PayloadData Checksum错误的包时，是否可以直接丢弃。
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_PKT_INCORRECT_PC
    Received_Nothing_In_Time