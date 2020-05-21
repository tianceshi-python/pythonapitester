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
conf_meetingreminders_creat = {'method': 'POST','uri': '/api/rest/external/v1/meetingreminders'}
conf_meetingreminders_modify = {'method': 'PUT','uri': '/api/rest/external/v1/meetingreminders/%s'}
conf_meetingreminders_que = {'method': 'GET','uri': '/api/rest/external/v1/meetingreminders'}
conf_meetingreminders_del = {'method': 'DELETE','uri': '/api/rest/external/v1/meetingreminders/%s'}
conf_conferenceControl_currentMeeting = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/currentMeeting'}
conf_conferenceControl_end = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}

class meetingreminders(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.user1 = eval(allconf['enterprise']['user1'])
        self.user1confpwd = self.user1['confpwd']
        self.user1controlpwd = self.user1['controlpwd']
        self.user1confnumber = self.user1['confnumber']
        self.user1phone = self.user1['phone']
        self.NE60number = eval(allconf['enterprise']['ne60'])['number']

    @staticmethod
    def getTestFunc(testdata):
        def func(self):
            self.basecase(testdata)
        return func
    def basecase(self,casedata):
        ###预约会议###
        info(u'预约会议')
        start_time = (int(time.time())+60)*1000
        end_time = start_time + 600000
        end_time2 = end_time + 100000
        url_meetingreminders_creat = 'https://'+ self.ip+ conf_meetingreminders_creat['uri'] + '?enterpriseId=' + self.enterpriseId
        #data = eval(casedata['data'].encode("UTF-8") % ('start_time','end_time')) eval方法备份
        data = json.loads(casedata['data'] % (start_time,end_time))
        data["password"] = self.user1confpwd
        data["conferenceControlPassword"] = self.user1controlpwd
        data["conferenceNumber"] = self.user1confnumber
        data["participants"] = [self.user1phone,self.NE60number]
        meetingreminders_creat = requests_sig(conf_meetingreminders_creat['method'], url_meetingreminders_creat,data,self.token, verify=False,headers=self.headers_json)
        #断言response code
        if casedata.has_key('assert_code') and (casedata['assert_code'] != ''):
            try:
                self.assertEqual(meetingreminders_creat.status_code, casedata['assert_code'],msg=u'预约会议')
            except Exception, e:
                error(e)
                error(meetingreminders_creat.url)
                error(meetingreminders_creat.request.body)
                error(meetingreminders_creat.text)
                raise e
        meetingId = meetingreminders_creat.json()['meetingId']

        #jsonpath表达式备份。由于从excel中获取断言校验不太有单双引号问题，不使用了，
        #expr = '$.?(@.id=="'+meetingId+'")'
        #d1 = jsonpath.jsonpath(meetingreminders_que.json(), expr=expr)
        time.sleep(1)
        ###查询预约会议，验证创建时的配置
        info(u'查询预约会议')
        url_meetingreminders_que = 'https://'+ self.ip+ conf_meetingreminders_que['uri'] + '?enterpriseId=' + self.enterpriseId
        meetingreminders_que = requests_sig(conf_meetingreminders_que['method'], url_meetingreminders_que,"",self.token, verify=False)
        try:
            self.assertEqual(meetingreminders_que.status_code, 200,msg=u'查询预约会议')
        except Exception, e:
            error(e)
            error(meetingreminders_que.url)
            error(meetingreminders_que.request.body)
            error(meetingreminders_que.text)
            raise e
        #根据id，用正则提取查到的预约会议信息
        regexp_get_reminder = '{[^{]*'+ meetingId + '[^}]*}'
        remindertmp = re.findall(regexp_get_reminder, meetingreminders_que.text)

        if casedata.has_key('assert_tex_reg') and (casedata['assert_tex_reg'] != ''):
            regtextall = casedata['assert_tex_reg'].split(',,,')
            for regtext in regtextall:
                try:
                    self.assertRegexpMatches(str(remindertmp), regtext, msg=u'查询预约会议')
                except Exception, e:
                    error(e)
                    error(meetingreminders_que.url)
                    error(meetingreminders_que.request.body)
                    error(meetingreminders_que.text)
                    raise e
        time.sleep(90)
        ###查询会议状态
        info(u'查询会议状态')
        url_conferenceControl_currentMeeting = 'https://'+ self.ip+ conf_conferenceControl_currentMeeting['uri'] + '?enterpriseId=' + self.enterpriseId
        conferenceControl_currentMeeting = requests_sig(conf_conferenceControl_currentMeeting['method'], url_conferenceControl_currentMeeting,"",self.token, verify=False)
        try:
            self.assertRegexpMatches(conferenceControl_currentMeeting.text, self.user1confnumber, msg=u'查询会议状态,验证预约')

        except Exception, e:
            error(e)
            error(conferenceControl_currentMeeting.url)
            error(conferenceControl_currentMeeting.request.body)
            error(conferenceControl_currentMeeting.text)
            raise e
        time.sleep(1)
        ###结束会议
        info(u'结束会议')
        url_conferenceControl_end = ('https://'+ self.ip+ conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.user1confnumber
        conferenceControl_end = requests_sig(conf_conferenceControl_end['method'], url_conferenceControl_end,"",self.token, verify=False)
        try:
            self.assertEqual(conferenceControl_end.status_code, 200, msg=u'结束会议')
        except Exception, e:
            error(e)
            error(conferenceControl_end.url)
            error(conferenceControl_end.request.body)
            error(conferenceControl_end.text)
            raise e
        time.sleep(1)

        ###修改预约会议###
        info(u'修改预约会议')
        url_meetingreminders_modify = ('https://'+ self.ip+ conf_meetingreminders_modify['uri'] + '?enterpriseId=' + self.enterpriseId) % meetingId
        data_modify = {"address": "aAa1", "autoInvite": 0, "autoRecord": 0, "details": "修改详情", "endTime": end_time2, "meetingRoomType": 2,"startTime": start_time,"title": "修改title"}
        data_modify["password"] = self.user1confpwd
        data_modify["conferenceControlPassword"] = self.user1controlpwd
        data_modify["conferenceNumber"] = self.user1confnumber
        data_modify["participants"] = [self.user1phone,self.NE60number]
        meetingreminders_modify = requests_sig(conf_meetingreminders_modify['method'], url_meetingreminders_modify,data_modify,self.token, verify=False,headers=self.headers_json)

        #断言response code
        try:
            self.assertEqual(meetingreminders_modify.status_code, 200,msg=u'修改预约会议')
        except Exception, e:
            error(e)
            error(meetingreminders_modify.url)
            error(meetingreminders_modify.request.body)
            error(meetingreminders_modify.text)
            raise e

        time.sleep(1)


        ###查询预约会议，验证修改###
        info(u'查询预约会议,验证修改')
        url_meetingreminders_que = 'https://'+ self.ip+ conf_meetingreminders_que['uri'] + '?enterpriseId=' + self.enterpriseId
        meetingreminders_que2 = requests_sig(conf_meetingreminders_que['method'], url_meetingreminders_que,"",self.token, verify=False)
        try:
            self.assertEqual(meetingreminders_que2.status_code, 200,msg=u'查询预约会议，验证修改')
        except Exception, e:
            error(e)
            error(meetingreminders_que2.url)
            error(meetingreminders_que2.request.body)
            error(meetingreminders_que2.text)
            raise e
        #根据id，用正则提取查到的预约会议信息
        regexp_get_reminder = '{[^{]*'+ meetingId + '[^}]*}'
        remindertmp2 = re.findall(regexp_get_reminder, meetingreminders_que2.text)
        try:
            self.assertRegexpMatches(str(remindertmp2), '"address":"aAa1"', msg=u'查询预约会议,验证修改')
            self.assertRegexpMatches(str(remindertmp2), '"autoInvite":0', msg=u'查询预约会议,验证修改')
            self.assertRegexpMatches(str(remindertmp2), '"autoRecord":0', msg=u'查询预约会议,验证修改')
            self.assertRegexpMatches(str(remindertmp2), '"endTime":'+str(end_time2), msg=u'查询预约会议,验证修改')


            info('check ok:      ')
        except Exception, e:
            error(e)
            error(meetingreminders_que2.url)
            error(meetingreminders_que2.request.body)
            error(meetingreminders_que2.text)
            raise e
        time.sleep(1)

        ###删除预约会议###
        url_meetingreminders_del = ('https://'+ self.ip+ conf_meetingreminders_del['uri'] + '?enterpriseId=' + self.enterpriseId) % meetingId
        info(u'删除预约会议')
        meetingreminders_del = requests_sig(conf_meetingreminders_del['method'], url_meetingreminders_del,"",self.token, verify=False,headers=self.headers_json)
        #断言response code

        try:
            self.assertEqual(meetingreminders_del.status_code, 200,msg=u'删除预约会议')

        except Exception, e:
            error(e)
            error(meetingreminders_del.url)
            error(meetingreminders_del.text)
            raise e

        time.sleep(1)

        ###查询预约会议，验证删除###
        info(u'查询预约会议，验证删除')

        url_meetingreminders_que = 'https://'+ self.ip+ conf_meetingreminders_que['uri'] + '?enterpriseId=' + self.enterpriseId
        meetingreminders_que = requests_sig(conf_meetingreminders_que['method'], url_meetingreminders_que,"",self.token, verify=False)
        try:
            self.assertEqual(meetingreminders_que.status_code, 200,msg=u'查询预约会议，验证删除')
        except Exception, e:
            error(e)
            error(meetingreminders_que.url)
            error(meetingreminders_que.request.body)
            error(meetingreminders_que.text)
            raise e
        try:
            self.assertNotIn(meetingId,meetingreminders_que.text, msg=u'查询预约会议，验证删除预约会议')

        except Exception, e:
            error(e)
            error(meetingreminders_que.url)
            error(meetingreminders_que.text)
            raise e
        time.sleep(1)

#传入excel
def __generateTestCases(case_data_all):
    for casedata in case_data_all:
        if casedata['version'] == 'v1':
            setattr(meetingreminders, 'test_%s' % casedata['case_name'],meetingreminders.getTestFunc(casedata))
        elif casedata['version'] == 'v2':
            setattr(meetingreminders, 'test_creatv2_%s' % casedata['case_name'],meetingreminders.getTestFunc_v2(casedata))


ddd = get_data(dir_case, u'预约会议')
__generateTestCases(ddd)

if __name__ == '__main__':
    info(' start')


    unittest.main()
