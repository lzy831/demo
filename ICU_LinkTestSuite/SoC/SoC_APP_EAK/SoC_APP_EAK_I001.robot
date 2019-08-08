*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_I001
    [Documentation]  测试SoC在正常通信中，接收到脱离序列的SYN包，是会影响正常EAK的逻辑处理
    MCU_SYN
    Test_Start
    Test_Send_NoNAK_PKT
    Send_SYN_Skip_One_PSN
    Received_EAK_In_Time
    Test_Send_Missing_NoNAK_PKT_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time