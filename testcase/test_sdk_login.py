#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time
import urllib
import os,sys
sys.path.append('../')
from public.Myrequests import requests_normal
from public.log import *
from public.readconf import allconf
from public.excelrd import *
import json
import hashlib
import jsonpath
import re
import random
import string

#接口配置（配置与测试数据分离）。接口配在这里，数据从excel获取。这里配置对应 http://123.57.12.62/meeting/rest-api-create-conf/中的 1-8
conf_login_soft = {'method': 'PUT','uri': '/api/rest/v3/en/login'}
conf_login_tvbox = {'method': 'PUT','uri': '/api/rest/v3/en/tvbox/login'}
conf_login_bruce = {'method': 'PUT','uri': '/api/rest/v3/bruce/loginv2'}
conf_UnbindDevice = {'method': 'PUT','uri': '/api/rest/internal/v1/device/internalUnbindDevice'}
conf_addsn_bruce = {'method': 'POST','uri': '/api/rest/internal/v3/bruce'}









class login_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.iauth_ip = allconf['sdk_login']['iauth_ip']
        self.internal_nginx_ip = allconf['sdk_login']['internal_nginx_ip']
        self.headers_json = {'content-type': 'application/json'}
        self.token = str(allconf['enterprise']['token'])
        self.soft = json.loads(allconf['sdk_login']['soft'])
        self.ne2005 = json.loads(allconf['sdk_login']['ne2005'])
        self.ne60 = json.loads(allconf['sdk_login']['ne60'])
        self.me20 = json.loads(allconf['sdk_login']['me20'])
        self.me40 = json.loads(allconf['sdk_login']['me40'])
        self.tvbox = json.loads(allconf['sdk_login']['tvbox'])
        self.me90 = json.loads(allconf['sdk_login']['me90'])


    def getsn(self,SN_pre):
        sn1 = SN_pre + "".join(random.sample(string.ascii_uppercase, 12-len(SN_pre)))
        m = hashlib.md5()
        m.update(sn1+')G$d')
        sn2 = m.hexdigest()[28:].upper()
        return sn1+sn2


    def test_soft_login(self):

        softinfo = self.soft
        #软终端登录
        info(u'软终端登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":softinfo['phone'],"deviceSn":"111222", "deviceDisplayName":"", "deviceType":5, "model":None, "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":None, "hardVersion":None, "packageName":None,"password":softinfo['password']}

        login_soft = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_soft.status_code, 200, msg=u'软终端登录')
            self.assertRegexpMatches(str(login_soft.json()['userDevice']['securityKey']),'.+',msg=u'软终端登录')
            self.assertRegexpMatches(login_soft.text,'12345678899',msg=u'软终端登录')
            self.assertEqual(login_soft.json()['userDevice']['type'],5,msg=u'软终端登录')

        except Exception, e:
            error(e)
            error(login_soft.url)
            error(login_soft.request.body)
            error(login_soft.text)
            raise e
        time.sleep(1)

    def test_ne2005_login(self):
        deviceinfo = self.ne2005
        sn = self.getsn(deviceinfo['sn_pre'])
        #ne2005登录
        info(u'ne2005登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}

        login_ne2005 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne2005.status_code, 200, msg=u'ne2005登录')
            self.assertRegexpMatches(str(login_ne2005.json()['userDevice']['type']),'2',msg=u'ne2005登录')
            self.assertRegexpMatches(str(login_ne2005.json()['userDevice']['securityKey']),'.+',msg=u'ne2005登录')
            self.assertRegexpMatches(str(login_ne2005.json()['userDevice']['nemoNumber']),'^\d{6}$',msg=u'ne2005登录')
            self.assertEqual(login_ne2005.json()['userDevice']['category'],'NE2005',msg=u'ne2005登录')

            id_2005 = login_ne2005.json()['userDevice']['id']
            sn_2005 = login_ne2005.json()['userDevice']['deviceSN']
            userProfileID_ne2005 = login_ne2005.json()['userDevice']['userProfileID']
            nemoNumber_ne2005 = login_ne2005.json()['nemoNumber']
        except Exception, e:
            error(e)
            error(login_ne2005.url)
            error(login_ne2005.request.body)
            error(login_ne2005.text)
            raise e
        time.sleep(1)

        #NE2005重复登录
        info(u'NE2005重复登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}

        login_ne2005 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne2005.status_code, 200, msg=u'NE2005重复登录')
            self.assertEqual(login_ne2005.json()['userDevice']['id'],id_2005,msg=u'NE2005重复登录')
            self.assertEqual(login_ne2005.json()['nemoNumber'],nemoNumber_ne2005,msg=u'NE2005重复登录')
            self.assertEqual(login_ne2005.json()['userDevice']['deviceSN'],sn_2005,msg=u'NE2005重复登录')
            self.assertEqual(login_ne2005.json()['userDevice']['userProfileID'],userProfileID_ne2005,msg=u'NE2005重复登录')
            self.assertEqual(login_ne2005.json()['userDevice']['category'],'NE2005',msg=u'NE2005重复登录')

        except Exception, e:
            error(e)
            error(login_ne2005.url)
            error(login_ne2005.request.body)
            error(login_ne2005.text)
            raise e
        time.sleep(1)
        #解绑ne2005
        info(u'解绑ne2005')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_2005,"deviceSN":sn_2005,"userProfileID":userProfileID_ne2005}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑ne2005')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑ne2005')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #ne2005解绑后重新登录
        info(u'ne2005解绑后重新登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}
        login_ne2005_2 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne2005_2.status_code, 200, msg=u'ne2005解绑后重新登录')
            self.assertNotEqual(login_ne2005_2.json()['userDevice']['id'],id_2005,msg=u'ne2005解绑后重新登录')
            self.assertNotEqual(login_ne2005_2.json()['nemoNumber'],nemoNumber_ne2005,msg=u'ne2005解绑后重新登录')
            self.assertEqual(login_ne2005_2.json()['userDevice']['deviceSN'],sn_2005,msg=u'ne2005解绑后重新登录')
            self.assertEqual(login_ne2005_2.json()['userDevice']['userProfileID'],userProfileID_ne2005,msg=u'ne2005解绑后重新登录')
            id_2005_2 = login_ne2005_2.json()['userDevice']['id']
            sn_2005_2 = login_ne2005_2.json()['userDevice']['deviceSN']
            userProfileID_ne2005_2 = login_ne2005_2.json()['userDevice']['userProfileID']
            self.assertEqual(login_ne2005_2.json()['userDevice']['category'],'NE2005',msg=u'NE2005重复登录')
        except Exception, e:
            error(e)
            error(login_ne2005_2.url)
            error(login_ne2005_2.request.body)
            error(login_ne2005_2.text)
            raise e
        time.sleep(1)
        #解绑ne2005
        info(u'解绑ne2005')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_2005_2,"deviceSN":sn_2005_2,"userProfileID":userProfileID_ne2005_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑ne2005')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑ne2005')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑ne2005，验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_2005_2, "deviceSN": sn_2005_2, "userProfileID": userProfileID_ne2005_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑ne2005，验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑ne2005，验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)

    def test_ne60_login(self):
        deviceinfo = self.ne60
        sn = self.getsn(deviceinfo['sn_pre'])
        #ne60登录
        info(u'ne60登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}

        login_ne60 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne60.status_code, 200, msg=u'ne60登录')
            self.assertRegexpMatches(str(login_ne60.json()['userDevice']['type']),'2',msg=u'ne60登录')
            self.assertRegexpMatches(str(login_ne60.json()['userDevice']['securityKey']),'.+',msg=u'ne60登录')
            self.assertRegexpMatches(str(login_ne60.json()['userDevice']['nemoNumber']),'^\d{6}$',msg=u'ne60登录')
            self.assertEqual(login_ne60.json()['userDevice']['category'],'NE60',msg=u'ne60登录')

            id_60 = login_ne60.json()['userDevice']['id']
            sn_60 = login_ne60.json()['userDevice']['deviceSN']
            userProfileID_ne60 = login_ne60.json()['userDevice']['userProfileID']
            nemoNumber_ne60 = login_ne60.json()['nemoNumber']
        except Exception, e:
            error(e)
            error(login_ne60.url)
            error(login_ne60.request.body)
            error(login_ne60.text)
            raise e
        time.sleep(1)

        #ne60重复登录
        info(u'ne60重复登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}

        login_ne60 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne60.status_code, 200, msg=u'ne60重复登录')
            self.assertEqual(login_ne60.json()['userDevice']['id'],id_60,msg=u'ne60重复登录')
            self.assertEqual(login_ne60.json()['nemoNumber'],nemoNumber_ne60,msg=u'ne60重复登录')
            self.assertEqual(login_ne60.json()['userDevice']['deviceSN'],sn_60,msg=u'ne60重复登录')
            self.assertEqual(login_ne60.json()['userDevice']['userProfileID'],userProfileID_ne60,msg=u'ne60重复登录')
            self.assertEqual(login_ne60.json()['userDevice']['category'],'NE60',msg=u'ne60重复登录')

        except Exception, e:
            error(e)
            error(login_ne60.url)
            error(login_ne60.request.body)
            error(login_ne60.text)
            raise e
        time.sleep(1)
        #解绑ne60
        info(u'解绑ne60')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_60,"deviceSN":sn_60,"userProfileID":userProfileID_ne60}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑ne60')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑ne60')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #ne60解绑后重新登录
        info(u'ne60解绑后重新登录')
        url_login_soft = 'http://'+ self.iauth_ip+ conf_login_soft['uri']
        data = {"account":None,"deviceSn":sn+deviceinfo['finger'], "deviceDisplayName":"", "deviceType":deviceinfo['deviceType'], "model":deviceinfo['model'], "cpu":"", "cores":0, "freq":0, "deviceToken":None, "softVersion":deviceinfo['softVersion'], "hardVersion":deviceinfo['hardVersion'], "packageName":deviceinfo['packageName'],"password":None}
        login_ne60_2 = requests_normal(conf_login_soft['method'], url_login_soft,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_ne60_2.status_code, 200, msg=u'ne60解绑后重新登录')
            self.assertNotEqual(login_ne60_2.json()['userDevice']['id'],id_60,msg=u'ne60解绑后重新登录')
            self.assertNotEqual(login_ne60_2.json()['nemoNumber'],nemoNumber_ne60,msg=u'ne60解绑后重新登录')
            self.assertEqual(login_ne60_2.json()['userDevice']['deviceSN'],sn_60,msg=u'ne60解绑后重新登录')
            self.assertEqual(login_ne60_2.json()['userDevice']['userProfileID'],userProfileID_ne60,msg=u'ne60解绑后重新登录')
            self.assertEqual(login_ne60_2.json()['userDevice']['category'],'NE60',msg=u'ne60解绑后重新登录')
            id_60_2 = login_ne60_2.json()['userDevice']['id']
            sn_60_2 = login_ne60_2.json()['userDevice']['deviceSN']
            userProfileID_ne60_2 = login_ne60_2.json()['userDevice']['userProfileID']
        except Exception, e:
            error(e)
            error(login_ne60_2.url)
            error(login_ne60_2.request.body)
            error(login_ne60_2.text)
            raise e
        time.sleep(1)
        #解绑ne60
        info(u'解绑ne60')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_60_2,"deviceSN":sn_60_2,"userProfileID":userProfileID_ne60_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑ne60')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑ne60')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑ne60,验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_60_2, "deviceSN": sn_60_2, "userProfileID": userProfileID_ne60_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑ne60,验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑ne60,验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        
        
    def test_me20_login(self):
        deviceinfo = self.me20
        sn = self.getsn(deviceinfo['sn_pre'])
        #me20登录
        info(u'me20登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN":sn,"packageName":deviceinfo['packageName'], "deviceModel":deviceinfo['deviceModel'], "category":deviceinfo['category']}

        login_me20 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me20.status_code, 200, msg=u'me20登录')
            self.assertRegexpMatches(str(login_me20.json()['userDevice']['type']),'8',msg=u'me20登录')
            self.assertRegexpMatches(str(login_me20.json()['userDevice']['securityKey']),'.+',msg=u'me20登录')
            self.assertRegexpMatches(str(login_me20.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'me20登录')
            self.assertEqual(login_me20.json()['userDevice']['category'],'ME20',msg=u'me20登录')
            id_me20 = login_me20.json()['userDevice']['id']
            sn_me20 = login_me20.json()['userDevice']['deviceSN']
            userProfileID_me20 = login_me20.json()['userDevice']['userProfileID']
            nemoNumber_me20 = login_me20.json()['nemoNumber']
        except Exception, e:
            error(e)
            error(login_me20.url)
            error(login_me20.request.body)
            error(login_me20.text)
            raise e
        time.sleep(1)

        #me20重复登录
        info(u'me20重复登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_me20 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me20.status_code, 200, msg=u'me20重复登录')
            self.assertEqual(login_me20.json()['userDevice']['id'],id_me20,msg=u'me20重复登录')
            self.assertEqual(login_me20.json()['nemoNumber'],nemoNumber_me20,msg=u'me20重复登录')
            self.assertEqual(login_me20.json()['userDevice']['deviceSN'],sn_me20,msg=u'me20重复登录')
            self.assertEqual(login_me20.json()['userDevice']['userProfileID'],userProfileID_me20,msg=u'me20重复登录')
            self.assertEqual(login_me20.json()['userDevice']['category'],'ME20',msg=u'me20重复登录')

        except Exception, e:
            error(e)
            error(login_me20.url)
            error(login_me20.request.body)
            error(login_me20.text)
            raise e
        time.sleep(1)
        #解绑me20
        info(u'解绑me20')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me20,"deviceSN":sn_me20,"userProfileID":userProfileID_me20}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me20')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me20')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #me20解绑后重新登录
        info(u'me20解绑后重新登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_me20_2 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me20_2.status_code, 200, msg=u'me20解绑后重新登录')
            self.assertRegexpMatches(str(login_me20.json()['userDevice']['type']),'8',msg=u'me20解绑后重新登录')
            self.assertNotEqual(login_me20_2.json()['userDevice']['id'],id_me20,msg=u'me20解绑后重新登录')
            self.assertNotEqual(login_me20_2.json()['nemoNumber'],nemoNumber_me20,msg=u'me20解绑后重新登录')
            self.assertEqual(login_me20_2.json()['userDevice']['deviceSN'],sn_me20,msg=u'me20解绑后重新登录')
            self.assertEqual(login_me20_2.json()['userDevice']['userProfileID'],userProfileID_me20,msg=u'me20解绑后重新登录')
            self.assertRegexpMatches(str(login_me20_2.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'me20解绑后重新登录')
            self.assertEqual(login_me20_2.json()['userDevice']['category'],'ME20',msg=u'me20解绑后重新登录')

            id_me20_2 = login_me20_2.json()['userDevice']['id']
            sn_me20_2 = login_me20_2.json()['userDevice']['deviceSN']
            userProfileID_me20_2 = login_me20_2.json()['userDevice']['userProfileID']


        except Exception, e:
            error(e)
            error(login_me20_2.url)
            error(login_me20_2.request.body)
            error(login_me20_2.text)
            raise e
        time.sleep(1)
        #解绑me20
        info(u'解绑me20')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me20_2,"deviceSN":sn_me20_2,"userProfileID":userProfileID_me20_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me20')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me20')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑me20,验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_me20_2, "deviceSN": sn_me20_2, "userProfileID": userProfileID_me20_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑me20,验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑me20,验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        
    def test_me40_login(self):
        deviceinfo = self.me40
        sn = self.getsn(deviceinfo['sn_pre'])
        #me40登录
        info(u'me40登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN":sn,"packageName":deviceinfo['packageName'], "deviceModel":deviceinfo['deviceModel'], "category":deviceinfo['category']}

        login_me40 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me40.status_code, 200, msg=u'me40登录')
            self.assertRegexpMatches(str(login_me40.json()['userDevice']['type']),'8',msg=u'me40登录')
            self.assertRegexpMatches(str(login_me40.json()['userDevice']['securityKey']),'.+',msg=u'me40登录')
            self.assertRegexpMatches(str(login_me40.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'me40登录')
            self.assertEqual(login_me40.json()['userDevice']['category'],'ME40',msg=u'me40登录')

            id_me40 = login_me40.json()['userDevice']['id']
            sn_me40 = login_me40.json()['userDevice']['deviceSN']
            userProfileID_me40 = login_me40.json()['userDevice']['userProfileID']
            nemoNumber_me40 = login_me40.json()['nemoNumber']
        except Exception, e:
            error(e)
            error(login_me40.url)
            error(login_me40.request.body)
            error(login_me40.text)
            raise e
        time.sleep(1)

        #me40重复登录
        info(u'me40重复登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_me40 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me40.status_code, 200, msg=u'me40重复登录')
            self.assertEqual(login_me40.json()['userDevice']['id'],id_me40,msg=u'me40重复登录')
            self.assertEqual(login_me40.json()['nemoNumber'],nemoNumber_me40,msg=u'me40重复登录')
            self.assertEqual(login_me40.json()['userDevice']['deviceSN'],sn_me40,msg=u'me40重复登录')
            self.assertEqual(login_me40.json()['userDevice']['userProfileID'],userProfileID_me40,msg=u'me40重复登录')
            self.assertEqual(login_me40.json()['userDevice']['category'],'ME40',msg=u'me40重复登录')

        except Exception, e:
            error(e)
            error(login_me40.url)
            error(login_me40.request.body)
            error(login_me40.text)
            raise e
        time.sleep(1)
        #解绑me40
        info(u'解绑me40')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me40,"deviceSN":sn_me40,"userProfileID":userProfileID_me40}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me40')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me40')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #me40解绑后重新登录
        info(u'me40解绑后重新登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_me40_2 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me40_2.status_code, 200, msg=u'me40解绑后重新登录')
            self.assertRegexpMatches(str(login_me40.json()['userDevice']['type']),'8',msg=u'me40解绑后重新登录')
            self.assertNotEqual(login_me40_2.json()['userDevice']['id'],id_me40,msg=u'me40解绑后重新登录')
            self.assertNotEqual(login_me40_2.json()['nemoNumber'],nemoNumber_me40,msg=u'me40解绑后重新登录')
            self.assertEqual(login_me40_2.json()['userDevice']['deviceSN'],sn_me40,msg=u'me40解绑后重新登录')
            self.assertEqual(login_me40_2.json()['userDevice']['userProfileID'],userProfileID_me40,msg=u'me40解绑后重新登录')
            self.assertRegexpMatches(str(login_me40_2.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'me40解绑后重新登录')
            self.assertEqual(login_me40_2.json()['userDevice']['category'],'ME40',msg=u'me40解绑后重新登录')

            id_me40_2 = login_me40_2.json()['userDevice']['id']
            sn_me40_2 = login_me40_2.json()['userDevice']['deviceSN']
            userProfileID_me40_2 = login_me40_2.json()['userDevice']['userProfileID']


        except Exception, e:
            error(e)
            error(login_me40_2.url)
            error(login_me40_2.request.body)
            error(login_me40_2.text)
            raise e
        time.sleep(1)
        #解绑me40
        info(u'解绑me40')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me40_2,"deviceSN":sn_me40_2,"userProfileID":userProfileID_me40_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me40')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me40')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑me40,验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_me40_2, "deviceSN": sn_me40_2, "userProfileID": userProfileID_me40_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑me40,验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑me40,验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        
    def test_tvbox_login(self):
        deviceinfo = self.tvbox
        sn = self.getsn(deviceinfo['sn_pre'])
        #tvbox登录
        info(u'tvbox登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN":sn,"packageName":deviceinfo['packageName'], "deviceModel":deviceinfo['deviceModel'], "category":deviceinfo['category']}

        login_tvbox = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_tvbox.status_code, 200, msg=u'tvbox登录')
            self.assertRegexpMatches(str(login_tvbox.json()['userDevice']['type']),'8',msg=u'tvbox登录')
            self.assertRegexpMatches(str(login_tvbox.json()['userDevice']['securityKey']),'.+',msg=u'tvbox登录')
            self.assertRegexpMatches(str(login_tvbox.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'tvbox登录')
            self.assertEqual(login_tvbox.json()['userDevice']['category'],'NP40',msg=u'tvbox登录')

            id_tvbox = login_tvbox.json()['userDevice']['id']
            sn_tvbox = login_tvbox.json()['userDevice']['deviceSN']
            userProfileID_tvbox = login_tvbox.json()['userDevice']['userProfileID']
            nemoNumber_tvbox = login_tvbox.json()['nemoNumber']
        except Exception, e:
            error(e)
            error(login_tvbox.url)
            error(login_tvbox.request.body)
            error(login_tvbox.text)
            raise e
        time.sleep(1)

        #tvbox重复登录
        info(u'tvbox重复登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_tvbox = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_tvbox.status_code, 200, msg=u'tvbox重复登录')
            self.assertEqual(login_tvbox.json()['userDevice']['id'],id_tvbox,msg=u'tvbox重复登录')
            self.assertEqual(login_tvbox.json()['nemoNumber'],nemoNumber_tvbox,msg=u'tvbox重复登录')
            self.assertEqual(login_tvbox.json()['userDevice']['deviceSN'],sn_tvbox,msg=u'tvbox重复登录')
            self.assertEqual(login_tvbox.json()['userDevice']['userProfileID'],userProfileID_tvbox,msg=u'tvbox重复登录')
            self.assertEqual(login_tvbox.json()['userDevice']['category'],'NP40',msg=u'tvbox重复登录')

        except Exception, e:
            error(e)
            error(login_tvbox.url)
            error(login_tvbox.request.body)
            error(login_tvbox.text)
            raise e
        time.sleep(1)
        #解绑tvbox
        info(u'解绑tvbox')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_tvbox,"deviceSN":sn_tvbox,"userProfileID":userProfileID_tvbox}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑tvbox')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑tvbox')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #tvbox解绑后重新登录
        info(u'tvbox解绑后重新登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN": sn, "packageName": deviceinfo['packageName'], "deviceModel": deviceinfo['deviceModel'],"category": deviceinfo['category']}
        login_tvbox_2 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_tvbox_2.status_code, 200, msg=u'tvbox解绑后重新登录')
            self.assertRegexpMatches(str(login_tvbox.json()['userDevice']['type']),'8',msg=u'tvbox解绑后重新登录')
            self.assertNotEqual(login_tvbox_2.json()['userDevice']['id'],id_tvbox,msg=u'tvbox解绑后重新登录')
            self.assertNotEqual(login_tvbox_2.json()['nemoNumber'],nemoNumber_tvbox,msg=u'tvbox解绑后重新登录')
            self.assertEqual(login_tvbox_2.json()['userDevice']['deviceSN'],sn_tvbox,msg=u'tvbox解绑后重新登录')
            self.assertEqual(login_tvbox_2.json()['userDevice']['userProfileID'],userProfileID_tvbox,msg=u'tvbox解绑后重新登录')
            self.assertRegexpMatches(str(login_tvbox_2.json()['userDevice']['nemoNumber']),'^20\d{6}$',msg=u'tvbox解绑后重新登录')
            self.assertEqual(login_tvbox_2.json()['userDevice']['category'],'NP40',msg=u'tvbox解绑后重新登录')

            id_tvbox_2 = login_tvbox_2.json()['userDevice']['id']
            sn_tvbox_2 = login_tvbox_2.json()['userDevice']['deviceSN']
            userProfileID_tvbox_2 = login_tvbox_2.json()['userDevice']['userProfileID']


        except Exception, e:
            error(e)
            error(login_tvbox_2.url)
            error(login_tvbox_2.request.body)
            error(login_tvbox_2.text)
            raise e
        time.sleep(1)
        #解绑tvbox
        info(u'解绑tvbox')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_tvbox_2,"deviceSN":sn_tvbox_2,"userProfileID":userProfileID_tvbox_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑tvbox')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑tvbox')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑tvbox,验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_tvbox_2, "deviceSN": sn_tvbox_2, "userProfileID": userProfileID_tvbox_2}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑tvbox,验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑tvbox,验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)

    def test_me90_login(self):
        deviceinfo = self.me90
        sn = self.getsn(deviceinfo['sn_pre'])
        #添加me90sn
        info(u'添加me90sn')
        url_addsn_bruce = 'http://'+ self.internal_nginx_ip+ conf_addsn_bruce['uri']
        data = {"sn":sn,"name":u"小鱼会议终端ME90"}
        addsn_bruce = requests_normal(conf_addsn_bruce['method'], url_addsn_bruce,data,self.token, verify=False,headers=self.headers_json)
        try:
            #self.assertEqual(addsn_bruce.status_code, 200, msg=u'添加me90sn')  #没有删除sn，这里先不校验
            #self.assertRegexpMatches(addsn_bruce.text,'ok',msg=u'添加me90sn')  #没有删除sn，这里先不校验
            info(addsn_bruce.text)
        except Exception, e:
            error(e)
            error(addsn_bruce.url)
            error(addsn_bruce.request.body)
            error(addsn_bruce.text)
            raise e
        time.sleep(1)
        #me90登录
        info(u'me90登录')
        url_login_me90 = 'http://'+ self.iauth_ip+ conf_login_bruce['uri']
        data = {"sn":sn, "model":deviceinfo['model']}
        login_me90 = requests_normal(conf_login_bruce['method'], url_login_me90,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me90.status_code, 200, msg=u'me90登录')
            self.assertRegexpMatches(str(login_me90.json()['securityKey']),'.+',msg=u'me90登录')
            self.assertRegexpMatches(str(login_me90.json()['number']),'^60\d{6}$',msg=u'me90登录')
            self.assertRegexpMatches(str(login_me90.json()['sn']),sn,msg=u'me90登录')

            id_me90 = login_me90.json()['id']
            sn_me90 = login_me90.json()['sn']
            nemoNumber_me90 = login_me90.json()['number']
        except Exception, e:
            error(e)
            error(login_me90.url)
            error(login_me90.request.body)
            error(login_me90.text)
            raise e
        time.sleep(1)

        #me90重复登录
        info(u'me90重复登录')
        url_login_me90 = 'http://'+ self.iauth_ip+ conf_login_bruce['uri']
        data = {"sn":sn, "model":deviceinfo['model']}
        login_me90 = requests_normal(conf_login_bruce['method'], url_login_me90,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me90.status_code, 200, msg=u'me90重复登录')
            self.assertEqual(login_me90.json()['id'],id_me90,msg=u'me90重复登录')
            self.assertEqual(login_me90.json()['number'],nemoNumber_me90,msg=u'me90重复登录')
            self.assertEqual(login_me90.json()['sn'],sn_me90,msg=u'me90重复登录')

        except Exception, e:
            error(e)
            error(login_me90.url)
            error(login_me90.request.body)
            error(login_me90.text)
            raise e
        time.sleep(1)
        #解绑me90
        info(u'解绑me90')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me90,"deviceSN":sn_me90,"userProfileID":None}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me90')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me90')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #me90解绑后重新登录
        info(u'me90解绑后重新登录')
        url_login_me90 = 'http://'+ self.iauth_ip+ conf_login_bruce['uri']
        data = {"sn":sn, "model":deviceinfo['model']}
        login_me90_2 = requests_normal(conf_login_bruce['method'], url_login_me90,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me90_2.status_code, 200, msg=u'me90解绑后重新登录')
            self.assertEqual(login_me90_2.status_code, 200, msg=u'me90重复登录')
            self.assertNotEqual(login_me90_2.json()['id'],id_me90,msg=u'me90重复登录')
            self.assertEqual(login_me90_2.json()['number'],nemoNumber_me90,msg=u'me90重复登录')
            self.assertEqual(login_me90_2.json()['sn'],sn_me90,msg=u'me90重复登录')

            self.assertRegexpMatches(str(login_me90_2.json()['number']),'^60\d{6}$',msg=u'me90解绑后重新登录')

            id_me90_2 = login_me90_2.json()['id']
            sn_me90_2 = login_me90_2.json()['sn']


        except Exception, e:
            error(e)
            error(login_me90_2.url)
            error(login_me90_2.request.body)
            error(login_me90_2.text)
            raise e
        time.sleep(1)
        #解绑me90
        info(u'解绑me90')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id":id_me90_2,"deviceSN":sn_me90_2,"userProfileID":None}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 200, msg=u'解绑me90')
            self.assertRegexpMatches(UnbindDevice.text,'ok',msg=u'解绑me90')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
        #验证解绑成功
        info(u'解绑me90,验证解绑成功')
        url_UnbindDevice = 'http://'+ self.internal_nginx_ip+ conf_UnbindDevice['uri']
        data = [{"id": id_me90_2, "deviceSN": sn_me90_2, "userProfileID": None}]
        UnbindDevice = requests_normal(conf_UnbindDevice['method'], url_UnbindDevice,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(UnbindDevice.status_code, 400, msg=u'解绑me90,验证解绑成功')
            self.assertRegexpMatches(UnbindDevice.text,'device.not.bind',msg=u'解绑me90,验证解绑成功')
        except Exception, e:
            error(e)
            error(UnbindDevice.url)
            error(UnbindDevice.request.body)
            error(UnbindDevice.text)
            raise e
        time.sleep(1)
  

if __name__ == '__main__':
    info(' start')


    unittest.main()
