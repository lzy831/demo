*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc_SYN_ONCE_FC002
    [Documentation]  测试Retransmission Timeout(每次测试次数在2~Maximum Number of Retransmissions之间随机)
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Retransmit_SYN_ACK
    Received_ACK_In_Time
    Received_Nothing_In_Time