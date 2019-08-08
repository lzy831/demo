*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_FC005
    [Documentation]  测试Soc的CumAckTimeout时间是否准确
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT_And_Received_ACK_In_LimitTime
    Received_Nothing_In_Time