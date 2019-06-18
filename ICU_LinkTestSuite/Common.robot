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
Send Acceptable SYN To MCU
    Send SYN Packet To Remote   &{Acceptable SYN To MCU}

Reply SYN ACK To Remote
    [Arguments]             &{syn_ack_param}
    &{SYN ACK Param} =      Library_Reply_SYN_ACK_To_Remote     &{syn_ack_param}
    Return From Keyword     &{SYN ACK Param}

Receive Acceptable SYN In Time
    &{SYN Param}=               Receive SYN In Time        ${Default Timeout In Seconds}
    MCU Can Accept SYN Param    &{SYN Param}
    Return From Keyword         &{SYN Param}

Send Negotiated SYN ACK To SoC
    [Arguments]             &{recv_syn_param}
    ${PSN}=                 Library_Get_PSN_From_Param          &{recv_syn_param}
    &{sent_param}=          Library_Send_SYN_ACK_To_SoC         ${PSN}
    Return From Keyword     &{sent_param}

Receive Matched SYN ACK In Time
    [Arguments]                                 &{sent_syn_param}
    &{recv_syn_ack_param}=                      Library_Receive_ACK_In_Time     ${Default Timeout In Seconds}    &{sent_syn_param}
    Library_SYN_Negotiated_Param_Can_Match      &{recv_syn_ack_param}
    Return From Keyword                         &{recv_syn_ack_param}












*** Keywords ***
MCU Suite Setup
    Set MCU Default Param       &{Default MCU SYN Param}
    Set MCU Negotiated Param    &{Negotiate MCU Param}
    Open Transport

MCU Suite Teardown
    Close Transport

Open Transport
    Library Open Transport

Close Transport
    Library Close Transport

Send RST To Soc
    # Library Reset Transport
    Library Send RST To Remote

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

Receive ACK In Time
    [Arguments]                      &{sent_response_param}
    Library Receive ACK In Time      &{sent_response_param}

Receive Nothing In Time
    Library Receive Nothing In Time     ${Default Timeout In Seconds}

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


