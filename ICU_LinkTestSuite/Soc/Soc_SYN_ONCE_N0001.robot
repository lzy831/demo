*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_正常流程_协商一次_全部数据包一次成功
    [Documentation]     Soc端可以通过一次SYN协商握手成功
    Send_RST
    Received_Acceptable_SYN_In_Time
    Reply_SYN
    Received_ACK_In_Time
    Received_Nothing_In_Time