*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_穿插各种类型包_协商一次_握手过程中穿插NAK包
    [Documentation]     Soc在握手过程中收到穿插NAK包
    Send RST To Soc
    &{SYN Param} =          Received_Acceptable_SYN_In_Time
    Send NAK to Soc
    &{SYN Param} =          Received_Acceptable_SYN_In_Time
    &{SYN ACK Param} =      Reply_SYN_ACK_To_Remote                 &{SYN Param}
    Received_ACK_In_Time     &{SYN ACK Param}
    Received_Nothing_In_Time