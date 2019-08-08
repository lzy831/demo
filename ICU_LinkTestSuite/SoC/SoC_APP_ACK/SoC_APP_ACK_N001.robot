*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_N001
    [Documentation]  测试SoC是否可以正确回复ACK
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Received_Nothing_In_Time