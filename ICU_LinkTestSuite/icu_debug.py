#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from robot.api import logger
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(thread)d - %(message)s')
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)

def skdebug(*args):
    s = ''
    for i in args:
        s += (str(i) + ' ')

    # logger.debug(s)
    # logger.trace(s)

    # logger.info(s)
    # print(s)
    logger.debug(s)
