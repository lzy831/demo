*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SYN_ONCE_I0004
    [Documentation]  握手过程中穿插纯ACK包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_ACK
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time