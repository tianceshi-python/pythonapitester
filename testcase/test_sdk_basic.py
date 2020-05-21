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
import jsonpath
import re

#接口配置（配置与测试数据分离）。接口配在这里，数据从excel获取。这里配置对应 http://123.57.12.62/meeting/rest-api-create-conf/中的 1-8
conf_sdk_user = {'method': 'GET','uri': '/api/rest/v3/en/sdk/user'}
conf_sdk_login = {'method': 'PUT','uri': '/api/rest/v3/en/sdk/login'}
conf_sdk_conference = {'method': 'POST','uri': '/api/rest/v3/en/sdk/conference'}
conf_sdk_callurl = {'method': 'GET','uri': '/api/rest/v3/en/sdk/callUrlInfo'}
conf_sdk_logout = {'method': 'PUT','uri': '/api/rest/v3/en/sdk/%s/logout'}
conf_sdk_wechatuser = {'method': 'GET','uri': '/api/rest/v3/en/sdk/wechat/user'}
conf_sdk_wechatlogin = {'method': 'PUT','uri': '/api/rest/v3/en/sdk/wechat/login'}
conf_sdk_boxlogin = {'method': 'PUT','uri': '/api/rest/v3/en/sdk/box/login'}
conf_sdk_thirddevicelogin = {'method': 'PUT','uri': '/api/rest/v3/en/sdk/box/third/device/login'}
conf_login_tvbox = {'method': 'PUT','uri': '/api/rest/v3/en/tvbox/login'}







class sdk_basic_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['pivotor_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.phone = json.loads(allconf['enterprise']['sdk_test'])['phone']
        self.pstn = json.loads(allconf['enterprise']['sdk_test'])['pstn']
        self.userconf = json.loads(allconf['enterprise']['sdk_test'])['userconf']
        self.cloudconf = json.loads(allconf['enterprise']['sdk_test'])['cloudconf']
        self.H323 = json.loads(allconf['enterprise']['sdk_test'])['H323']
        self.externalUserId = json.loads(allconf['enterprise']['sdk_test'])['externalUserId']
        self.securityKey_hard = json.loads(allconf['enterprise']['sdk_test'])['securityKey_hard']
        self.start_time = (int(time.time())+60)*1000
        self.extid = allconf['enterprise']['extid']
        self.box = json.loads(allconf['enterprise']['box'])
        self.third = json.loads(allconf['enterprise']['third'])
        self.me40 = json.loads(allconf['sdk_login']['me40'])
        self.me40tmp = json.loads(allconf['enterprise']['me40tmp'])
        self.iauth_ip = allconf['sdk_login']['iauth_ip']
        self.me90tmp = json.loads(allconf['enterprise']['me90tmp'])


    def test_sdk_user(self):
        #创建用户
        info(u'创建用户')
        url_sdk_user = 'http://'+ self.ip+ conf_sdk_user['uri'] + '?extId=' + self.enterpriseId + '&externalUserId=' + self.externalUserId
        sdk_user = requests_normal(conf_sdk_user['method'], url_sdk_user,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_user.status_code, 200, msg=u'创建用户')
            #self.assertRegexpMatches(sdk_user.text,'"autoRecording":false',msg=u'创建用户')
            account = sdk_user.json()['userName']
            password = sdk_user.json()['password']
        except Exception, e:
            error(e)
            error(sdk_user.url)
            error(sdk_user.request.body)
            error(sdk_user.text)
            raise e
        time.sleep(1)
        #登录
        info(u'登录')
        url_sdk_login = 'http://'+ self.ip+ conf_sdk_login['uri']
        data = {
                "account":account,
                "password":password,
                "deviceSn":"12345666",
                "deviceType":5,
                "model":"iphone 10",
                "deviceDisplayName":"test_user"
                }
        sdk_login = requests_normal(conf_sdk_login['method'], url_sdk_login,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_login.status_code, 200, msg=u'登录')
            securityKey = sdk_login.json()['securityKey']
            userProfileid = sdk_login.json()['userProfile']['id']

        except Exception, e:
            error(e)
            error(sdk_login.url)
            error(sdk_login.request.body)
            error(sdk_login.text)
            raise e
        time.sleep(1)
        #sdk_conference
        info(u'conference')
        url_sdk_conference = 'http://'+ self.ip+ conf_sdk_conference['uri'] + '?extId=' + self.enterpriseId
        data = {
                "startTime":self.start_time,
                "duration":"120000",
                "meetingName":"yhuitest",
                "maxParticipantCount":2,
                "requirePassword":False,
                "autoRecord":False,
                "password":"",
                "meetingNumber":"",
                "autoMute":"0",
                "smartMutePerson":5
                }
        sdk_conference = requests_normal(conf_sdk_conference['method'], url_sdk_conference,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_conference.status_code, 200, msg=u'sdk_conference')
            conference = sdk_conference.json()['meetingNumber']

        except Exception, e:
            error(e)
            error(sdk_conference.url)
            error(sdk_conference.request.body)
            error(sdk_conference.text)
            raise e
        #callurlInfo_phone
        info(u'callurlInfo_phone')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.phone + '&securityKey=' + securityKey
        sdk_callurl = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_callurl.status_code, 200, msg=u'callurlInfo_phone')
            self.assertRegexpMatches(sdk_callurl.text,'\d{8}@SOFT',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_callurl.url)
            error(sdk_callurl.request.body)
            error(sdk_callurl.text)
            raise e
        time.sleep(1)
        #callurlInfo_pstn
        info(u'callurlInfo_pstn')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.pstn + '&securityKey=' + securityKey
        sdk_pstn = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_pstn.status_code, 400, msg=u'callurlInfo_phone')
            #self.assertRegexpMatches(sdk_callurl.text,'"autoRecording":false',msg=u'callurlInfo_phone')
            info(sdk_pstn.text)
        except Exception, e:
            error(e)
            error(sdk_pstn.url)
            error(sdk_pstn.request.body)
            error(sdk_pstn.text)
            raise e
        time.sleep(1)
        #callurlInfo_userconf
        info(u'callurlInfo_pstn')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.userconf + '&securityKey=' + securityKey
        sdk_userconf = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_userconf.status_code, 200, msg=u'callurlInfo_phone')
            self.assertRegexpMatches(sdk_userconf.text,self.userconf+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_userconf.url)
            error(sdk_userconf.request.body)
            error(sdk_userconf.text)
            raise e
        time.sleep(1)
        #callurlInfo_cloudconf
        info(u'callurlInfo_cloudconf')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.cloudconf + '&securityKey=' + securityKey
        sdk_cloudconf = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_cloudconf.status_code, 200, msg=u'callurlInfo_cloudconf')
            self.assertRegexpMatches(sdk_cloudconf.text,self.cloudconf+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_cloudconf.url)
            error(sdk_cloudconf.request.body)
            error(sdk_cloudconf.text)
            raise e
        time.sleep(1)
        #callurlInfo_H323
        info(u'callurlInfo_H323')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.H323 + '&securityKey=' + securityKey
        sdk_H323 = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_H323.status_code, 200, msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"deviceType":"H323"',msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"callUrl":".+@H323"', msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"callNumber":".+"', msg=u'sdk_H323')
            #self.assertRegexpMatches(sdk_callurl.text,'"autoRecording":false',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_H323.url)
            error(sdk_H323.request.body)
            error(sdk_H323.text)
            raise e
        time.sleep(1)
        #sdk_conference
        info(u'sdk_conference')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + conference + '&securityKey=' + securityKey
        sdk_conference = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_conference.status_code, 200, msg=u'sdk_conference')
            self.assertRegexpMatches(sdk_conference.text,conference+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_conference.url)
            error(sdk_conference.request.body)
            error(sdk_conference.text)
            raise e
        time.sleep(1)
        #登出
        info(u'登出')
        url_sdk_logout = ('http://'+ self.ip+ conf_sdk_logout['uri'] + '?securityKey=' + securityKey) % userProfileid
        data = {
                "account":account,
                "password":password,
                "deviceSn":"12345666",
                "deviceType":5,
                "model":"iphone 10",
                "deviceDisplayName":"test_user"
                }
        sdk_logout= requests_normal(conf_sdk_logout['method'], url_sdk_logout,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_logout.status_code, 204, msg=u'登出')

        except Exception, e:
            error(e)
            error(sdk_logout.url)
            error(sdk_logout.request.body)
            error(sdk_logout.text)
            raise e
        time.sleep(1)

    def test_sdk_hard(self):
        deviceinfo = self.me40

        sn = self.me40tmp['SN']

        #me40登录
        info(u'me40登录')
        url_login_tvbox = 'http://'+ self.iauth_ip+ conf_login_tvbox['uri']
        data = {"deviceSN":sn,"packageName":deviceinfo['packageName'], "deviceModel":deviceinfo['deviceModel'], "category":deviceinfo['category']}

        login_me40 = requests_normal(conf_login_tvbox['method'], url_login_tvbox,data,self.token,verify=False,headers=self.headers_json)
        try:
            self.assertEqual(login_me40.status_code, 200, msg=u'me40登录')
            securityKey = login_me40.json()['userDevice']['securityKey']
            info(securityKey)
        except Exception, e:
            error(e)
            error(login_me40.url)
            error(login_me40.request.body)
            error(login_me40.text)
            raise e
        time.sleep(1)

        #securityKey = self.securityKey_hard
        #sdk_conference
        info(u'conference')
        url_sdk_conference = 'http://'+ self.ip+ conf_sdk_conference['uri'] + '?extId=' + self.enterpriseId
        data = {
                "startTime":self.start_time,
                "duration":"120000",
                "meetingName":"yhuitest",
                "maxParticipantCount":2,
                "requirePassword":False,
                "autoRecord":False,
                "password":"",
                "meetingNumber":"",
                "autoMute":"0",
                "smartMutePerson":5
                }
        sdk_conference = requests_normal(conf_sdk_conference['method'], url_sdk_conference,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_conference.status_code, 200, msg=u'sdk_conference')
            conference = sdk_conference.json()['meetingNumber']

        except Exception, e:
            error(e)
            error(sdk_conference.url)
            error(sdk_conference.request.body)
            error(sdk_conference.text)
            raise e
        time.sleep(1)
        #callurlInfo_phone
        info(u'callurlInfo_phone')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.phone + '&securityKey=' + securityKey
        sdk_callurl = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_callurl.status_code, 200, msg=u'callurlInfo_phone')
            self.assertRegexpMatches(sdk_callurl.text,'\d{8}@SOFT',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_callurl.url)
            error(sdk_callurl.request.body)
            error(sdk_callurl.text)
            raise e
        time.sleep(1)
        #callurlInfo_pstn
        info(u'callurlInfo_pstn')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.pstn + '&securityKey=' + securityKey
        sdk_pstn = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_pstn.status_code, 200, msg=u'callurlInfo_pstn')
            self.assertRegexpMatches(sdk_pstn.text,'"numberType":"PSTN"',msg=u'callurlInfo_pstn')
            self.assertRegexpMatches(sdk_pstn.text,'"deviceType":"TEL"',msg=u'callurlInfo_pstn')
            self.assertRegexpMatches(sdk_pstn.text,'"callUrl":".+@TEL"',msg=u'callurlInfo_pstn')

            #self.assertRegexpMatches(sdk_callurl.text,'"autoRecording":false',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_pstn.url)
            error(sdk_pstn.request.body)
            error(sdk_pstn.text)
            raise e
        time.sleep(1)
        #callurlInfo_userconf
        info(u'callurlInfo_pstn')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.userconf + '&securityKey=' + securityKey
        sdk_userconf = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_userconf.status_code, 200, msg=u'callurlInfo_phone')
            self.assertRegexpMatches(sdk_userconf.text,self.userconf+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_userconf.url)
            error(sdk_userconf.request.body)
            error(sdk_userconf.text)
            raise e
        time.sleep(1)
        #callurlInfo_cloudconf
        info(u'callurlInfo_cloudconf')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.cloudconf + '&securityKey=' + securityKey
        sdk_cloudconf = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_cloudconf.status_code, 200, msg=u'callurlInfo_cloudconf')
            self.assertRegexpMatches(sdk_cloudconf.text,self.cloudconf+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_cloudconf.url)
            error(sdk_cloudconf.request.body)
            error(sdk_cloudconf.text)
            raise e
        time.sleep(1)
        #sdk_conference
        info(u'sdk_conference')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + conference + '&securityKey=' + securityKey
        sdk_conference = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_conference.status_code, 200, msg=u'sdk_conference')
            self.assertRegexpMatches(sdk_conference.text,conference+'@CONFNO',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_conference.url)
            error(sdk_conference.request.body)
            error(sdk_conference.text)
            raise e
        time.sleep(1)
        #callurlInfo_H323
        info(u'callurlInfo_H323')
        url_sdk_callurl = 'http://'+ self.ip+ conf_sdk_callurl['uri'] + '?number=' + self.H323 + '&securityKey=' + securityKey
        sdk_H323 = requests_normal(conf_sdk_callurl['method'], url_sdk_callurl,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_H323.status_code, 200, msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"deviceType":"H323"',msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"callUrl":".+@H323"', msg=u'sdk_H323')
            self.assertRegexpMatches(sdk_H323.text, '"callNumber":".+"', msg=u'sdk_H323')

            #self.assertRegexpMatches(sdk_callurl.text,'"autoRecording":false',msg=u'callurlInfo_phone')
        except Exception, e:
            error(e)
            error(sdk_H323.url)
            error(sdk_H323.request.body)
            error(sdk_H323.text)
            raise e
        time.sleep(1)

    def test_wechart(self):
        #创建用户
        info(u'wechart创建用户')
        url_sdk_wechatuser = 'http://'+ self.ip+ conf_sdk_wechatuser['uri'] + '?enterpriseId=' + self.extid + '&wechatEnId=aab&wechatUserId=bbb&displayName=test1'
        sdk_wechatuser = requests_normal(conf_sdk_wechatuser['method'], url_sdk_wechatuser,'',self.token, verify=False)
        try:
            self.assertEqual(sdk_wechatuser.status_code, 200, msg=u'wechart创建用户')
            account = sdk_wechatuser.json()['userName']
            password = sdk_wechatuser.json()['password']
        except Exception, e:
            error(e)
            error(sdk_wechatuser.url)
            error(sdk_wechatuser.request.body)
            error(sdk_wechatuser.text)
            raise e
        time.sleep(1)
        #登录
        info(u'wechart登录')
        url_wechatlogin = 'http://'+ self.ip+ conf_sdk_wechatlogin['uri']
        data = {
                "account":account,
                "password":password,
                "deviceSn":"12345666",
                "deviceType":5,
                "model":"iphone 10",
                "deviceDisplayName":"test_wechart"
                }
        wechatlogin = requests_normal(conf_sdk_wechatlogin['method'], url_wechatlogin,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(wechatlogin.status_code, 200, msg=u'wechart登录')
            self.assertRegexpMatches(wechatlogin.text,'"securityKey":".+"',msg=u'wechart登录')



        except Exception, e:
            error(e)
            error(wechatlogin.url)
            error(wechatlogin.request.body)
            error(wechatlogin.text)
            raise e
        time.sleep(1)

    def test_sdk_box(self):
        #登录
        info(u'box登录')
        url_sdk_boxlogin = 'http://'+ self.ip+ conf_sdk_boxlogin['uri'] + '?extId=' + self.enterpriseId
        data = self.box
        sdk_boxlogin = requests_normal(conf_sdk_boxlogin['method'], url_sdk_boxlogin,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_boxlogin.status_code, 200, msg=u'box登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['type']),'8',msg=u'box登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['securityKey']),'.+',msg=u'box登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['nemoNumber']),'^\d{8}$',msg=u'box登录')
            numb_box = sdk_boxlogin.json()['userDevice']['nemoNumber']
            sk_box = sdk_boxlogin.json()['userDevice']['securityKey']
        except Exception, e:
            error(e)
            error(sdk_boxlogin.url)
            error(sdk_boxlogin.request.body)
            error(sdk_boxlogin.text)
            raise e
        time.sleep(1)
        #重复登录
        info(u'box重复登录')
        url_sdk_boxlogin = 'http://'+ self.ip+ conf_sdk_boxlogin['uri'] + '?extId=' + self.enterpriseId
        data = self.box
        sdk_boxlogin = requests_normal(conf_sdk_boxlogin['method'], url_sdk_boxlogin,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sdk_boxlogin.status_code, 200, msg=u'box重复登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['type']),'8',msg=u'box重复登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['securityKey']),'.+',msg=u'box重复登录')
            self.assertRegexpMatches(str(sdk_boxlogin.json()['userDevice']['nemoNumber']),'^\d{8}$',msg=u'box重复登录')
            self.assertNotEqual(sdk_boxlogin.json()['userDevice']['securityKey'],sk_box,msg=u'box重复登录')
            self.assertEqual(sdk_boxlogin.json()['userDevice']['nemoNumber'],numb_box,msg=u'box重复登录')
        except Exception, e:
            error(e)
            error(sdk_boxlogin.url)
            error(sdk_boxlogin.request.body)
            error(sdk_boxlogin.text)
            raise e
        time.sleep(1)
        #登录
        info(u'第三方硬件登录')
        url_thirddevicelogin = 'http://'+ self.ip+ conf_sdk_thirddevicelogin['uri'] + '?extId=' + self.enterpriseId
        data = self.third
        thirddevicelogin = requests_normal(conf_sdk_thirddevicelogin['method'], url_thirddevicelogin,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(thirddevicelogin.status_code, 200, msg=u'第三方硬件登录')
            self.assertRegexpMatches(str(thirddevicelogin.json()['securityKey']),'.+',msg=u'第三方硬件登录')
            self.assertRegexpMatches(str(thirddevicelogin.json()['number']),'^\d{8}$',msg=u'第三方硬件登录')
            numb_third = thirddevicelogin.json()['number']
            sk_third = thirddevicelogin.json()['securityKey']

        except Exception, e:
            error(e)
            error(thirddevicelogin.url)
            error(thirddevicelogin.request.body)
            error(thirddevicelogin.text)
            raise e
        time.sleep(1)
        #登录
        info(u'第三方硬件重复登录')
        url_thirddevicelogin = 'http://'+ self.ip+ conf_sdk_thirddevicelogin['uri'] + '?extId=' + self.enterpriseId
        data = self.third
        thirddevicelogin = requests_normal(conf_sdk_thirddevicelogin['method'], url_thirddevicelogin,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(thirddevicelogin.status_code, 200, msg=u'第三方硬件重复登录')
            self.assertRegexpMatches(str(thirddevicelogin.json()['securityKey']),'.+',msg=u'第三方硬件重复登录')
            self.assertRegexpMatches(str(thirddevicelogin.json()['number']),'^\d{8}$',msg=u'第三方硬件重复登录')
            self.assertNotEqual(thirddevicelogin.json()['securityKey'],sk_third,msg=u'第三方硬件重复登录')
            self.assertEqual(thirddevicelogin.json()['number'],numb_third,msg=u'第三方硬件重复登录')

        except Exception, e:
            error(e)
            error(thirddevicelogin.url)
            error(thirddevicelogin.request.body)
            error(thirddevicelogin.text)
            raise e
        time.sleep(1)





if __name__ == '__main__':
    info(' start')


    unittest.main()
