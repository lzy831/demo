*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc_SYN_ONCE_N0001
    [Documentation]  协商一次_全部数据包一次成功
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time