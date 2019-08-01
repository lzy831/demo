*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc_SYN_ONCE_FC003
    [Documentation]  握手过程中穿插>Maximum Received Packet Length的包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_OverLength_PKT
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Send_OverLength_PKT
    Received_ACK_In_Time
    Received_Nothing_In_Time