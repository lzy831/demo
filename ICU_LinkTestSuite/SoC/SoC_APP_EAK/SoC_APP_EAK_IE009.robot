*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE009
    [Documentation]  测试SoC在正常通信中，接收到包长错误的包，是否会影响正常EAK包的发送
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Send_BAD_PKT_INVALID_PL_LTA
    Test_Send_NoNAK_PKT_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time