*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_IE001
    [Documentation]  正常的通信中，插入包起始位错误的包，ACK状态是否正确
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Received_ACK_In_Time
    Send_BAD_SOP_PKT
    Received_Nothing_In_Time