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

conf_invitation = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/invitation'}
conf_stop_meeting = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}
conf_start_recoding = {'method': 'GET','uri': '/api/rest/external/v1/meeting/recording/%s/start'}
conf_stop_recoding = {'method': 'GET','uri': '/api/rest/external/v1/meeting/recording/%s/stop'}
conf_stop_recoding_v2 = {'method': 'GET','uri': '/api/rest/external/v2/meeting/recording/%s/stopWithSessionId'}
conf_geturl_by_se = {'method': 'GET','uri': '/api/rest/external/v1/vods/session/%s/downloadurl'}
conf_get_recoders_byroom = {'method': 'GET','uri': '/api/rest/external/v1/meetingroom/%s/vods'}
conf_get_recoders_bynemo = {'method': 'GET','uri': '/api/rest/external/v1/nemo/%s/vods'}
conf_get_recoders_byext = {'method': 'GET','uri': '/api/rest/external/v1/vods'}
conf_get_thumbnail = {'method': 'GET','uri': '/api/rest/external/v1/vods/%s/thumbnail'}
conf_get_sharedInfo = {'method': 'GET','uri': '/api/rest/external/v1/vods/%s/sharedInfo'}
conf_get_downloadurl = {'method': 'GET','uri': '/api/rest/external/v1/vods/%s/getdownloadurl'}
conf_del_recoders = {'method': 'DELETE','uri': '/api/rest/external/v1/meetingroom/%s/vods'}
conf_del_recoder = {'method': 'DELETE','uri': '/api/rest/external/v1/vods/%s'}
conf_conferenceControl_meetingStatus = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/%s/meetingStatus'}
conf_conferenceControl_end= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}


class Recording_video(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.cloudroom1_number = json.loads(allconf['enterprise']['cloudroom1'])['meetingNumber']
        self.NE60number = json.loads(allconf['enterprise']['ne60'])['number']
        self.startTime = int(time.time())*1000
        self.endTime = (int(time.time())+30)*1000
        self.user1_confnumber = json.loads(allconf['enterprise']['user1'])['confnumber']

    @classmethod
    def tearDownClass(self):
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        info(end.text)
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.user1_confnumber
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        info(end.text)


    def test_recording_v1(self):
        cloudroom1 = self.user1_confnumber
        NE60 = self.NE60number
        #开始会议
        info(u'开始会议')
        url_invitation = 'https://'+ self.ip+ conf_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": cloudroom1,"deviceList":[{"number":NE60}]}
        invitation = requests_sig(conf_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(invitation.status_code, 200, msg=u'开始会议')
        except Exception, e:
            error(e)
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise e
        time.sleep(5)
        #查询会议状态
        info(u'查询会议状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_conferenceControl_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        meetingStatus = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,'"participantNumber":"'+NE60+'"',msg=u'查询会议状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        time.sleep(1)
        #开始录制
        info(u'开始录制')
        url_start_recoding = ('https://'+ self.ip+ conf_start_recoding['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        start_recoding = requests_sig(conf_start_recoding['method'], url_start_recoding,'',self.token, verify=False)
        try:
            self.assertEqual(start_recoding.status_code, 200, msg=u'开始录制')

        except Exception, e:
            error(e)
            error(start_recoding.url)
            error(start_recoding.request.body)
            error(start_recoding.text)
            raise e
        time.sleep(10)
        #停止录制
        info(u'停止录制')
        url_stop_recoding = ('https://'+ self.ip+ conf_stop_recoding['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        stop_recoding = requests_sig(conf_stop_recoding['method'], url_stop_recoding,'',self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(stop_recoding.status_code, 200, msg=u'停止录制')
            self.assertRegexpMatches(stop_recoding.text,'"recordingStatusResponse":"OK"',msg=u'停止录制')
            self.assertRegexpMatches(stop_recoding.text,'"downLoadRestApi":"http.*',msg=u'停止录制')
        except Exception, e:
            error(e)
            error(stop_recoding.url)
            error(stop_recoding.request.body)
            error(stop_recoding.text)
            raise e
        time.sleep(2)


        #结束会议
        info(u'结束会议')
        url_stop_meeting = ('https://'+ self.ip+ conf_stop_meeting['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        stop_meeting = requests_sig(conf_stop_meeting['method'], url_stop_meeting,'',self.token, verify=False)
        try:
            self.assertEqual(stop_meeting.status_code, 200, msg=u'结束会议')
        except Exception, e:
            error(e)
            error(stop_meeting.url)
            error(stop_meeting.request.body)
            error(stop_meeting.text)
            raise e
        time.sleep(5)
        self.endTime = int(time.time())*1000
        time.sleep(5)
        #根据云会议室查询录制文件_时间段
        info(u'根据云会议室查询录制文件_时间段')
        url_get_recoders = ('https://'+ self.ip+ conf_get_recoders_byroom['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1 + '&startTime=' + str(self.startTime) + '&endTime=' + str(self.endTime)
        get_recoders = requests_sig(conf_get_recoders_byroom['method'], url_get_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders.status_code, 200, msg=u'根据云会议室查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据云会议室查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据云会议室查询录制文件_时间段')
            vodId = get_recoders.json()[0]['vodId']
        except Exception, e:
            error(e)
            error(get_recoders.url)
            error(get_recoders.request.body)
            error(get_recoders.text)
            raise e
        time.sleep(1)

        #根据云会议室查询录制文件_所有
        info(u'根据云会议室查询录制文件_所有')
        url_get_recoders = ('https://'+ self.ip+ conf_get_recoders_byroom['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        get_recoders = requests_sig(conf_get_recoders_byroom['method'], url_get_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders.status_code, 200, msg=u'根据云会议室查询录制文件_所有')
            info(get_recoders.text)
            info(len(get_recoders.text))
        except Exception, e:
            error(e)
            error(get_recoders.url)
            error(get_recoders.request.body)
            error(get_recoders.text)
            raise e
        time.sleep(1)
        #根据小鱼号查询录制文件
        info(u'根据小鱼号查询录制文件')
        url_get_recoders_bynemo = ('https://'+ self.ip+ conf_get_recoders_bynemo['uri'] + '?enterpriseId=' + self.enterpriseId) % NE60
        get_recoders_bynemo = requests_sig(conf_get_recoders_bynemo['method'], url_get_recoders_bynemo,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_bynemo.status_code, 200, msg=u'根据小鱼号查询录制文件')
            info(get_recoders_bynemo.text)
        except Exception, e:
            error(e)
            error(get_recoders_bynemo.url)
            error(get_recoders_bynemo.request.body)
            error(get_recoders_bynemo.text)
            raise e
        time.sleep(1)
        #根据企业查询录制文件
        info(u'根据企业查询录制文件一天')
        url_get_recoders_byext = 'https://'+ self.ip+ conf_get_recoders_byext['uri'] + '?enterpriseId=' + self.enterpriseId +'&startTime=' + str(self.endTime-86400000) + '&endTime=' + str(self.endTime)
        get_recoders_byext = requests_sig(conf_get_recoders_byext['method'], url_get_recoders_byext,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_byext.status_code, 200, msg=u'根据企业查询录制文件一天')
            self.assertRegexpMatches(get_recoders_byext.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext.text,str(vodId),msg=u'根据企业查询录制文件_时间段')
        except Exception, e:
            error(e)
            error(get_recoders_byext.url)
            error(get_recoders_byext.request.body)
            error(get_recoders_byext.text)
            raise e
        time.sleep(1)
        #根据企业查询录制文件_时间段
        info(u'根据企业查询录制文件_时间段')
        url_get_recoders_byext = 'https://'+ self.ip+ conf_get_recoders_byext['uri'] + '?enterpriseId=' + self.enterpriseId +'&startTime=' + str(self.startTime) + '&endTime=' + str(self.endTime)
        get_recoders_byext2 = requests_sig(conf_get_recoders_byext['method'], url_get_recoders_byext,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_byext2.status_code, 200, msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext2.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext2.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext2.text,str(vodId),msg=u'根据企业查询录制文件_时间段')

        except Exception, e:
            error(e)
            error(get_recoders_byext2.url)
            error(get_recoders_byext2.request.body)
            error(get_recoders_byext2.text)
            raise e
        time.sleep(1)
        #根据vodId获取缩略图
        info(u'根据vodId获取缩略图')
        url_get_thumbnail = ('https://'+ self.ip+ conf_get_thumbnail['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_thumbnail = requests_sig(conf_get_thumbnail['method'], url_get_thumbnail,'',self.token, verify=False)
        try:
            self.assertEqual(get_thumbnail.status_code, 200, msg=u'根据vodId获取缩略图')
        except Exception, e:
            error(e)
            error(get_thumbnail.url)
            error(get_thumbnail.request.body)
            error(get_thumbnail.text)
            raise e
        time.sleep(1)
        #根据vodId获取播放链接
        info(u'根据vodId获取播放链接')
        url_get_sharedInfo = ('https://'+ self.ip+ conf_get_sharedInfo['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_sharedInfo = requests_sig(conf_get_sharedInfo['method'], url_get_sharedInfo,'',self.token, verify=False)
        try:
            self.assertEqual(get_sharedInfo.status_code, 200, msg=u'根据vodId获取播放链接')
            self.assertRegexpMatches(get_sharedInfo.text,'"shared":false',msg=u'根据vodId获取播放链接')
            self.assertRegexpMatches(get_sharedInfo.text,'"playUrl":"http.*',msg=u'根据vodId获取播放链接')


            info(get_sharedInfo.text)
        except Exception, e:
            error(e)
            error(get_sharedInfo.url)
            error(get_sharedInfo.request.body)
            error(get_sharedInfo.text)
            raise e
        time.sleep(1)
        #根据vodId获取下载链接
        info(u'根据vodId获取下载链接')
        url_get_downloadurl = ('https://'+ self.ip+ conf_get_downloadurl['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_downloadurl = requests_sig(conf_get_downloadurl['method'], url_get_downloadurl,'',self.token, verify=False)
        try:
            self.assertEqual(get_downloadurl.status_code, 200, msg=u'根据vodId获取下载链接')
            self.assertRegexpMatches(get_downloadurl.text,'"downloadUrl":null,"status":777001',msg=u'根据vodId获取下载链接')
        except Exception, e:
            error(e)
            error(get_downloadurl.url)
            error(get_downloadurl.request.body)
            error(get_downloadurl.text)
            raise e
        time.sleep(5)
        #根据vodId获取下载链接
        info(u'根据vodId获取下载链接')
        url_get_downloadurl = ('https://'+ self.ip+ conf_get_downloadurl['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_downloadurl = requests_sig(conf_get_downloadurl['method'], url_get_downloadurl,'',self.token, verify=False)
        try:
            self.assertEqual(get_downloadurl.status_code, 200, msg=u'根据vodId获取下载链接')
            self.assertRegexpMatches(get_downloadurl.text,'status":777000',msg=u'根据vodId获取下载链接')
            self.assertRegexpMatches(get_downloadurl.text,'"downloadUrl":"http.*',msg=u'根据vodId获取下载链接')
        except Exception, e:
            error(e)
            error(get_downloadurl.url)
            error(get_downloadurl.request.body)
            error(get_downloadurl.text)
            raise e
        time.sleep(1)
        #根据vodId删除视频
        info(u'根据vodId删除视频')
        url_del_recoder = ('https://'+ self.ip+ conf_del_recoder['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        del_recoder = requests_sig(conf_del_recoder['method'], url_del_recoder,'',self.token, verify=False)
        try:
            self.assertEqual(del_recoder.status_code, 200, msg=u'根据vodId删除视频')
        except Exception, e:
            error(e)
            error(del_recoder.url)
            error(del_recoder.request.body)
            error(del_recoder.text)
            raise e
        time.sleep(1)
        #验证删除
        info(u'验证删除')
        url_get_sharedInfo = ('https://'+ self.ip+ conf_get_sharedInfo['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_sharedInfo = requests_sig(conf_get_sharedInfo['method'], url_get_sharedInfo,'',self.token, verify=False)
        try:
            self.assertEqual(get_sharedInfo.status_code, 400, msg=u'验证删除')
            self.assertRegexpMatches(get_sharedInfo.text,'OPENAPI_VOD_INVALID_ID Invalid vod id',msg=u'验证删除')

        except Exception, e:
            error(e)
            error(get_sharedInfo.url)
            error(get_sharedInfo.request.body)
            error(get_sharedInfo.text)
            raise e
        time.sleep(1)


    def test_recording_v2(self):
        startTime = int(time.time())*1000
        #cloudroom1 = self.cloudroom1_number
        cloudroom1 = self.user1_confnumber

        NE60 = self.NE60number
        #开始会议
        info(u'录制v2')
        info(u'开始会议')
        url_invitation = 'https://'+ self.ip+ conf_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": cloudroom1,"deviceList":[{"number":NE60}]}
        invitation = requests_sig(conf_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(invitation.status_code, 200, msg=u'开始会议')
        except Exception, e:
            error(e)
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise e
        time.sleep(5)
        #查询会议状态
        info(u'查询会议状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_conferenceControl_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        meetingStatus = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,'"participantNumber":"'+NE60+'"',msg=u'查询会议状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        time.sleep(2)
        #开始录制
        info(u'开始录制')
        url_start_recoding = ('https://'+ self.ip+ conf_start_recoding['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        start_recoding = requests_sig(conf_start_recoding['method'], url_start_recoding,'',self.token, verify=False)
        try:
            self.assertEqual(start_recoding.status_code, 200, msg=u'开始录制')

        except Exception, e:
            error(e)
            error(start_recoding.url)
            error(start_recoding.request.body)
            error(start_recoding.text)
            raise e
        time.sleep(15)
        #停止录制v2
        info(u'停止录制v2')
        url_stop_recoding = ('https://'+ self.ip+ conf_stop_recoding_v2['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        stop_recoding = requests_sig(conf_stop_recoding_v2['method'], url_stop_recoding,'',self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(stop_recoding.status_code, 200, msg=u'停止录制v2')
            self.assertRegexpMatches(stop_recoding.text,'"recordingStatusResponse":"OK"',msg=u'停止录制v2')
            self.assertRegexpMatches(stop_recoding.text,'"sessionId":"'+cloudroom1+'@CONFNO_.*"',msg=u'停止录制v2')

            sessionId = stop_recoding.json()['sessionId']
        except Exception, e:
            error(e)
            error(stop_recoding.url)
            error(stop_recoding.request.body)
            error(stop_recoding.text)
            raise e
        time.sleep(5)
        #根据sessionid获取下载链接
        info(u'根据sessionid获取下载链接')
        url_geturl_by_se = ('https://'+ self.ip+ conf_geturl_by_se['uri'] + '?enterpriseId=' + self.enterpriseId ) % sessionId
        geturl_by_se = requests_sig(conf_geturl_by_se['method'], url_geturl_by_se,'',self.token, verify=False)
        try:
            self.assertEqual(geturl_by_se.status_code, 200, msg=u'根据sessionid获取下载链接')
            info(geturl_by_se.text)
        except Exception, e:
            error(e)
            error(geturl_by_se.url)
            error(geturl_by_se.request.body)
            error(geturl_by_se.text)
            raise e
        time.sleep(20)
        #根据sessionid获取下载链接
        info(u'根据sessionid获取下载链接')
        url_geturl_by_se = ('https://'+ self.ip+ conf_geturl_by_se['uri'] + '?enterpriseId=' + self.enterpriseId ) % sessionId
        geturl_by_se = requests_sig(conf_geturl_by_se['method'], url_geturl_by_se,'',self.token, verify=False)
        try:
            self.assertEqual(geturl_by_se.status_code, 200, msg=u'根据sessionid获取下载链接')
            self.assertRegexpMatches(geturl_by_se.text,'"status":777000',msg=u'根据sessionid获取下载链接')
            self.assertRegexpMatches(geturl_by_se.text,'"downloadUrl":"http.*',msg=u'根据sessionid获取下载链接')
            info(geturl_by_se.text)
        except Exception, e:
            error(e)
            error(geturl_by_se.url)
            error(geturl_by_se.request.body)
            error(geturl_by_se.text)
            raise e
        time.sleep(1)
        #结束会议
        info(u'结束会议')
        url_stop_meeting = ('https://'+ self.ip+ conf_stop_meeting['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        stop_meeting = requests_sig(conf_stop_meeting['method'], url_stop_meeting,'',self.token, verify=False)
        try:
            self.assertEqual(stop_meeting.status_code, 200, msg=u'结束会议')
        except Exception, e:
            error(e)
            error(stop_meeting.url)
            error(stop_meeting.request.body)
            error(stop_meeting.text)
            raise e
        time.sleep(5)
        endTime = int(time.time())*1000
        time.sleep(5)
        #根据云会议室查询录制文件_时间段
        info(u'根据云会议室查询录制文件_时间段')
        url_get_recoders = ('https://'+ self.ip+ conf_get_recoders_byroom['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1 + '&startTime=' + str(startTime) + '&endTime=' + str(endTime)
        get_recoders = requests_sig(conf_get_recoders_byroom['method'], url_get_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders.status_code, 200, msg=u'根据云会议室查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders.text, '"meetingRoomNumber":"' + cloudroom1 + '"',
                                     msg=u'根据云会议室查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders.text, '"vodMetadataType":"SERVER_RECORD"', msg=u'根据云会议室查询录制文件_时间段')
            vodId = get_recoders.json()[0]['vodId']
        except Exception, e:
            error(e)
            error(get_recoders.url)
            error(get_recoders.request.body)
            error(get_recoders.text)
            raise e
        time.sleep(1)

        #根据云会议室查询录制文件_所有
        info(u'根据云会议室查询录制文件_所有')
        url_get_recoders = ('https://'+ self.ip+ conf_get_recoders_byroom['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        get_recoders = requests_sig(conf_get_recoders_byroom['method'], url_get_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders.status_code, 200, msg=u'根据云会议室查询录制文件_所有')
            self.assertRegexpMatches(get_recoders.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据云会议室查询录制文件_所有')
            self.assertRegexpMatches(get_recoders.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据云会议室查询录制文件_所有')
            self.assertRegexpMatches(get_recoders.text,str(vodId),msg=u'根据云会议室查询录制文件_所有')
        except Exception, e:
            error(e)
            error(get_recoders.url)
            error(get_recoders.request.body)
            error(get_recoders.text)
            raise e
        time.sleep(1)
        #根据小鱼号查询录制文件
        info(u'根据小鱼号查询录制文件')
        url_get_recoders_bynemo = ('https://'+ self.ip+ conf_get_recoders_bynemo['uri'] + '?enterpriseId=' + self.enterpriseId) % NE60
        get_recoders_bynemo = requests_sig(conf_get_recoders_bynemo['method'], url_get_recoders_bynemo,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_bynemo.status_code, 200, msg=u'根据小鱼号查询录制文件')
            info(get_recoders_bynemo.text)
        except Exception, e:
            error(e)
            error(get_recoders_bynemo.url)
            error(get_recoders_bynemo.request.body)
            error(get_recoders_bynemo.text)
            raise e
        time.sleep(1)
        #根据企业查询录制文件
        info(u'根据企业查询录制文件一天')
        url_get_recoders_byext = 'https://'+ self.ip+ conf_get_recoders_byext['uri'] + '?enterpriseId=' + self.enterpriseId +'&startTime=' + str(endTime-86400000) + '&endTime=' + str(endTime)
        get_recoders_byext = requests_sig(conf_get_recoders_byext['method'], url_get_recoders_byext,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_byext.status_code, 200, msg=u'根据企业查询录制文件一天')
            self.assertRegexpMatches(get_recoders_byext.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据企业查询录制文件一天')
            self.assertRegexpMatches(get_recoders_byext.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据企业查询录制文件一天')
            self.assertRegexpMatches(get_recoders_byext.text,str(vodId),msg=u'根据企业查询录制文件一天')
        except Exception, e:
            error(e)
            error(get_recoders_byext.url)
            error(get_recoders_byext.request.body)
            error(get_recoders_byext.text)
            raise e
        time.sleep(1)
        #根据企业查询录制文件_时间段
        info(u'根据企业查询录制文件_时间段')
        url_get_recoders_byext = 'https://'+ self.ip+ conf_get_recoders_byext['uri'] + '?enterpriseId=' + self.enterpriseId +'&startTime=' + str(startTime) + '&endTime=' + str(endTime)
        get_recoders_byext = requests_sig(conf_get_recoders_byext['method'], url_get_recoders_byext,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders_byext.status_code, 200, msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext.text,'"meetingRoomNumber":"'+cloudroom1+'"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext.text,'"vodMetadataType":"SERVER_RECORD"',msg=u'根据企业查询录制文件_时间段')
            self.assertRegexpMatches(get_recoders_byext.text,str(vodId),msg=u'根据企业查询录制文件_时间段')
        except Exception, e:
            error(e)
            error(get_recoders_byext.url)
            error(get_recoders_byext.request.body)
            error(get_recoders_byext.text)
            raise e
        time.sleep(1)
        #根据vodId获取缩略图
        info(u'根据vodId获取缩略图')
        url_get_thumbnail = ('https://'+ self.ip+ conf_get_thumbnail['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_thumbnail = requests_sig(conf_get_thumbnail['method'], url_get_thumbnail,'',self.token, verify=False)
        try:
            self.assertEqual(get_thumbnail.status_code, 200, msg=u'根据vodId获取缩略图')
        except Exception, e:
            error(e)
            error(get_thumbnail.url)
            error(get_thumbnail.request.body)
            error(get_thumbnail.text)
            raise e
        time.sleep(1)
        #根据vodId获取播放链接
        info(u'根据vodId获取播放链接')
        url_get_sharedInfo = ('https://'+ self.ip+ conf_get_sharedInfo['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_sharedInfo = requests_sig(conf_get_sharedInfo['method'], url_get_sharedInfo,'',self.token, verify=False)
        try:
            self.assertEqual(get_sharedInfo.status_code, 200, msg=u'根据vodId获取播放链接')
            self.assertRegexpMatches(get_sharedInfo.text,'"shared":false',msg=u'根据vodId获取播放链接')
            self.assertRegexpMatches(get_sharedInfo.text,'"playUrl":"http.*',msg=u'根据vodId获取播放链接')
        except Exception, e:
            error(e)
            error(get_sharedInfo.url)
            error(get_sharedInfo.request.body)
            error(get_sharedInfo.text)
            raise e
        time.sleep(1)
        #根据vodId获取下载链接
        info(u'根据vodId获取下载链接')
        url_get_downloadurl = ('https://'+ self.ip+ conf_get_downloadurl['uri'] + '?enterpriseId=' + self.enterpriseId ) % vodId
        get_downloadurl = requests_sig(conf_get_downloadurl['method'], url_get_downloadurl,'',self.token, verify=False)
        try:
            self.assertEqual(get_downloadurl.status_code, 200, msg=u'根据vodId获取下载链接')
            self.assertRegexpMatches(get_downloadurl.text,'"status":777000',msg=u'根据vodId获取播放链接')
            self.assertRegexpMatches(get_downloadurl.text,'"downloadUrl":"http.*',msg=u'根据vodId获取播放链接')
            info(get_downloadurl.text)
        except Exception, e:
            error(e)
            error(get_downloadurl.url)
            error(get_downloadurl.request.body)
            error(get_downloadurl.text)
            raise e
        time.sleep(1)
        #按云会议号删除视频
        info(u'按云会议号删除视频')
        url_del_recoders = ('https://'+ self.ip+ conf_del_recoders['uri'] + '?enterpriseId=' + self.enterpriseId ) % cloudroom1
        del_recoders = requests_sig(conf_del_recoders['method'], url_del_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(del_recoders.status_code, 200, msg=u'按云会议号删除视频')
        except Exception, e:
            error(e)
            error(del_recoders.url)
            error(del_recoders.request.body)
            error(del_recoders.text)
            raise e
        time.sleep(1)
        #根据云会议室查询录制文件_验证删除
        info(u'根据云会议室查询录制文件_验证删除')
        url_get_recoders = ('https://'+ self.ip+ conf_get_recoders_byroom['uri'] + '?enterpriseId=' + self.enterpriseId) % cloudroom1
        get_recoders = requests_sig(conf_get_recoders_byroom['method'], url_get_recoders,'',self.token, verify=False)
        try:
            self.assertEqual(get_recoders.status_code, 200, msg=u'根据云会议室查询录制文件_验证删除')
            self.assertEqual(get_recoders.text, '[]', msg=u'根据云会议室查询录制文件_验证删除')

        except Exception, e:
            error(e)
            error(get_recoders.url)
            error(get_recoders.request.body)
            error(get_recoders.text)
            raise e
        time.sleep(1)

if __name__ == '__main__':
    info(' start')


    unittest.main()
