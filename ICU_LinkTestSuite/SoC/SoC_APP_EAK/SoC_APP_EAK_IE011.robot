*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE011
    [Documentation]  测试SoC在正常通信中，接收到不合法数据包(RST,EAK)等，或者收到OutOfRecvWin的失序包是否丢弃，不影响EAK包的处理
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Send_RST_With_PSN
    Test_Send_NoNAK_PKT_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time