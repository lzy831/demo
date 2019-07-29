*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_I0002
    [Documentation]  正常NoNAK包的通信中，插入SYN+ACK包，测试ACK状态是否正确
    MCU_SYN
    Test_Start
    Received_ACK_In_Time
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_SYN_ACK
    Received_ACK_In_Time
    Received_Nothing_In_Time