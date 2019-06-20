#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from robot.api import logger


def skdebug(*args):
    s = ''
    for i in args:
        s += (str(i) + ' ')
    # logger.debug(s)
    # logger.trace(s)

    # logger.info(s)
    print(s)