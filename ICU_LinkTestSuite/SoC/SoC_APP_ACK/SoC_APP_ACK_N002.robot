*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_N002
    [Documentation]  测试SoC是否会对连续的NoNAK数据包进行累计确认
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Received_Nothing_In_Time