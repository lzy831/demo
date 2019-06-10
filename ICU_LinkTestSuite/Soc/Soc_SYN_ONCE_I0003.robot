*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc Can Complete Handshake By One Negotiation
    [Documentation]     Soc在握手过程中收到穿插NAK包
    Send RST To Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    Send NAK to Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    &{SYN ACK Param} =      Send SYN ACK to Soc                 &{SYN Param}
    Receive ACK In Time     &{SYN ACK Param}
    Receive Nothing In Time