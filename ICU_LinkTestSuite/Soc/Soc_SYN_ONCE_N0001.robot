*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc Can Complete Handshake By One Negotiation
    [Documentation]     Soc端可以通过一次SYN协商握手成功
    Send RST To Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    &{SYN ACK Param} =      Send SYN ACK to Soc                 &{SYN Param}
    Receive ACK In Time     &{SYN ACK Param}