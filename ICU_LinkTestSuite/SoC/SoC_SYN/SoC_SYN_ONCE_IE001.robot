*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SYN_ONCE_IE001
    [Documentation]  穿插包起始位错误的Session包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_BAD_SOP_PKT
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time