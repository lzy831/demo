*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_FC001
    [Documentation]  测试SoC在正常通信中，接收到超过己端MRPL的数据包时，是否可以丢弃不处理
    MCU_SYN
    Test_Start
    Send_Test_NoNAK_Pkt
    Send_Bad_Pkt_OverLength
    Send_Test_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time