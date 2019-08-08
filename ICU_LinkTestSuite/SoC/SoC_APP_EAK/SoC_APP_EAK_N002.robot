*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_N002
    [Documentation]  测试SoC是否可以正常响应并处理EAK数据包
    MCU_SYN
    Test_Start
    Test_Request_Three_NoNAK_PKT
    Received_Test_NoNAK_ACK
    Received_Test_NoNAK_ACK_And_Drop
    Received_Test_NoNAK_ACK
    Send_EAK
    Test_Received_Missing_NoNAK
    Send_ACK
    Received_Nothing_In_Time