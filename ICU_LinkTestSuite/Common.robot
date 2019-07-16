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

Send_Negotiated_SYN_ACK
    Library_Send_Negotiated_SYN_ACK

Reply_SYN
    Library_Reply_SYN




Received_Acceptable_SYN_In_Time
    Library_Received_Acceptable_SYN_In_Time

Received_ACK_In_Time
    Library_Received_ACK_In_Time

Received_Nothing_In_Time
    Library_Received_Nothing_In_Time












Send Acceptable SYN To MCU
    Send SYN Packet To Remote   &{Acceptable SYN To MCU}







Receive Matched SYN ACK In Time
    [Arguments]                                 &{sent_syn_param}
    &{recv_syn_ack_param}=                      Library_Received_ACK_In_Time     ${Default Timeout In Seconds}    &{sent_syn_param}
    Library_SYN_Negotiated_Param_Can_Match      &{recv_syn_ack_param}
    Return From Keyword                         &{recv_syn_ack_param}












*** Keywords ***
MCU Suite Setup
    Set MCU Default Param       &{Default MCU SYN Param}
    Set MCU Negotiated Param    &{Negotiate MCU Param}
    Library_Open_Transport

MCU Suite Teardown
    Library_Close_Transport




Send SYN To Soc
    [Arguments]                 &{syn_param}
    Library Send SYN To Soc     &{syn_param}



Send NAK to Soc
    Library Send NAK to Soc

Hold On A While
    Library_Hold_On_A_While

Receive SYN In Time
    [Arguments]             ${timeout}
    &{SYN Param} =          Library_Receive_SYN_In_Time     ${timeout}
    Return From Keyword     &{SYN Param}

Receive SYN ACK In Time
    [Arguments]             ${timeout}      &{syn_param}
    &{SYN ACK Param}=       Library Recvive SYN ACK In Time    ${timeout}      &{syn_param}
    Return From Keyword     &{SYN ACK Param}





*** Keywords ***
MCU Can Accept SYN Param
    [Arguments]                         &{syn_param}
    Library MCU Can Accept SYN Param    &{syn_param}

Set MCU Default Param
    [Arguments]                         &{mcu_param}
    Library Set MCU Default Param       &{mcu_param}

Set MCU Negotiated Param
    [Arguments]                         &{param}
    Library_Set_MCU_Negotiated_Param    &{param}


