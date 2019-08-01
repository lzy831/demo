*** Settings ***
Library  icu_test_api.py




*** Variables ***
${Default Soc LinkVersion}      1
${Default Soc MaxNumOfPkt}      5
${Default Soc MaxRecvPktLen}     2048
${Default Soc RetransTimeout}   400
${Default Soc CumAckTimeout}    22
${Default Soc MaxNumOfRetrans}  10
${Default Soc MaxCumAck}        3


${Default MCU LinkVersion}      1
${Default MCU MaxNumOfPkt}      4
${Default MCU MaxRecvPktLen}     256
${Default MCU RetransTimeout}   400
${Default MCU CumAckTimeout}    22
${Default MCU MaxNumOfRetrans}  10
${Default MCU MaxCumAck}        3


${Negotiated MCU LinkVersion}      1
${Negotiated MCU MaxNumOfPkt}       4
${Negotiated MCU MaxRecvPktLen}     256
${Negotiated MCU RetransTimeout}    400
${Negotiated MCU CumAckTimeout}     22
${Negotiated MCU MaxNumOfRetrans}   12
${Negotiated MCU MaxCumAck}         3


&{Default MCU SYN Param}
...     LinkVersion=${Default MCU LinkVersion}
...     MaxNumOfOutStdPkts=${Default MCU MaxNumOfPkt}
...     MaxRecvPktLen=${Default MCU MaxRecvPktLen}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxNumOfRetrans=${Default MCU MaxNumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck}

&{Negotiate MCU Param}
...     LinkVersion=${Negotiated MCU LinkVersion}
...     MaxNumOfOutStdPkts=${Default MCU MaxNumOfPkt}
...     MaxRecvPktLen=${Default MCU MaxRecvPktLen}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxNumOfRetrans=${Negotiated MCU MaxNumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck}


${Default Timeout In Seconds}   2


*** Variables ***
&{Acceptable SYN To MCU}
...     LinkVersion=${Default MCU LinkVersion}
...     MaxNumOfOutStdPkts=${Default Soc MaxNumOfPkt}
...     MaxRecvPktLen=${Default Soc MaxRecvPktLen}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxNumOfRetrans=${Default MCU MaxNumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck} 


&{Acceptable SYN Respone From MCU}
...     RetransTimeout=${Default Soc RetransTimeout}
...     CumAckTimeout=${Default Soc CumAckTimeout}
...     MaxNumOfRetrans=${Default Soc MaxNumOfRetrans}
...     MaxCumAck=${Default Soc MaxCumAck}

&{Acceptable SYN To SoC}
...     LinkVersion=${Default SoC LinkVersion}
...     MaxNumOfOutStdPkts=${Default MCU MaxNumOfPkt}
...     MaxRecvPktLen=${Default MCU MaxRecvPktLen}
...     RetransTimeout=${Default Soc RetransTimeout}
...     CumAckTimeout=${Default Soc CumAckTimeout}
...     MaxNumOfRetrans=${Default Soc MaxNumOfRetrans}
...     MaxCumAck=${Default Soc MaxCumAck} 

&{Acceptable SYN Respone From MCU}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxNumOfRetrans=${Default MCU MaxNumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck} 



*** Keywords ***
Send_RST
    Library_Send_RST

Send_SYN
    Library_Send_SYN

Send_ACK
    Library_Send_ACK

Send_NAK
    Library_Send_NAK

Send_EAK
    Library_Send_Random_EAK

Send_APP
    Library_Send_APP

Send_Negotiated_SYN_ACK
    Library_Send_Negotiated_SYN_ACK

Send_SYN_ACK
    Library_Send_SYN_ACK

Send_Random_EAK
    Library_Send_Random_EAK

Send_BAD_SOP_PKT
    Library_Send_BAD_PKT_INVALID_SOP

Send_BAD_PL_PKT
    Library_Send_BAD_PL_PKT

Send_BAD_PAN_PKT
    Library_Send_BAD_PAN_PKT

Reply_SYN
    Library_Reply_SYN

MCU_SYN
    Library_MCU_SYN

Retransmit_SYN_ACK
    Library_Retransmit_SYN_ACK

##################################################################
Received_Acceptable_SYN_In_Time
    Library_Received_Acceptable_SYN_In_Time

Received_ACK_In_Time
    Library_Received_ACK_In_Time

Received_Nothing_In_Time
    Library_Received_Nothing_In_Time

Update_SYN_Negotiable_Param
    Library_Update_SYN_Negotiable_Param

Received_Negotiable_SYN_In_Time
    Library_Received_Negotiable_SYN_In_Time

Received_Acceptable_SYN_ACK_In_Time
    Library_Received_Acceptable_SYN_ACK_In_Time

Received_Test_NoNAK
    Library_Received_Test_NoNAK

##################################################################
Test_Start
    Library_Test_Start

Test_Send_NoNAK_PKT
    Library_Test_Send_NoNAK_PKT

Test_Request_NoNAK_PKT
    Library_Test_Request_NoNAK_PKT


##################################################################
*** Keywords ***
MCU_Suite_Setup
    Library_Open_Transport

MCU_Suite_Teardown
    Library_Close_Transport

SoC_Suite_Setup
    Library_Reset_For_Soc
    Library_Open_Transport

SoC_Suite_Teardown
    Library_Close_Transport
