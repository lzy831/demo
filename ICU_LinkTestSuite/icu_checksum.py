#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from icu_debug import *

def clac_checksum(data_without_checksum: bytes):
    skdebug('clac_checksum begin, data:', data_without_checksum.hex())
    return cumulative_sum_checksum(data_without_checksum)
    # return crc_checksum(data_without_checksum)

def crc_checksum(data_without_checksum: bytes):
    pass

def cumulative_sum_checksum(data_without_checksum: bytes):
    checksum = 0
    for value in data_without_checksum:
        checksum = checksum + value
        # skdebug('checksum', hex(checksum), 'value', value)
    return checksum