*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_IE014
    [Documentation]  测试SoC在正常通信中，接收到不合法数据包(RST,EAK)等，或者收到OutOfRecvWin的失序包是否会影响EAK包的发送
    MCU_SYN
    Test_Start
    Test_Request_Two_NoNAK_PKT
    Received_Test_NoNAK_ACK_And_Drop
    Received_Test_NoNAK_ACK
    Send_BAD_PKT_RST_With_PAN
    Send_EAK
    Test_Received_Missing_NoNAK
    Send_ACK
    Received_Nothing_In_Time