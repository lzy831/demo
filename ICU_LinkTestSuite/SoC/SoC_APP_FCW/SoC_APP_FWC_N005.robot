*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_APP_FWC_N005
    [Documentation]  测试SoC在发送窗口第一个数据包未被ACK之前，不会移动发送窗口，也不会发送超出当前滑动窗口范围的数据包
    MCU_SYN
    Test_Start
    Request_MaxOutOfStdPkt_Add_Two_Test_NoNAK_Pkt
    Received_MaxOutOfStdPkt_Test_NoNAK_And_Drop_First
    Send_EAK
    Received_Test_NoNAK
    Send_ACK
    Received_Test_NoNAK
    Received_Test_NoNAK
    Send_ACK