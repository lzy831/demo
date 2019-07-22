*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc_SYN_ONCE_FC001
    [Documentation]  测试SYN包一直发送的情况
    Send_RST
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time