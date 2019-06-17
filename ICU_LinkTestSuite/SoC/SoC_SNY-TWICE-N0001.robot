*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_正常流程_协商二次_测试两次协商正常情况
    Send RST To Soc
    &{SYN Param}=                   Receive SYN In Time                     ${Default Timeout In Seconds}
    &{Negotiated SYN ACK Param}=    Send Negotiated SYN ACK To SoC          &{SYN Param}
    &{SYN ACK Param}=               Receive Matched SYN ACK In Time         &{Negotiated SYN ACK Param}
    &{SYN ACK Param}=               Reply SYN ACK To Remote                 &{SYN ACK Param}
    Receive ACK In Time             &{SYN ACK Param}
    Receive Nothing In Time
