*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_正常流程_协商一次_全部数据包一次成功
    [Documentation]     Soc端可以通过一次SYN协商握手成功
    Send RST To Soc
    &{SYN Param} =          Receive Acceptable SYN In Time
    &{SYN ACK Param} =      Reply SYN ACK To Remote                 &{SYN Param}
    Receive ACK In Time     &{SYN ACK Param}
    Receive Nothing In Time