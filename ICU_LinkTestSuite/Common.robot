*** Settings ***
Library  icu_test_api.py




*** Variables ***
${Default Soc MaxNumOfPkt}      5
${Default Soc MaxRecvPktLen}     2048
${Default Soc RetransTimeout}   400
${Default Soc CumAckTimeout}    22
${Default Soc MaxCumOfRetrans}  10
${Default Soc MaxCumAck}        3

${Default MCU MaxNumOfPkt}      4
${Default MCU MaxRecvPktLen}     256
${Default MCU RetransTimeout}   400
${Default MCU CumAckTimeout}    22
${Default MCU MaxCumOfRetrans}  10
${Default MCU MaxCumAck}        3


&{Default MCU SYN Param}
...     MaxNumOfOutStdPkts=${Default MCU MaxNumOfPkt}
...     MaxRecvPktLen=${Default MCU MaxRecvPktLen}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxCumOfRetrans=${Default MCU MaxCumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck}

${Default Timeout In Seconds}   2


*** Variables ***
&{Acceptable SYN To MCU}
...     MaxNumOfOutStdPkts=${Default Soc MaxNumOfPkt}
...     MaxRecvPktLen=${Default Soc MaxRecvPktLen}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxCumOfRetrans=${Default MCU MaxCumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck} 

&{Acceptable SYN Respone From MCU}
...     RetransTimeout=${Default Soc RetransTimeout}
...     CumAckTimeout=${Default Soc CumAckTimeout}
...     MaxCumOfRetrans=${Default Soc MaxCumOfRetrans}
...     MaxCumAck=${Default Soc MaxCumAck}

&{Acceptable SYN To SoC}
...     MaxNumOfOutStdPkts=${Default MCU MaxNumOfPkt}
...     MaxRecvPktLen=${Default MCU MaxRecvPktLen}
...     RetransTimeout=${Default Soc RetransTimeout}
...     CumAckTimeout=${Default Soc CumAckTimeout}
...     MaxCumOfRetrans=${Default Soc MaxCumOfRetrans}
...     MaxCumAck=${Default Soc MaxCumAck} 

&{Acceptable SYN Respone From MCU}
...     RetransTimeout=${Default MCU RetransTimeout}
...     CumAckTimeout=${Default MCU CumAckTimeout}
...     MaxCumOfRetrans=${Default MCU MaxCumOfRetrans}
...     MaxCumAck=${Default MCU MaxCumAck} 



*** Keywords ***
Send Acceptable SYN To MCU
    Send SYN Packet To Remote   &{Acceptable SYN To MCU}

Receive Correct Response With Same Param In Time
    Receive SYN Response In Time   ${Default Timeout In Seconds}	&{Acceptable SYN Respone From MCU}

Receive Acceptable SYN In Time
    &{SYN Param}=    Receive SYN In Time        ${Default Timeout In Seconds}
    MCU Can Accept SYN Param    &{SYN Param}
    Return From Keyword         &{SYN Param}











*** Keywords ***
MCU Suite Setup
    Set MCU Default Param       &{Default MCU SYN Param}  
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

Send SYN ACK to Soc
    [Arguments]                                              &{recved_syn_param}
    &{SYN ACK Param} =      Library Send SYN ACK to Soc      &{recved_syn_param}
    Return From Keyword     &{SYN ACK Param}

Send NAK to Soc
    Library Send NAK to Soc

Hold On A While
    Library_Hold_On_A_While

Receive SYN In Time
    [Arguments]                                     ${timeout}
    &{SYN Param}=   Library Receive SYN In Time     ${timeout}
    Return From Keyword    &{SYN Param}

Receive SYN Response In Time
    [Arguments]                             ${timeout}	&{syn_param}
    Library Recvive SYN Response In Time    ${timeout}  &{syn_param}

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



