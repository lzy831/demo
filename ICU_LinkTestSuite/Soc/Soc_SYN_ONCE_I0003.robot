*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_穿插各种类型包_协商一次_握手过程中穿插NAK包
    [Documentation]     Soc在握手过程中收到穿插NAK包
    Send RST To Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    Send NAK to Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    &{SYN ACK Param} =      Reply SYN ACK To Remote                 &{SYN Param}
    Receive ACK In Time     &{SYN ACK Param}
    Receive Nothing In Time