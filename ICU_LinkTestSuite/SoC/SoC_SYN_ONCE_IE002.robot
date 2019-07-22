*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SYN_ONCE_IE002
    [Documentation]  穿插包长错误的包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_BAD_PL_PKT
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time