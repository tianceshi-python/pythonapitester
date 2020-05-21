#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time
import urllib
import os,sys
sys.path.append('../')
from public.Myrequests import requests_sig
from public.log import *
from public.readconf import allconf
from public.excelrd import *
import json
import jsonpath
import re

#接口配置（配置与测试数据分离）。接口配在这里，数据从excel获取。这里配置对应 http://123.57.12.62/meeting/rest-api-create-conf/中的 1-8
enterpriseId = allconf['enterprise']['enterpriseid']
ip = allconf['enterprise']['sdk_ip']
iauth_ip = allconf['sdk_login']['iauth_ip']
internal_nginx_ip = allconf['sdk_login']['internal_nginx_ip']
headers_json = {'content-type': 'application/json'}
token = str(allconf['enterprise']['token'])
url = 'https://172.18.160.42/api/rest/external/v1/en/order?enterpriseId=e608e0f43963706372c006235c79d01890e82966'
data = {"enterpriseId":"ff80808162469b810162f5ed6ce8237d",
"externalEmail":"wulihua@xylink.com",
"externalPhone":"10186515916",
"externalName":"abcAPRE",
"externalId":"ff8vfbftsngtfsdgdfhtvers1241",
"items":[
{"productCode":"VXY-1000-0049",
"productNum":1,
"productCycle":1,
"externalItemId":"ff8vfbftsngtfsdgdfhtvers1241"}
]}

#req = requests_sig('POST', url,data,token, verify=False,headers=headers_json)

aaa = 'Traceback (most recent call last):  File "C:\myworkspace\git_back\pythonapitester\testcase\test_creat_sdkroom.py", line 234, in test_batch_get_room     raise e AssertionError  9000043836  9000043836 '
bbb = ''
print aaa[aaa.find('AssertionError'):]
print bbb[bbb.find('AssertionError'):]
