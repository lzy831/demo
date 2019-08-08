*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_N001
    [Documentation]  测试SoC端是否不处理接收窗口之外（OutOfRecvWin范围内）的NoNAK数据包
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Send_Test_Missing_NoNAK_Pkt_According_EAK
    Received_ACK_In_Time
    Received_Nothing_In_Time