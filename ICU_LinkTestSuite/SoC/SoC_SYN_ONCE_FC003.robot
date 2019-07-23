*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
Soc_SYN_ONCE_FC003
    [Documentation]  握手过程中穿插>Maximum Received Packet Length的包
