*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SYN_ONCE_I0005
    [Documentation]  握手过程中穿插EAK包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_EAK
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time