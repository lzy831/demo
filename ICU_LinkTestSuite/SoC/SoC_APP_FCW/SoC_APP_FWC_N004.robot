*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_N004
    [Documentation]  测试后SoC在接收到接收窗口内重复的数据包时，是否会立即执行数据包确认
    MCU_SYN
    Test_Start
    Send_Test_MNOOSP_NoNAK_Pkt_Skip_One_PSN
    Received_EAK_In_Time
    Wait
    Retransmit_Third_NoNAK_In_SentQ
    Received_EAK_In_Time