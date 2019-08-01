*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SYN_ONCE_I0007
    [Documentation]  握手过程中穿插应用包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_APP
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time