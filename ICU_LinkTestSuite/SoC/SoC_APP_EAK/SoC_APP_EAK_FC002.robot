*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_FC002
    [Documentation]  测试SoC是否在累计未确认达上限和超时确认时都会进行一个EAK统计和发送
    MCU_SYN
    Test_Start
    Send_Test_NoNAK_Pkt
    Send_Test_NoNAK_Pkt
    Send_Test_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Retransmit_Previous_NoNAK_Pkt
    Received_EAK_In_Time
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time