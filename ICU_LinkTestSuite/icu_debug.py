#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from robot.api import logger


def skdebug(*args):
    s = ''
    for i in args:
        s += (str(i) + ' ')
    # logger.debug(s)
    logger.info(s)
    # logger.trace(s)