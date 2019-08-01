*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_RESET_N001
    [Documentation]  触发Reset
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time