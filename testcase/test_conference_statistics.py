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
conf_conferenceControl_currentMeeting = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/currentMeeting'}
conf_conferenceControl_currentMeeting_detail = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/currentMeeting/detail'}
conf_meeting_enterprise = {'method': 'GET','uri': '/api/rest/external/v1/meeting/statistic/enterprise'}
conf_meeting_participant = {'method': 'GET','uri': '/api/rest/external/v1/meeting/statistic/participant'}
conf_currentMeeting_confnumber_detail = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/currentMeeting/%s/detail'}
conf_currentMeeting_confnumber = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/conference/currentMeeting?conferenceNumber='}
conf_invitation = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/invitation'}
conf_start_recoding = {'method': 'GET','uri': '/api/rest/external/v1/meeting/recording/%s/start'}
conf_meetingStatus = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/%s/meetingStatus'}
conf_stop_recoding = {'method': 'GET','uri': '/api/rest/external/v1/meeting/recording/%s/stop'}
conf_stop_meeting = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}
conf_get_recoders = {'method': 'GET','uri': '/api/rest/external/v1/meetingroom/%s/vods'}
conf_del_recoder = {'method': 'DELETE','uri': '/api/rest/external/v1/vods/%s'}


class meeting_statistic(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.cloudroom1_number = json.loads(allconf['enterprise']['cloudroom1'])['meetingNumber']
        self.NE60number = json.loads(allconf['enterprise']['ne60'])['number']
        self.NE60number_id = json.loads(allconf['enterprise']['ne60'])['deviceId']
        self.startTime = int(time.time())*1000
        self.endTime = (int(time.time())+40)*1000
        #开始会议
        url_invitation = 'https://'+ self.ip+ conf_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": self.cloudroom1_number,"deviceList":[{"number":self.NE60number}]}
        invitation = requests_sig(conf_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        if invitation.status_code == 200:
            info(u'开始会议成功')
        else:
            error(u'开始会议失败')
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise Exception(u"开始会议失败")
        time.sleep(2)
        #开始录制
        url_start_recoding = ('https://'+ self.ip+ conf_start_recoding['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        start_recoding = requests_sig(conf_start_recoding['method'], url_start_recoding,'',self.token, verify=False)
        if start_recoding.status_code == 200:
            info(u'开始录制成功')
        else:
            error(u'开始录制失败')
            error(start_recoding.url)
            error(start_recoding.request.body)
            error(start_recoding.text)
            raise Exception(u"开始录制失败")
        time.sleep(5)



    @classmethod
    def tearDownClass(self):
        #结束会议
        url_stop_meeting = ('https://'+ self.ip+ conf_stop_meeting['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        stop_meeting = requests_sig(conf_stop_meeting['method'], url_stop_meeting,'',self.token, verify=False)
        if stop_meeting.status_code == 200:
            info(u'结束会议成功')
        else:
            error(u'结束会议失败')
            error(stop_meeting.url)
            error(stop_meeting.request.body)
            error(stop_meeting.text)

    def test_que_currentMeeting(self):
        #查询录制状态
        info(u'查询录制状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        meetingStatus = requests_sig(conf_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询录制状态')
            self.assertRegexpMatches(meetingStatus.text, '"recordingDevice":{"id":0,"type":0,"participantId":null,"externalUserId":null,"participantNumber":"'+self.cloudroom1_number+'"}', msg=u'查询录制状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        time.sleep(5)
        #查询当前会议
        info(u'查询当前会议')
        url_currentMeeting = 'https://'+ self.ip+ conf_conferenceControl_currentMeeting['uri'] + '?enterpriseId=' + self.enterpriseId
        currentMeeting = requests_sig(conf_conferenceControl_currentMeeting['method'], url_currentMeeting,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting.status_code, 200, msg=u'查询当前会议')
            self.assertRegexpMatches(currentMeeting.text, '"recording":true', msg=u'查询当前会议')
            self.assertRegexpMatches(currentMeeting.text, '"participantCount":1', msg=u'查询当前会议')
            self.assertRegexpMatches(currentMeeting.text, self.cloudroom1_number, msg=u'查询当前会议')
        except Exception, e:
            error(e)
            error(currentMeeting.url)
            error(currentMeeting.request.body)
            error(currentMeeting.text)
            raise e
        time.sleep(1)
        # 查询当前会议详情
        info(u'查询当前会议详情_质量')
        time.sleep(5)
        url_currentMeeting_detail = 'https://'+ self.ip+ conf_conferenceControl_currentMeeting_detail['uri'] + '?enterpriseId=' + self.enterpriseId + '&needQuality=true'
        currentMeeting_detai = requests_sig(conf_conferenceControl_currentMeeting_detail['method'], url_currentMeeting_detail,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting_detai.status_code, 200, msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_detai.text, '"recording":true', msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_detai.text, '"recordStartTime":\d+,', msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_detai.text, self.cloudroom1_number, msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_detai.text, '"score":\d+,', msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_detai.text, '"audioScore":\d+,', msg=u'查询当前会议_质量')
        except Exception, e:
            error(e)
            error(currentMeeting_detai.url)
            error(currentMeeting_detai.request.body)
            error(currentMeeting_detai.text)
            raise e
        time.sleep(1)
        # 查询当前会议详情_无质量
        info(u'查询当前会议详情_无质量')
        url_currentMeeting_detail2 = 'https://'+ self.ip+ conf_conferenceControl_currentMeeting_detail['uri'] + '?enterpriseId=' + self.enterpriseId
        currentMeeting_detai2 = requests_sig(conf_conferenceControl_currentMeeting_detail['method'], url_currentMeeting_detail2,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting_detai2.status_code, 200, msg=u'查询当前会议_无质量')
            self.assertRegexpMatches(currentMeeting_detai2.text, '"recording":true', msg=u'查询当前会议_无质量')
            self.assertRegexpMatches(currentMeeting_detai2.text, '"recordStartTime":\d+,', msg=u'查询当前会议_无质量')
            self.assertRegexpMatches(currentMeeting_detai2.text, self.cloudroom1_number, msg=u'查询当前会议_无质量')
            self.assertRegexpMatches(currentMeeting_detai2.text, '"quality":null}],"quality":null}]', msg=u'查询当前会议_无质量')

        except Exception, e:
            error(e)
            error(currentMeeting_detai2.url)
            error(currentMeeting_detai2.request.body)
            error(currentMeeting_detai2.text)
            raise e
        time.sleep(1)
        # 查询当前会议_指定会议室
        info(u'查询当前会议详情__指定会议室')
        url_currentMeeting_confnumber_detail = ('https://'+ self.ip+ conf_currentMeeting_confnumber_detail['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        currentMeeting_confnumber_detail = requests_sig(conf_currentMeeting_confnumber_detail['method'], url_currentMeeting_confnumber_detail,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting_confnumber_detail.status_code, 200, msg=u'查询当前会议详情__指定会议室')
            self.assertEqual(currentMeeting_confnumber_detail.status_code, 200, msg=u'查询当前会议详情__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber_detail.text, '"recording":true', msg=u'查询当前会议详情__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber_detail.text, '"recordStartTime":\d+,', msg=u'查询当前会议详情__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber_detail.text, self.cloudroom1_number, msg=u'查询当前会议详情__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber_detail.text, '"quality":null}],"quality":null}', msg=u'查询当前会议详情__指定会议室')
        except Exception, e:
            error(e)
            error(currentMeeting_confnumber_detail.url)
            error(currentMeeting_confnumber_detail.request.body)
            error(currentMeeting_confnumber_detail.text)
            raise e
        time.sleep(1)
        # 查询当前会议_指定会议室_质量
        info(u'查询当前会议详情_指定会议室_质量')
        url_currentMeeting_confnumber_detail = ('https://'+ self.ip+ conf_currentMeeting_confnumber_detail['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number + '&needQuality=true'
        currentMeeting_confnumber_detail2 = requests_sig(conf_currentMeeting_confnumber_detail['method'], url_currentMeeting_confnumber_detail,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting_confnumber_detail2.status_code, 200, msg=u'查询当前会议详情_指定会议室_质量')
            self.assertEqual(currentMeeting_confnumber_detail2.status_code, 200, msg=u'查询当前会议详情_指定会议室_质量')
            self.assertRegexpMatches(currentMeeting_confnumber_detail2.text, '"recording":true', msg=u'查询当前会议详情_指定会议室_质量')
            self.assertRegexpMatches(currentMeeting_confnumber_detail2.text, '"recordStartTime":\d+,', msg=u'查询当前会议详情_指定会议室_质量')
            self.assertRegexpMatches(currentMeeting_confnumber_detail2.text, self.cloudroom1_number, msg=u'查询当前会议详情_指定会议室_质量')
            self.assertRegexpMatches(currentMeeting_confnumber_detail2.text, '"score":\d+,', msg=u'查询当前会议_质量')
            self.assertRegexpMatches(currentMeeting_confnumber_detail2.text, '"audioScore":\d+,', msg=u'查询当前会议_质量')
        except Exception, e:
            error(e)
            error(currentMeeting_confnumber_detail2.url)
            error(currentMeeting_confnumber_detail2.request.body)
            error(currentMeeting_confnumber_detail2.text)
            raise e
        time.sleep(1)
        # 查询当前会议_指定会议室
        info(u'查询当前会议__指定会议室')
        url_currentMeeting_confnumber = 'https://'+ self.ip+ conf_currentMeeting_confnumber['uri'] +self.cloudroom1_number + '&enterpriseId=' + self.enterpriseId
        currentMeeting_confnumber = requests_sig(conf_currentMeeting_confnumber['method'], url_currentMeeting_confnumber,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting_confnumber.status_code, 200, msg=u'查询当前会议__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber.text, '"recording":true', msg=u'查询当前会议__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber.text, '"recordStartTime":\d+', msg=u'查询当前会议__指定会议室')
            self.assertRegexpMatches(currentMeeting_confnumber.text, self.cloudroom1_number, msg=u'查询当前会议__指定会议室')
        except Exception, e:
            error(e)
            error(currentMeeting_confnumber.url)
            error(currentMeeting_confnumber.request.body)
            error(currentMeeting_confnumber.text)
            raise e
        time.sleep(1)
        #停止录制
        url_stop_recoding = ('https://'+ self.ip+ conf_stop_recoding['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        stop_recoding = requests_sig(conf_stop_recoding['method'], url_stop_recoding,'',self.token, verify=False,headers=self.headers_json)
        if stop_recoding.status_code == 200:
            info(u'停止录制成功')
            info(stop_recoding.text)
        else:
            error(u'停止录制失败')
            error(stop_recoding.url)
            error(stop_recoding.request.body)
            error(stop_recoding.text)
        time.sleep(1)
        #结束会议
        url_stop_meeting = ('https://'+ self.ip+ conf_stop_meeting['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        stop_meeting = requests_sig(conf_stop_meeting['method'], url_stop_meeting,'',self.token, verify=False)
        if stop_meeting.status_code == 200:
            info(u'结束会议成功')
        else:
            error(u'结束会议失败')
            error(stop_meeting.url)
            error(stop_meeting.request.body)
            error(stop_meeting.text)
        time.sleep(5)
        self.endTime = int(time.time())*1000
        time.sleep(5)
        # 按会议时间导出会议详情
        info(u'按会议时间导出会议详情')
        url_meeting_enterprise = 'https://'+ self.ip+ conf_meeting_enterprise['uri'] + '?enterpriseId=' + self.enterpriseId + '&timeBegin=' + str(self.startTime) + '&timeEnd=' + str(self.endTime)
        meeting_enterprise = requests_sig(conf_meeting_enterprise['method'], url_meeting_enterprise,'',self.token, verify=False)
        try:
            self.assertEqual(meeting_enterprise.status_code, 200, msg=u'按会议时间导出会议详情')
            self.assertRegexpMatches(meeting_enterprise.text, '"callNumber":"'+self.cloudroom1_number+'"', msg=u'按会议时间导出会议详情')

        except Exception, e:
            error(e)
            error(meeting_enterprise.url)
            error(meeting_enterprise.request.body)
            error(meeting_enterprise.text)
            raise e
        time.sleep(1)
        # 按会议时间导出会议详情
        info(u'按会议时间导出会议详情')
        url_meeting_participant = 'https://'+ self.ip+ conf_meeting_participant['uri'] + '?enterpriseId=' + self.enterpriseId + '&timeBegin=' + str(self.startTime) + '&timeEnd=' + str(self.endTime)
        meeting_participant = requests_sig(conf_meeting_participant['method'], url_meeting_participant,'',self.token, verify=False)
        try:
            self.assertEqual(meeting_participant.status_code, 200, msg=u'按会议时间导出会议详情')
            self.assertRegexpMatches(meeting_participant.text, '"participantId":"'+self.NE60number_id+'"', msg=u'按会议时间导出会议详情')
            self.assertRegexpMatches(meeting_participant.text, '"meetingNumber":"'+self.cloudroom1_number+'"', msg=u'按会议时间导出会议详情')

            #self.assertRegexpMatches(meeting_participant.text, '"recordStartTime":\d+', msg=u'按会议时间导出会议详情')
            #self.assertRegexpMatches(meeting_participant.text, self.cloudroom1_number, msg=u'按会议时间导出会议详情')

        except Exception, e:
            error(e)
            error(meeting_participant.url)
            error(meeting_participant.request.body)
            error(meeting_participant.text)
            raise e
        time.sleep(1)



if __name__ == '__main__':
    info(' start')


    unittest.main()
