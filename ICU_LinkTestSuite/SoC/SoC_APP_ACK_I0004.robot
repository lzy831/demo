*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_I0004
    [Documentation]  正常NoNAK包的通信中，插入EAK包，ACK状态是否正确
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_Random_EAK
    Received_Nothing_In_Time