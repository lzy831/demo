*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_EAK_FC003
    [Documentation]  测试SoC是否可以在Cumulative Acknowledgement Timeout时间内发送出EAK
    MCU_SYN
    Test_Start
    Send_Test_NoNAK_Pkt
    Send_OutSeq_NoNAK_Pkt_And_Received_EAK_In_LimitTime
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time