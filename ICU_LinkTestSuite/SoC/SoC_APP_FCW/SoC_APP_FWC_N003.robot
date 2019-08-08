*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_N003
    [Documentation]  测试SoC接收到OutOfRecvWin范围内的NoNAK数据包是否会丢弃不处理
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_Test_NoNAK_Pkt_Out_Of_Recv_Win
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time