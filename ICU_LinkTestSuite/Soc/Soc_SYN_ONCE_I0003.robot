*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_穿插各种类型包_协商一次_握手过程中穿插NAK包
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_NAK
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time