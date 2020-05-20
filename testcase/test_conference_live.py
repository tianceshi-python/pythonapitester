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
conf_live_creat = {'method': 'POST','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live'}
conf_live_modify = {'method': 'PUT','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live/%s'}
conf_live_del = {'method': 'DELETE','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live/%s'}
conf_live_que = {'method': 'GET','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live/%s'}
conf_live_s = {'method': 'PUT','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live/%s/status'}
conf_live_vedio = {'method': 'GET','uri': '/api/rest/external/v1/liveVideo3/enterprise/%s/conf/%s/live/%s/videoswithduration'}
conf_live_ContentLayout = {'method': 'POST','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/liveContentLayout'}
conf_live_PeopleLayout = {'method': 'POST','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/livePeopleLayout'}


conf_conferenceControl_invitation = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/invitation'}
conf_conferenceControl_meetingStatus = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/%s/meetingStatus'}
conf_conferenceControl_end= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}



class Conference_live(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.cloudroom1_number = json.loads(allconf['enterprise']['cloudroom1'])['meetingNumber']
        self.cloudroom1_pwd = json.loads(allconf['enterprise']['cloudroom1'])['meetingControlPwd']
        self.cloudroom2_number = json.loads(allconf['enterprise']['cloudroom2'])['meetingNumber']
        self.cloudroom2_pwd = json.loads(allconf['enterprise']['cloudroom2'])['meetingControlPwd']
        self.NE60number = json.loads(allconf['enterprise']['ne60'])['number']
        self.NE60number_id = json.loads(allconf['enterprise']['ne60'])['deviceId']
        self.NE60number_type = json.loads(allconf['enterprise']['ne60'])['type']
        self.ME40number = json.loads(allconf['enterprise']['me40'])['number']
        self.ME40number_id = json.loads(allconf['enterprise']['me40'])['deviceId']
        self.ME40number_type = json.loads(allconf['enterprise']['me40'])['type']

        self.startTime = int(time.time()+120)*1000
        self.endTime = (int(time.time())+1200)*1000
    @classmethod
    def tearDownClass(self):
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        print url_end
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        info(end.text)


    def test_cloudroom_live(self):
        confno = self.cloudroom1_number
        confpwd = self.cloudroom1_pwd
        starttime = self.startTime
        endtime = self.endTime
        ne60 = self.NE60number
        title = u'直播测试'
        detail = u'云会议室直播测试'
        location = u'西安'
        id = self.NE60number_id
        type = self.NE60number_type
        #预约直播
        info(u'预约直播')
        url_live_creat = ('https://'+ self.ip+ conf_live_creat['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno)
        data = {
   "title":title,
   "startTime":starttime,
   "endTime":endtime,
   "detail":detail,
   "autoRecording":"false",
   "autoPublishRecording":"false",
   "location":location
}
        live_creat = requests_sig(conf_live_creat['method'], url_live_creat,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_creat.status_code, 200, msg=u'预约直播')
            liveid = live_creat.json()['liveId']
            self.assertRegexpMatches(live_creat.text,'"autoRecording":false',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"autoPublishRecording":false',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"confNo":"'+confno,msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"status":"WAIT"',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"viewUrl":"http.*'+liveid,msg=u'预约直播')
        except Exception, e:
            error(e)
            error(live_creat.url)
            error(live_creat.request.body)
            error(live_creat.text)
            raise e
        time.sleep(2)

        #查询直播
        info(u'查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":false',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":false',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"viewUrl":"http.*'+liveid,msg=u'查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #修改直播
        info(u'修改直播')
        url_live_modify = ('https://'+ self.ip+ conf_live_modify['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data = {
   "title":u"修改直播title",
   "detail":u"修改直播详情",
   "autoRecording":"true",
   "autoPublishRecording":"true",
   "location":u"修改直播地点"
}
        live_modify = requests_sig(conf_live_modify['method'], url_live_modify,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_modify.status_code, 204, msg=u'修改直播')

        except Exception, e:
            error(e)
            error(live_modify.url)
            error(live_modify.request.body)
            error(live_modify.text)
            raise e
        time.sleep(2)
        #修改后查询直播
        info(u'修改后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'修改后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #开始会议
        info(u'邀请入会')
        url_invitation = 'https://'+ self.ip+ conf_conferenceControl_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": confno,"deviceList":[{"number":ne60}]}
        invitation = requests_sig(conf_conferenceControl_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(invitation.status_code, 200, msg=u'邀请入会')
        except Exception, e:
            error(e)
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise e
        time.sleep(5)
        #查询会议状态
        info(u'查询会议状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_conferenceControl_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        meetingStatus = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,'"participantNumber":"'+self.NE60number+'"',msg=u'查询会议状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        time.sleep(1)
        #开始直播
        info(u'开始直播')
        url_live_start = ('https://'+ self.ip+ conf_live_s['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data ={"status":"start"}
        live_start = requests_sig(conf_live_s['method'], url_live_start,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_start.status_code, 204, msg=u'开始直播')
        except Exception, e:
            error(e)
            error(live_start.url)
            error(live_start.request.body)
            error(live_start.text)
            raise e
        time.sleep(5)
        #开始后查询直播
        info(u'开始后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"LIVING"',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"viewUrl":"http.*'+liveid,msg=u'开始后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #设置人物布局
        info(u'设置人物布局')
        url_live_PeopleLayout = ('https://' + self.ip + conf_live_PeopleLayout['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        data = {
   "peopleLayoutType":"MULTI",
   "mainImageId":id,
   "mainImageType":type
}
        live_PeopleLayout = requests_sig(conf_live_PeopleLayout['method'], url_live_PeopleLayout, data, self.token, verify=False,
                                  headers=self.headers_json)
        try:
            self.assertEqual(live_PeopleLayout.status_code, 200, msg=u'设置人物布局')
        except Exception, e:
            error(e)
            error(live_PeopleLayout.url)
            error(live_PeopleLayout.request.body)
            error(live_PeopleLayout.text)
            raise e
        time.sleep(1)
        # 设置content布局
        info(u'设置content布局')
        url_live_ContentLayout = ('https://' + self.ip + conf_live_ContentLayout['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        data = {
            "contentLayout":"SMART",
            "mainImageId": id,
            "mainImageType": type
        }
        live_ContentLayout = requests_sig(conf_live_ContentLayout['method'], url_live_ContentLayout, data, self.token,verify=False,                                         headers=self.headers_json)
        try:
            self.assertEqual(live_ContentLayout.status_code, 200, msg=u'设置content布局')
        except Exception, e:
            error(e)
            error(live_ContentLayout.url)
            error(live_ContentLayout.request.body)
            error(live_ContentLayout.text)
            raise e
        time.sleep(1)
        #停止直播
        info(u'停止直播')
        url_live_stop = ('https://'+ self.ip+ conf_live_s['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data ={"status":"end"}
        live_stop = requests_sig(conf_live_s['method'], url_live_start,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_stop.status_code, 204, msg=u'停止直播')
        except Exception, e:
            error(e)
            error(live_stop.url)
            error(live_stop.request.body)
            error(live_stop.text)
            raise e
        time.sleep(5)
        #停止后查询直播
        info(u'停止后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'停止后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #删除直播
        info(u'删除直播')
        url_live_del = ('https://'+ self.ip+ conf_live_del['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_del = requests_sig(conf_live_del['method'], url_live_del,'',self.token, verify=False)
        try:
            self.assertEqual(live_del.status_code, 204, msg=u'删除直播')
        except Exception, e:
            error(e)
            error(live_del.url)
            error(live_del.request.body)
            error(live_del.text)
            raise e
        time.sleep(1)
        #删除后查询直播
        info(u'删除后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"NOT_FOUND"',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'删除后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        #获取当前直播的视频列表
        info(u'获取当前直播的视频列表')
        url_live_vedio = ('https://'+ self.ip+ conf_live_vedio['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_vedio = requests_sig(conf_live_vedio['method'], url_live_vedio,'',self.token, verify=False)
        try:
            self.assertEqual(live_vedio.status_code, 200, msg=u'获取当前直播的视频列表')
            self.assertRegexpMatches(live_vedio.text,'"url":"http.*'+liveid+'.*mp4',msg=u'获取当前直播的视频列表')
        except Exception, e:
            error(e)
            error(live_vedio.url)
            error(live_vedio.request.body)
            error(live_vedio.text)
            raise e
        time.sleep(1)

    def test_cloudroom_live_ne60(self):
        confno = self.cloudroom2_number
        confpwd = self.cloudroom2_pwd
        starttime = self.startTime
        endtime = self.endTime
        ne60 = self.NE60number
        title = u'直播测试'
        detail = u'云会议室直播测试'
        location = u'西安'
        id = self.NE60number_id
        type = self.NE60number_type
        #预约直播
        info(u'预约直播')
        url_live_creat = ('https://'+ self.ip+ conf_live_creat['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno)
        data = {
                "title":title,
                "startTime":starttime,
                "endTime":endtime,
                "detail":detail,
                "autoRecording":"false",
                "autoPublishRecording":"false",
                "location":location,
                "nemoNumber":self.NE60number
}
        live_creat = requests_sig(conf_live_creat['method'], url_live_creat,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_creat.status_code, 200, msg=u'预约直播')
            liveid = live_creat.json()['liveId']
            self.assertRegexpMatches(live_creat.text,'"autoRecording":false',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"autoPublishRecording":false',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"confNo":"'+confno,msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"status":"WAIT"',msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"viewUrl":"http.*'+liveid,msg=u'预约直播')
            self.assertRegexpMatches(live_creat.text,'"nemoNumber":"'+self.NE60number,msg=u'预约直播')

        except Exception, e:
            error(e)
            error(live_creat.url)
            error(live_creat.request.body)
            error(live_creat.text)
            raise e
        time.sleep(2)

        #查询直播
        info(u'查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":false',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":false',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'查询直播')
            self.assertRegexpMatches(live_que.text,'"viewUrl":"http.*'+liveid,msg=u'查询直播')
            self.assertRegexpMatches(live_que.text, '"nemoNumber":"' + self.NE60number, msg=u'查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #修改直播
        info(u'修改直播')
        url_live_modify = ('https://'+ self.ip+ conf_live_modify['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data = {
   "title":u"修改直播title",
   "detail":u"修改直播详情",
   "autoRecording":"true",
   "autoPublishRecording":"true",
   "location":u"修改直播地点"
}
        live_modify = requests_sig(conf_live_modify['method'], url_live_modify,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_modify.status_code, 204, msg=u'修改直播')

        except Exception, e:
            error(e)
            error(live_modify.url)
            error(live_modify.request.body)
            error(live_modify.text)
            raise e
        time.sleep(2)
        #修改后查询直播
        info(u'修改后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"nemoNumber":""', msg=u'修改后查询直播')

        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        # 修改直播
        info(u'修改直播')
        url_live_modify = ('https://' + self.ip + conf_live_modify[
            'uri'] + '?confPwd=' + confpwd + '&enterpriseId=' + self.enterpriseId) % (self.enterpriseId, confno, liveid)
        data = {
            "title": u"修改直播title",
            "detail": u"修改直播详情",
            "autoRecording": "true",
            "autoPublishRecording": "true",
            "location": u"修改直播地点",
            "nemoNumber":self.NE60number

        }
        live_modify = requests_sig(conf_live_modify['method'], url_live_modify, data, self.token, verify=False,
                                   headers=self.headers_json)
        try:
            self.assertEqual(live_modify.status_code, 204, msg=u'修改直播')

        except Exception, e:
            error(e)
            error(live_modify.url)
            error(live_modify.request.body)
            error(live_modify.text)
            raise e
        time.sleep(2)
        # 修改后查询直播
        info(u'修改后查询直播')
        url_live_que = ('https://' + self.ip + conf_live_que[
            'uri'] + '?confPwd=' + confpwd + '&enterpriseId=' + self.enterpriseId) % (self.enterpriseId, confno, liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que, '', self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"autoRecording":true', msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"autoPublishRecording":true', msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"confNo":"' + confno, msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"status":"WAIT"', msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"liveId":"' + liveid, msg=u'修改后查询直播')
            self.assertRegexpMatches(live_que.text, '"nemoNumber":"' + self.NE60number, msg=u'修改后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #开始会议
        info(u'邀请入会')
        url_invitation = 'https://'+ self.ip+ conf_conferenceControl_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": confno,"deviceList":[{"number":ne60}]}
        invitation = requests_sig(conf_conferenceControl_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(invitation.status_code, 200, msg=u'邀请入会')
        except Exception, e:
            error(e)
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise e
        time.sleep(5)
        #查询会议状态
        info(u'查询会议状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_conferenceControl_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        meetingStatus = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,'"participantNumber":"'+self.NE60number+'"',msg=u'查询会议状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        #开始直播
        info(u'开始直播')
        url_live_start = ('https://'+ self.ip+ conf_live_s['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data ={"status":"start"}
        live_start = requests_sig(conf_live_s['method'], url_live_start,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_start.status_code, 204, msg=u'开始直播')
        except Exception, e:
            error(e)
            error(live_start.url)
            error(live_start.request.body)
            error(live_start.text)
            raise e
        time.sleep(5)
        #开始后查询直播
        info(u'开始后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"LIVING"',msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text,'"viewUrl":"http.*'+liveid,msg=u'开始后查询直播')
            self.assertRegexpMatches(live_que.text, '"nemoNumber":"' + self.NE60number, msg=u'开始后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #设置人物布局
        info(u'设置人物布局')
        url_live_PeopleLayout = ('https://' + self.ip + conf_live_PeopleLayout['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        data = {
   "peopleLayoutType":"MULTI",
   "mainImageId":id,
   "mainImageType":type
}
        live_PeopleLayout = requests_sig(conf_live_PeopleLayout['method'], url_live_PeopleLayout, data, self.token, verify=False,
                                  headers=self.headers_json)
        try:
            self.assertEqual(live_PeopleLayout.status_code, 200, msg=u'设置人物布局')
        except Exception, e:
            error(e)
            error(live_PeopleLayout.url)
            error(live_PeopleLayout.request.body)
            error(live_PeopleLayout.text)
            raise e
        time.sleep(2)
        # 设置content布局
        info(u'设置content布局')
        url_live_ContentLayout = ('https://' + self.ip + conf_live_ContentLayout['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        data = {
            "contentLayout":"SMART",
            "mainImageId": id,
            "mainImageType": type
        }
        live_ContentLayout = requests_sig(conf_live_ContentLayout['method'], url_live_ContentLayout, data, self.token,verify=False,                                         headers=self.headers_json)
        try:
            self.assertEqual(live_ContentLayout.status_code, 200, msg=u'设置content布局')
        except Exception, e:
            error(e)
            error(live_ContentLayout.url)
            error(live_ContentLayout.request.body)
            error(live_ContentLayout.text)
            raise e
        time.sleep(2)
        #停止直播
        info(u'停止直播')
        url_live_stop = ('https://'+ self.ip+ conf_live_s['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        data ={"status":"end"}
        live_stop = requests_sig(conf_live_s['method'], url_live_start,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(live_stop.status_code, 204, msg=u'停止直播')
        except Exception, e:
            error(e)
            error(live_stop.url)
            error(live_stop.request.body)
            error(live_stop.text)
            raise e
        time.sleep(5)
        #停止后查询直播
        info(u'停止后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"WAIT"',msg=u'停止后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'停止后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #删除直播
        info(u'删除直播')
        url_live_del = ('https://'+ self.ip+ conf_live_del['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_del = requests_sig(conf_live_del['method'], url_live_del,'',self.token, verify=False)
        try:
            self.assertEqual(live_del.status_code, 204, msg=u'删除直播')
        except Exception, e:
            error(e)
            error(live_del.url)
            error(live_del.request.body)
            error(live_del.text)
            raise e
        time.sleep(1)
        #删除后查询直播
        info(u'删除后查询直播')
        url_live_que = ('https://'+ self.ip+ conf_live_que['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_que = requests_sig(conf_live_que['method'], url_live_que,'',self.token, verify=False)
        try:
            self.assertEqual(live_que.status_code, 200, msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoRecording":true',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"autoPublishRecording":true',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"confNo":"'+confno,msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"status":"NOT_FOUND"',msg=u'删除后查询直播')
            self.assertRegexpMatches(live_que.text,'"liveId":"'+liveid,msg=u'删除后查询直播')
        except Exception, e:
            error(e)
            error(live_que.url)
            error(live_que.request.body)
            error(live_que.text)
            raise e
        time.sleep(1)
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % confno
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        #获取当前直播的视频列表
        info(u'获取当前直播的视频列表')
        url_live_vedio = ('https://'+ self.ip+ conf_live_vedio['uri'] + '?confPwd='+ confpwd +'&enterpriseId=' + self.enterpriseId) % (self.enterpriseId,confno,liveid)
        live_vedio = requests_sig(conf_live_vedio['method'], url_live_vedio,'',self.token, verify=False)
        try:
            self.assertEqual(live_vedio.status_code, 200, msg=u'获取当前直播的视频列表')
            self.assertRegexpMatches(live_vedio.text,'"url":"http.*'+liveid+'.*mp4',msg=u'获取当前直播的视频列表')
        except Exception, e:
            error(e)
            error(live_vedio.url)
            error(live_vedio.request.body)
            error(live_vedio.text)
            raise e
        time.sleep(1)


if __name__ == '__main__':
    info(' start')


    unittest.main()
