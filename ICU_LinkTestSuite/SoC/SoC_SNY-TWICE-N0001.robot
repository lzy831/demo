*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_正常流程_协商二次_测试两次协商正常情况
    Send_RST
    Received_Acceptable_SYN_In_Time
    Send_Negotiated_SYN_ACK
    &{Negotiated ACK Param}=        Receive Matched SYN ACK In Time         &{Negotiated Param}
    &{SYN ACK Param}=               Reply_SYN_ACK_To_Remote                 &{Negotiated ACK Param}
    Received_ACK_In_Time             &{SYN ACK Param}
    Received_Nothing_In_Time
