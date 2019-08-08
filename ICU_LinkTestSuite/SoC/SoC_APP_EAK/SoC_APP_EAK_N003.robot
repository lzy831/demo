*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_N003
    [Documentation]  测试SoC是否会等到缺失的数据包到来后再顺序的去处理数据包
    MCU_SYN
    Test_Start
    Test_Request_NoNAK_PKT_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_Test_NoNAK_ACK
    Send_ACK
    Received_Nothing_In_Time