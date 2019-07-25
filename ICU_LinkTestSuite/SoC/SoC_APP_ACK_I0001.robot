*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_I0001
    [Documentation]  正常NoNAK包的通信中，插入纯SYN包，测试ACK状态是否正确
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time