*** Settings ***
Resource    ..\\Common.robot

*** Test Cases ***
SoC_SNY_TWICE_N0002
    [Documentation]  握手_正常流程_协商二次_测试两次协商不成功的情况
    Send_RST