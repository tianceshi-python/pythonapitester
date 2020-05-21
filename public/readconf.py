#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ConfigParser
import codecs
import os

def readconf(conf_dir='conf/pub_pre.conf',):
    cf = ConfigParser.ConfigParser()
    allconf = {}
    file = os.path.join(os.path.dirname(os.path.dirname(__file__)), conf_dir)
    cf.readfp(codecs.open(os.path.normpath(file), "r", "utf-8-sig"))
    for section in cf.sections():
        allconf[section] = dict(cf.items(section))
    return allconf
#prd配置
#allconf = readconf('conf/pub_prd.conf')
#dev配置
#allconf = readconf('conf/pub_dev.conf')

#pre配置
allconf = readconf('conf/pub_prd.conf')

if __name__=="__main__":
    ext = readconf()
    print ext
    print ext['testcase']['casefile']
