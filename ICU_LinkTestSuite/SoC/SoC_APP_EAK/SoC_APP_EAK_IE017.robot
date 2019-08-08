*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE017
    [Documentation]  测试SoC在正常通信中，接收到HeaderChecksum错误的包，是否会影响正常EAK包的发送
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Send_BAD_PKT_INCORRECT_HC
    Test_Send_NoNAK_PKT_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time