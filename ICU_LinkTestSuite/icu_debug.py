#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from robot.api import logger
import inspect
import logging

plogger = logging.getLogger()
plogger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(thread)d - %(message)s')
consoleHandler.setFormatter(formatter)

plogger.addHandler(consoleHandler)

def skdebug(*args):
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    # s = function_name + ': '
    s = ''
    for i in args:
        s += (str(i) + ' ')

    # logger.debug(s)
    # logger.trace(s)

    logger.info(s)
    # print(s)

    # plogger.debug(s)
    # logger.debug(s)


def sk_library_api_begin():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    skdebug("[Robot Test Library API]",function_name,'Begin')

def sk_library_api_end():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    skdebug("[Robot Test Library API]",function_name,'End')

def sk_api_begin():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    skdebug(function_name,'Begin')

def sk_api_end():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    skdebug(function_name,'End')