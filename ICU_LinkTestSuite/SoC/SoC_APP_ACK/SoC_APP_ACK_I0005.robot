*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_I0005
    [Documentation]  测试SoC在正常通信中，收到RESET包，SoC状态是否会重新启动SYN
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time