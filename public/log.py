#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import logging.config
reload(sys)
sys.setdefaultencoding('utf8')
#读取日志的配置文件
file = '../conf/logging.conf'
print file
logging.config.fileConfig(file)
#选择一个日志格式
logger=logging.getLogger('simpleExample')
def debug(msg):
    logger.debug(msg)
def info(msg):
    logger.info(msg)
def warn(msg):
    logger.warn(msg)
def error(msg):
    logger.error(msg)
def critical(msg):
    logger.critical(msg)
if __name__=='__main__':
    debug('错错错')
    info('中中中asdds')
    warn('中中中a')
    error('中中中a message')
    critical('中中中a message')