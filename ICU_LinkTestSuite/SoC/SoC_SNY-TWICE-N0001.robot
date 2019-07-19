*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
握手_正常流程_协商二次_测试两次协商正常情况
    # Update_SYN_Negotiable_Param
    # Send_RST
    # Received_Negotiable_SYN_In_Time
    # Reply_SYN
    # Received_Acceptable_SYN_ACK_In_Time
    # Reply_SYN
    # Received_ACK_In_Time
    # Received_Nothing_In_Time