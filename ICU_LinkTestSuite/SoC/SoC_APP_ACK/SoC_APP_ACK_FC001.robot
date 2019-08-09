*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_ACK_FC001
    [Documentation]  SoC在正常通信中,收到超过处理长度的数据包，是否可以丢弃
    MCU_SYN
    Test_Start
    Send_BAD_PKT_TEST_NoNAK_Exceed_Remote_MRPL
    Received_Nothing_In_Time