*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_N001
    [Documentation]  测试SoC是否可以正常发送EAK数据包
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Test_Send_NoNAK_PKT_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time