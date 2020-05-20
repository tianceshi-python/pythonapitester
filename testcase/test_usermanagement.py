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
conf_user_batch = {'method': 'POST','uri': '/api/rest/external/v1/buffet/batch/users'}
conf_user_add = {'method': 'POST','uri': '/api/rest/external/v1/buffet/user'}
conf_user_modify = {'method': 'PUT','uri': '/api/rest/external/v1/buffet/user'}
conf_user_del = {'method': 'DELETE','uri': '/api/rest/external/v1/buffet/user'}
conf_user_que = {'method': 'GET','uri': '/api/rest/external/v1/buffet/user'}
conf_user_all_nemos = {'method': 'GET','uri': '/api/rest/external/v1/buffet/nemos'}
conf_user_que_nemos = {'method': 'GET','uri': '/api/rest/external/v1/buffet/nemos/page'}
conf_user_que_nemo = {'method': 'GET','uri': '/api/rest/external/v1/deviceInfo/%s'}
conf_user_deviceInfo = {'method': 'GET','uri': '/api/rest/external/v1/deviceInfo'}
conf_user_deviceInfo_sn = {'method': 'PUT','uri': '/api/rest/external/v1/deviceInfo'}
conf_change_nemo = {'method': 'PUT','uri': '/api/rest/external/v1/buffet/nemos'}
conf_del_nemo = {'method': 'DELETE','uri': '/api/rest/external/v1/buffet/nemos'}
conf_add_nemo = {'method': 'POST','uri': '/api/rest/external/v1/buffet/nemos'}
conf_cat_log = {'method': 'PUT','uri': '/api/rest/external/v1/portal/cat/log'}
conf_cat_fulllog = {'method': 'PUT','uri': '/api/rest/external/v1/portal/cat/fulllog'}
conf_reboot_nemo = {'method': 'PUT','uri': '/api/rest/external/v1/portal/reboot'}
conf_upgrade_nemo = {'method': 'PUT','uri': '/api/rest/external/v1/portal/upgrade'}
conf_add_mailuser = {'method': 'POST','uri': '/api/rest/external/v1/buffet/mail/user'}
conf_del_mailuser = {'method': 'DELETE','uri': '/api/rest/external/v1/buffet/mail/user'}

class user_management(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.userphone = json.loads(allconf['enterprise']['user_tmpadd'])['phone']
        self.username = json.loads(allconf['enterprise']['user_tmpadd'])['name']
        self.usercountryCode = json.loads(allconf['enterprise']['user_tmpadd'])['countryCode']
        self.userpassword = json.loads(allconf['enterprise']['user_tmpadd'])['password']
        self.mailuserinactivate = json.loads(allconf['enterprise']['mailuser_tmpadd'])['inactivate']
        self.mailuseractivate = json.loads(allconf['enterprise']['mailuser_tmpadd'])['activate']
        self.NE60number = json.loads(allconf['enterprise']['ne60'])['number']
        self.NE60number_SN = json.loads(allconf['enterprise']['ne60'])['SN']
        self.ME40number = json.loads(allconf['enterprise']['me40'])['number']
        self.ME40number_SN = json.loads(allconf['enterprise']['me40'])['SN']
        self.ME40tmpnumber = json.loads(allconf['enterprise']['me40tmp'])['number']
        self.ME40tmpnumber_SN = json.loads(allconf['enterprise']['me40tmp'])['SN']
        self.ME90tmpnumber = json.loads(allconf['enterprise']['me90tmp'])['number']
        self.ME90tmpnumber_SN = json.loads(allconf['enterprise']['me90tmp'])['SN']
        

    def test_sdk_user(self):
        #批量重建通讯录
        info(u'批量重建通讯录')
        url_user_batch = 'https://'+ self.ip+ conf_user_batch['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [{"userId":"ff80808158f7d9ca015919e7f72c2b47","countryCode":"+86","phone":"12345678900","mailbox":None,"name":u"假手机号"},{"userId":"ff808081620159490162f5ed6fc5081c","countryCode":"+86","phone":"17791269352","mailbox":"","name":u"赵川"},{"userId":"ff80808165675a680165f1e8398671a3","countryCode":"+86","phone":"12345678899","mailbox":None,"name":"aa"},{"userId":"00000000680c534c01685b534a24005c","countryCode":"+86","phone":"10091702593","mailbox":None,"name":"guest"},{"userId":"00000000680c534c01685c26484600cd","countryCode":"+86","phone":"10069288499","mailbox":None,"name":"test1"}]
        user_batch = requests_sig(conf_user_batch['method'], url_user_batch,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(user_batch.status_code, 200, msg=u'批量重建通讯录')
            self.assertEqual(len(user_batch.json()), 5, msg=u'批量重建通讯录')
        except Exception, e:
            error(e)
            error(user_batch.url)
            error(user_batch.request.body)
            error(user_batch.text)
            raise e
        time.sleep(1)
        #添加企业通讯录用户
        info(u'添加企业通讯录用户')
        url_user_add = 'https://'+ self.ip+ conf_user_add['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {
                "userId":"123456",
                "name":self.username,
                "countryCode":self.usercountryCode,
                "phone":self.userphone,
                "telephone":"010-451283",
                "mailbox":"user1@123.com",
                "avatar":"http://pic14.nipic.com/20110522/7411759_164157418126_2.jpg",
                "dept": "tester",
                "password": self.userpassword
                }
        user_add = requests_sig(conf_user_add['method'], url_user_add,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(user_add.status_code, 200, msg=u'添加企业通讯录用户')
            self.assertEqual(user_add.json()['phone'],self.usercountryCode+'-'+self.userphone,msg=u'添加企业通讯录用户')
            self.assertEqual(user_add.json()['name'],self.username,msg=u'添加企业通讯录用户')

            info(user_add.text)
        except Exception, e:
            error(e)
            error(user_add.url)
            error(user_add.request.body)
            error(user_add.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,self.userphone,msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,self.username,msg=u'查询企业通讯录用户')

        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)
        #重复添加企业通讯录用户
        info(u'重复添加企业通讯录用户')
        url_user_add = 'https://' + self.ip + conf_user_add['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {
                "userId":"123456",
                "name":u'重复添加',
                "countryCode":self.usercountryCode,
                "phone":self.userphone,
                "telephone":"029-451283",
                "mailbox":"user1@456.com",
                "avatar":"http://pic14.nipic.com/20110522/7411759_164157418126_2.jpg",
                "dept": "tester1",
                "password": '654321'
                }
        user_add = requests_sig(conf_user_add['method'], url_user_add, data, self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(user_add.status_code, 200, msg=u'重复添加企业通讯录用户')
            self.assertRegexpMatches(user_add.text,u'"name":"重复添加"',msg=u'重复添加企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_add.url)
            error(user_add.request.body)
            error(user_add.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,self.userphone,msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,u"重复添加",msg=u'查询企业通讯录用户')
            info(user_que.text)
        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)
        #修改企业通讯录用户
        info(u'修改企业通讯录用户')
        url_user_modify = 'https://' + self.ip + conf_user_modify['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {
                "userId":"123456",
                "name":u'修改名称',
                "countryCode":self.usercountryCode,
                "phone":self.userphone,
                "telephone":"010-451283",
                "mailbox":"user1@123.com",
                "avatar":"http://pic14.nipic.com/20110522/7411759_164157418126_2.jpg",
                "dept": "tester",
                "password": '123456'
                }
        user_modify = requests_sig(conf_user_modify['method'], url_user_modify, data, self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(user_modify.status_code, 204, msg=u'修改企业通讯录用户')
            # self.assertRegexpMatches(sdk_user.text,'"autoRecording":false',msg=u'创建用户')
        except Exception, e:
            error(e)
            error(user_modify.url)
            error(user_modify.request.body)
            error(user_modify.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,self.userphone,msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,u"修改名称",msg=u'查询企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)
        #删除企业通讯录用户
        info(u'删除企业通讯录用户')
        url_user_del = 'https://'+ self.ip+ conf_user_del['uri'] + '?enterpriseId=' + self.enterpriseId + '&countryCode=' + self.usercountryCode + '&phone=' + self.userphone
        user_del = requests_sig(conf_user_del['method'], url_user_del,'',self.token, verify=False)
        try:
            self.assertEqual(user_del.status_code, 204, msg=u'删除企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_del.url)
            error(user_del.request.body)
            error(user_del.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,self.userphone,msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,"修改名称",msg=u'查询企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)

    def test_mailuser(self):
        #添加激活邮箱用户
        info(u'添加激活邮箱用户')
        url_mailuser_add = 'https://'+ self.ip+ conf_add_mailuser['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {
                "name":'mailuser3',
                "mailbox":self.mailuseractivate
                }
        mailuser_add = requests_sig(conf_add_mailuser['method'], url_mailuser_add,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(mailuser_add.status_code, 200, msg=u'添加激活邮箱用户')
            self.assertEqual(mailuser_add.json()['mailbox'],self.mailuseractivate,msg=u'添加激活邮箱用户')
            self.assertEqual(mailuser_add.json()['name'],'mailuser3',msg=u'添加激活邮箱用户')
            info(mailuser_add.text)
        except Exception, e:
            error(e)
            error(mailuser_add.url)
            error(mailuser_add.request.body)
            error(mailuser_add.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,self.mailuseractivate,msg=u'查询企业通讯录用户')
            self.assertRegexpMatches(user_que.text,'mailuser3',msg=u'查询企业通讯录用户')

        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)
        #删除激活邮箱用户
        info(u'删除激活邮箱用户')
        url_del_mailuser = 'https://'+ self.ip+ conf_del_mailuser['uri'] + '?enterpriseId=' + self.enterpriseId + '&email='+ self.mailuseractivate
        del_mailuser = requests_sig(conf_del_mailuser['method'], url_del_mailuser,'',self.token, verify=False)
        try:
            self.assertEqual(del_mailuser.status_code, 204, msg=u'删除激活邮箱用户')
        except Exception, e:
            error(e)
            error(del_mailuser.url)
            error(del_mailuser.request.body)
            error(del_mailuser.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://' + self.ip + conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que, '', self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,self.mailuseractivate,msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,'mailuser3',msg=u'查询企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)

        #添加未激活邮箱用户
        info(u'添加未激活邮箱用户')
        url_mailuser_add = 'https://'+ self.ip+ conf_add_mailuser['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {
                "name":'mailuser4',
                "mailbox":self.mailuserinactivate
                }
        mailuser_add = requests_sig(conf_add_mailuser['method'], url_mailuser_add,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(mailuser_add.status_code, 200, msg=u'添加未激活邮箱用户')
            self.assertEqual(mailuser_add.json()['mailbox'],self.mailuserinactivate,msg=u'添加未激活邮箱用户')
            self.assertEqual(mailuser_add.json()['name'],'mailuser4',msg=u'添加未激活邮箱用户')
            info(mailuser_add.text)
        except Exception, e:
            error(e)
            error(mailuser_add.url)
            error(mailuser_add.request.body)
            error(mailuser_add.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://'+ self.ip+ conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que,'',self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,self.mailuserinactivate,msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,'mailuser4',msg=u'查询企业通讯录用户')

        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)
        #删除激活邮箱用户
        info(u'删除激活邮箱用户')
        url_del_mailuser = 'https://'+ self.ip+ conf_del_mailuser['uri'] + '?enterpriseId=' + self.enterpriseId + '&email='+ self.mailuserinactivate
        del_mailuser = requests_sig(conf_del_mailuser['method'], url_del_mailuser,'',self.token, verify=False)
        try:
            self.assertEqual(del_mailuser.status_code, 204, msg=u'删除激活邮箱用户')
        except Exception, e:
            error(e)
            error(del_mailuser.url)
            error(del_mailuser.request.body)
            error(del_mailuser.text)
            raise e
        time.sleep(1)
        #查询企业通讯录用户
        info(u'查询企业通讯录用户')
        url_user_que = 'https://' + self.ip + conf_user_que['uri'] + '?enterpriseId=' + self.enterpriseId
        user_que = requests_sig(conf_user_que['method'], url_user_que, '', self.token, verify=False)
        try:
            self.assertEqual(user_que.status_code, 200, msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,self.mailuserinactivate,msg=u'查询企业通讯录用户')
            self.assertNotRegexpMatches(user_que.text,'mailuser4',msg=u'查询企业通讯录用户')
        except Exception, e:
            error(e)
            error(user_que.url)
            error(user_que.request.body)
            error(user_que.text)
            raise e
        time.sleep(1)


    def test_nemos_ne60(self):
        #获取企业通讯录小鱼
        info(u'NE60')

        number = self.NE60number
        sn = self.NE60number_SN
        info(u'获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'获取企业通讯录小鱼')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #分页获取企业通讯录小鱼
        info(u'分页获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_que_nemos['uri'] + '?enterpriseId=' + self.enterpriseId + '&page=1&pageSize=10'
        all_nemos = requests_sig(conf_user_que_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,'"currentPage":1,"pageSize":10',msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'分页获取企业通讯录小鱼')


        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 200, msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,number,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,sn,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,'"callState":"idle"',msg=u'获取某个小鱼终端状态')


        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #获取所有小鱼终端状态
        info(u'获取所有小鱼终端状态')
        url_deviceInfo = 'https://'+ self.ip+ conf_user_deviceInfo['uri'] + '?enterpriseId=' + self.enterpriseId
        deviceInfo = requests_sig(conf_user_deviceInfo['method'], url_deviceInfo,'',self.token, verify=False)
        try:
            self.assertEqual(deviceInfo.status_code, 200, msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,number,msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,sn,msg=u'获取所有小鱼终端状态')

        except Exception, e:
            error(e)
            error(deviceInfo.url)
            error(deviceInfo.request.body)
            error(deviceInfo.text)
            raise e
        time.sleep(1)
        #根据sn获取小鱼信息
        info(u'根据sn获取小鱼信息')
        url_deviceInfo_sn = 'https://'+ self.ip+ conf_user_deviceInfo_sn['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [sn]
        deviceInfo_sn = requests_sig(conf_user_deviceInfo_sn['method'], url_deviceInfo_sn,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(deviceInfo_sn.status_code, 200, msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,number,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,sn,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,'"callState":"idle"',msg=u'根据sn获取小鱼信息')

            info(deviceInfo_sn.text)

        except Exception, e:
            error(e)
            error(deviceInfo_sn.url)
            error(deviceInfo_sn.request.body)
            error(deviceInfo_sn.text)
            raise e
        time.sleep(1)

        #修改小鱼终端
        info(u'修改小鱼终端')
        url_change_nemo = 'https://'+ self.ip+ conf_change_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number +'&displayName=changename_nemo'
        print url_change_nemo
        change_nemo = requests_sig(conf_change_nemo['method'], url_change_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(change_nemo.status_code, 200, msg=u'修改小鱼终端')

            #self.assertEqual(change_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(change_nemo.url)
            error(change_nemo.request.body)
            error(change_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证修改')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证修改')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+'","name":"changename_nemo"',msg=u'获取企业通讯录小鱼,验证修改')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #删除小鱼终端
        info(u'删除小鱼终端')
        url_del_nemo = 'https://'+ self.ip+ conf_del_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number
        del_nemo = requests_sig(conf_del_nemo['method'], url_del_nemo,'',self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(del_nemo.status_code, 200, msg=u'删除小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(del_nemo.url)
            error(del_nemo.request.body)
            error(del_nemo.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态验证删除')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 400, msg=u'获取某个小鱼终端状态验证删除')
            #self.assertEqual(que_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证修改')
        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #添加小鱼终端
        info(u'添加小鱼终端')
        url_add_nemo = 'https://'+ self.ip+ conf_add_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [{"displayName":u"NE60_西安","nemoNumber":number}]
        add_nemo = requests_sig(conf_add_nemo['method'], url_add_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(add_nemo.status_code, 200, msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"failedDevices":null,',msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"deviceSN":"'+sn+'"',msg=u'添加小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(add_nemo.url)
            error(add_nemo.request.body)
            error(add_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证添加')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证添加')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+u'","name":"NE60_西安"',msg=u'获取企业通讯录小鱼,验证添加')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量升级设备
        info(u'根据小鱼号批量升级设备')
        url_upgrade_nemo = 'https://'+ self.ip+ conf_upgrade_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number,self.ME40tmpnumber]
        upgrade_nemo = requests_sig(conf_upgrade_nemo['method'], url_upgrade_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(upgrade_nemo.status_code, 200, msg=u'根据小鱼号批量升级设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(upgrade_nemo.url)
            error(upgrade_nemo.request.body)
            error(upgrade_nemo.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量重启设备
        info(u'根据小鱼号批量重启设备')
        url_reboot_nemo = 'https://'+ self.ip+ conf_reboot_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number,self.ME40tmpnumber]
        reboot_nemo = requests_sig(conf_reboot_nemo['method'], url_reboot_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(reboot_nemo.status_code, 200, msg=u'根据小鱼号批量重启设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(reboot_nemo.url)
            error(reboot_nemo.request.body)
            error(reboot_nemo.text)
            raise e
        time.sleep(20)
        #根据小鱼号批量上传日志
        info(u'根据小鱼号批量上传日志')
        url_cat_log = 'https://'+ self.ip+ conf_cat_log['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number,self.ME40tmpnumber]
        cat_log = requests_sig(conf_cat_log['method'], url_cat_log,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_log.status_code, 200, msg=u'根据小鱼号批量上传日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_log.url)
            error(cat_log.request.body)
            error(cat_log.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量上传全量日志
        info(u'根据小鱼号批量上传全量日志')
        url_cat_fulllog = 'https://'+ self.ip+ conf_cat_fulllog['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number,self.ME40tmpnumber]
        cat_fulllog = requests_sig(conf_cat_fulllog['method'], url_cat_fulllog,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_fulllog.status_code, 200, msg=u'根据小鱼号批量上传全量日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_fulllog.url)
            error(cat_fulllog.request.body)
            error(cat_fulllog.text)
            raise e
        time.sleep(1)


    def test_nemos_me40(self):
        info(u'ME40')

        #获取企业通讯录小鱼
        number = self.ME40tmpnumber
        sn = self.ME40tmpnumber_SN
        info(u'获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'获取企业通讯录小鱼')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #分页获取企业通讯录小鱼
        info(u'分页获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_que_nemos['uri'] + '?enterpriseId=' + self.enterpriseId + '&page=1&pageSize=10'
        all_nemos = requests_sig(conf_user_que_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,'"currentPage":1,"pageSize":10',msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'分页获取企业通讯录小鱼')


        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 200, msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,number,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,sn,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,'"callState":"offline"',msg=u'获取某个小鱼终端状态')


        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #获取所有小鱼终端状态
        info(u'获取所有小鱼终端状态')
        url_deviceInfo = 'https://'+ self.ip+ conf_user_deviceInfo['uri'] + '?enterpriseId=' + self.enterpriseId
        deviceInfo = requests_sig(conf_user_deviceInfo['method'], url_deviceInfo,'',self.token, verify=False)
        try:
            self.assertEqual(deviceInfo.status_code, 200, msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,number,msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,sn,msg=u'获取所有小鱼终端状态')

        except Exception, e:
            error(e)
            error(deviceInfo.url)
            error(deviceInfo.request.body)
            error(deviceInfo.text)
            raise e
        time.sleep(1)
        #根据sn获取小鱼信息
        info(u'根据sn获取小鱼信息')
        url_deviceInfo_sn = 'https://'+ self.ip+ conf_user_deviceInfo_sn['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [sn]
        deviceInfo_sn = requests_sig(conf_user_deviceInfo_sn['method'], url_deviceInfo_sn,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(deviceInfo_sn.status_code, 200, msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,number,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,sn,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,'"callState":"offline"',msg=u'根据sn获取小鱼信息')

            info(deviceInfo_sn.text)

        except Exception, e:
            error(e)
            error(deviceInfo_sn.url)
            error(deviceInfo_sn.request.body)
            error(deviceInfo_sn.text)
            raise e
        time.sleep(1)

        #修改小鱼终端
        info(u'修改小鱼终端')
        url_change_nemo = 'https://'+ self.ip+ conf_change_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number +'&displayName=changename_nemo_me40'
        print url_change_nemo
        change_nemo = requests_sig(conf_change_nemo['method'], url_change_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(change_nemo.status_code, 200, msg=u'修改小鱼终端')

            #self.assertEqual(change_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(change_nemo.url)
            error(change_nemo.request.body)
            error(change_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证修改')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证修改')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+'","name":"changename_nemo_me40"',msg=u'获取企业通讯录小鱼,验证修改')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #删除小鱼终端
        info(u'删除小鱼终端')
        url_del_nemo = 'https://'+ self.ip+ conf_del_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number
        del_nemo = requests_sig(conf_del_nemo['method'], url_del_nemo,'',self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(del_nemo.status_code, 200, msg=u'删除小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(del_nemo.url)
            error(del_nemo.request.body)
            error(del_nemo.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态验证删除')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 400, msg=u'获取某个小鱼终端状态验证删除')
            #self.assertEqual(que_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证修改')
        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #添加小鱼终端
        info(u'添加小鱼终端')
        url_add_nemo = 'https://'+ self.ip+ conf_add_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [{"displayName":u"ME40_西安","nemoNumber":number}]
        add_nemo = requests_sig(conf_add_nemo['method'], url_add_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(add_nemo.status_code, 200, msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"failedDevices":null,',msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"deviceSN":"'+sn+'"',msg=u'添加小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(add_nemo.url)
            error(add_nemo.request.body)
            error(add_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证添加')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证添加')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+u'","name":"ME40_西安"',msg=u'获取企业通讯录小鱼,验证添加')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量升级设备
        info(u'根据小鱼号批量升级设备')
        url_upgrade_nemo = 'https://'+ self.ip+ conf_upgrade_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        upgrade_nemo = requests_sig(conf_upgrade_nemo['method'], url_upgrade_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(upgrade_nemo.status_code, 200, msg=u'根据小鱼号批量升级设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(upgrade_nemo.url)
            error(upgrade_nemo.request.body)
            error(upgrade_nemo.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量重启设备
        info(u'根据小鱼号批量重启设备')
        url_reboot_nemo = 'https://'+ self.ip+ conf_reboot_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        reboot_nemo = requests_sig(conf_reboot_nemo['method'], url_reboot_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(reboot_nemo.status_code, 200, msg=u'根据小鱼号批量重启设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(reboot_nemo.url)
            error(reboot_nemo.request.body)
            error(reboot_nemo.text)
            raise e
        time.sleep(10)
        #根据小鱼号批量上传日志
        info(u'根据小鱼号批量上传日志')
        url_cat_log = 'https://'+ self.ip+ conf_cat_log['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        cat_log = requests_sig(conf_cat_log['method'], url_cat_log,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_log.status_code, 200, msg=u'根据小鱼号批量上传日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_log.url)
            error(cat_log.request.body)
            error(cat_log.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量上传全量日志
        info(u'根据小鱼号批量上传全量日志')
        url_cat_fulllog = 'https://'+ self.ip+ conf_cat_fulllog['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        cat_fulllog = requests_sig(conf_cat_fulllog['method'], url_cat_fulllog,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_fulllog.status_code, 200, msg=u'根据小鱼号批量上传全量日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_fulllog.url)
            error(cat_fulllog.request.body)
            error(cat_fulllog.text)
            raise e
        time.sleep(1)


    def test_nemos_me90(self):
        #获取企业通讯录小鱼
        info(u'ME90')
        number = self.ME90tmpnumber
        sn = self.ME90tmpnumber_SN
        info(u'获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'获取企业通讯录小鱼')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #分页获取企业通讯录小鱼
        info(u'分页获取企业通讯录小鱼')
        url_all_nemos = 'https://'+ self.ip+ conf_user_que_nemos['uri'] + '?enterpriseId=' + self.enterpriseId + '&page=1&pageSize=10'
        all_nemos = requests_sig(conf_user_que_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,'"currentPage":1,"pageSize":10',msg=u'分页获取企业通讯录小鱼')
            self.assertRegexpMatches(all_nemos.text,number,msg=u'分页获取企业通讯录小鱼')


        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 200, msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,number,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,sn,msg=u'获取某个小鱼终端状态')
            self.assertRegexpMatches(que_nemo.text,'"callState":"offline"',msg=u'获取某个小鱼终端状态')


        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #获取所有小鱼终端状态
        info(u'获取所有小鱼终端状态')
        url_deviceInfo = 'https://'+ self.ip+ conf_user_deviceInfo['uri'] + '?enterpriseId=' + self.enterpriseId
        deviceInfo = requests_sig(conf_user_deviceInfo['method'], url_deviceInfo,'',self.token, verify=False)
        try:
            self.assertEqual(deviceInfo.status_code, 200, msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,number,msg=u'获取所有小鱼终端状态')
            self.assertRegexpMatches(deviceInfo.text,sn,msg=u'获取所有小鱼终端状态')

        except Exception, e:
            error(e)
            error(deviceInfo.url)
            error(deviceInfo.request.body)
            error(deviceInfo.text)
            raise e
        time.sleep(1)
        #根据sn获取小鱼信息
        info(u'根据sn获取小鱼信息')
        url_deviceInfo_sn = 'https://'+ self.ip+ conf_user_deviceInfo_sn['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [sn]
        deviceInfo_sn = requests_sig(conf_user_deviceInfo_sn['method'], url_deviceInfo_sn,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(deviceInfo_sn.status_code, 200, msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,number,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,sn,msg=u'根据sn获取小鱼信息')
            self.assertRegexpMatches(deviceInfo_sn.text,'"callState":"offline"',msg=u'根据sn获取小鱼信息')

            info(deviceInfo_sn.text)

        except Exception, e:
            error(e)
            error(deviceInfo_sn.url)
            error(deviceInfo_sn.request.body)
            error(deviceInfo_sn.text)
            raise e
        time.sleep(1)

        #修改小鱼终端
        info(u'修改小鱼终端')
        url_change_nemo = 'https://'+ self.ip+ conf_change_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number +'&displayName=changename_nemo_me90'
        print url_change_nemo
        change_nemo = requests_sig(conf_change_nemo['method'], url_change_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(change_nemo.status_code, 200, msg=u'修改小鱼终端')

            #self.assertEqual(change_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(change_nemo.url)
            error(change_nemo.request.body)
            error(change_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证修改')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证修改')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+'","name":"changename_nemo_me90"',msg=u'获取企业通讯录小鱼,验证修改')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #删除小鱼终端
        info(u'删除小鱼终端')
        url_del_nemo = 'https://'+ self.ip+ conf_del_nemo['uri'] + '?enterpriseId=' + self.enterpriseId + '&nemoNumber='+ number
        del_nemo = requests_sig(conf_del_nemo['method'], url_del_nemo,'',self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(del_nemo.status_code, 200, msg=u'删除小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(del_nemo.url)
            error(del_nemo.request.body)
            error(del_nemo.text)
            raise e
        time.sleep(1)
        #获取某个小鱼终端状态
        info(u'获取某个小鱼终端状态验证删除')
        url_que_nemo = ('https://'+ self.ip+ conf_user_que_nemo['uri'] + '?enterpriseId=' + self.enterpriseId) % number
        que_nemo = requests_sig(conf_user_que_nemo['method'], url_que_nemo,'',self.token, verify=False)
        try:
            self.assertEqual(que_nemo.status_code, 400, msg=u'获取某个小鱼终端状态验证删除')
            #self.assertEqual(que_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证修改')
        except Exception, e:
            error(e)
            error(que_nemo.url)
            error(que_nemo.request.body)
            error(que_nemo.text)
            raise e
        time.sleep(1)
        #添加小鱼终端
        info(u'添加小鱼终端')
        url_add_nemo = 'https://'+ self.ip+ conf_add_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [{"displayName":u"ME90_西安","nemoNumber":number}]
        add_nemo = requests_sig(conf_add_nemo['method'], url_add_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(add_nemo.status_code, 200, msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"failedDevices":null,',msg=u'添加小鱼终端')
            self.assertRegexpMatches(add_nemo.text,'"deviceSN":"'+sn+'"',msg=u'添加小鱼终端')
            #self.assertEqual(del_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据sn获取小鱼信息')
        except Exception, e:
            error(e)
            error(add_nemo.url)
            error(add_nemo.request.body)
            error(add_nemo.text)
            raise e
        time.sleep(1)
        #获取企业通讯录小鱼
        info(u'获取企业通讯录小鱼,验证添加')
        url_all_nemos = 'https://'+ self.ip+ conf_user_all_nemos['uri'] + '?enterpriseId=' + self.enterpriseId
        all_nemos = requests_sig(conf_user_all_nemos['method'], url_all_nemos,'',self.token, verify=False)
        try:
            self.assertEqual(all_nemos.status_code, 200, msg=u'获取企业通讯录小鱼,验证添加')
            self.assertRegexpMatches(all_nemos.text,'"number":"'+number+u'","name":"ME90_西安"',msg=u'获取企业通讯录小鱼,验证添加')
        except Exception, e:
            error(e)
            error(all_nemos.url)
            error(all_nemos.request.body)
            error(all_nemos.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量升级设备
        info(u'根据小鱼号批量升级设备')
        url_upgrade_nemo = 'https://'+ self.ip+ conf_upgrade_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        upgrade_nemo = requests_sig(conf_upgrade_nemo['method'], url_upgrade_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(upgrade_nemo.status_code, 200, msg=u'根据小鱼号批量升级设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(upgrade_nemo.url)
            error(upgrade_nemo.request.body)
            error(upgrade_nemo.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量重启设备
        info(u'根据小鱼号批量重启设备')
        url_reboot_nemo = 'https://'+ self.ip+ conf_reboot_nemo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        reboot_nemo = requests_sig(conf_reboot_nemo['method'], url_reboot_nemo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(reboot_nemo.status_code, 200, msg=u'根据小鱼号批量重启设备')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'获取某个小鱼终端状态验证添加')
        except Exception, e:
            error(e)
            error(reboot_nemo.url)
            error(reboot_nemo.request.body)
            error(reboot_nemo.text)
            raise e
        time.sleep(10)
        #根据小鱼号批量上传日志
        info(u'根据小鱼号批量上传日志')
        url_cat_log = 'https://'+ self.ip+ conf_cat_log['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        cat_log = requests_sig(conf_cat_log['method'], url_cat_log,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_log.status_code, 200, msg=u'根据小鱼号批量上传日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_log.url)
            error(cat_log.request.body)
            error(cat_log.text)
            raise e
        time.sleep(1)
        #根据小鱼号批量上传全量日志
        info(u'根据小鱼号批量上传全量日志')
        url_cat_fulllog = 'https://'+ self.ip+ conf_cat_fulllog['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [number]
        cat_fulllog = requests_sig(conf_cat_fulllog['method'], url_cat_fulllog,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(cat_fulllog.status_code, 200, msg=u'根据小鱼号批量上传全量日志')
            #self.assertEqual(upgrade_nemo.json()['mailbox'],self.mailuseractivate,msg=u'根据小鱼号批量上传日志')
        except Exception, e:
            error(e)
            error(cat_fulllog.url)
            error(cat_fulllog.request.body)
            error(cat_fulllog.text)
            raise e
        time.sleep(1)



if __name__ == '__main__':
    info(' start')
    unittest.main()
