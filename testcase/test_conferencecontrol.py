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
conf_conferenceControl_meetingStatus = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/%s/meetingStatus'}
conf_conferenceControl_invitation = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/invitation'}
conf_conferenceControl_disconnect = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/disconnect'}
conf_conferenceControl_mainImage = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/mainImage'}
conf_conferenceControl_mute= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/mute'}
conf_conferenceControl_muteall= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/muteall'}
conf_conferenceControl_unmuteall= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/unmuteall'}
conf_conferenceControl_unmute= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/unmute'}
conf_conferenceControl_end= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/end'}
conf_conferenceControl_authShare= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/content/authShare'}
conf_conferenceControl_lock= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/lock'}
conf_conferenceControl_unlock= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/unlock'}
conf_conferenceControl_sendMsg= {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/sendMsg'}
conf_conferenceControl_startMultiImage= {'method': 'POST','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/startDeviceMultiImage'}
conf_conferenceControl_stopMultiImage= {'method': 'POST','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/stopDeviceMultiImage'}
conf_conferenceControl_subtitle= {'method': 'POST','uri': '/api/rest/external/v1/conferenceControl/%s/meeting/subtitle'}
conf_conferenceControl_meetingInfo= {'method': 'PUT','uri': '/api/rest/external/v1/meetingInfo/batch'}
conf_conferenceControl_currentMeeting = {'method': 'GET','uri': '/api/rest/external/v1/conferenceControl/conference/currentMeeting?conferenceNumber='}
conf_conferenceControl_meetingRoomInfo = {'method': 'GET','uri': '/api/rest/external/v1/meetingInfo/%s/meetingRoomInfo'}
conf_conferenceControl_hangup = {'method': 'PUT','uri': '/api/rest/external/v1/conferenceControl/nemo/%s/hangup'}


class conferenceControl(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
        self.cloudroom1_number = json.loads(allconf['enterprise']['cloudroom1'])['meetingNumber']
        self.NE60number = json.loads(allconf['enterprise']['ne60'])['number']
        self.NE60number_id = json.loads(allconf['enterprise']['ne60'])['deviceId']
        self.NE60number_type = json.loads(allconf['enterprise']['ne60'])['type']
        self.ME40number = json.loads(allconf['enterprise']['me40'])['number']
        self.ME40number_id = json.loads(allconf['enterprise']['me40'])['deviceId']
        self.ME40number_type = json.loads(allconf['enterprise']['me40'])['type']
        self.cloudroom2_number = json.loads(allconf['enterprise']['cloudroom2'])['meetingNumber']

    @classmethod
    def tearDownClass(self):
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        info(end.text)


    def test_conferenceControl_a(self):
        #邀请入会
        info(u'邀请入会')
        url_invitation = 'https://'+ self.ip+ conf_conferenceControl_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": self.cloudroom1_number,"deviceList":[{"number":self.NE60number}]}
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
        #全体禁言
        info(u'全体禁言')
        url_muteall = ('https://'+ self.ip+ conf_conferenceControl_muteall['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        muteall = requests_sig(conf_conferenceControl_muteall['method'], url_muteall,'',self.token, verify=False)
        try:
            self.assertEqual(muteall.status_code, 200, msg=u'全体禁言')
        except Exception, e:
            error(e)
            error(muteall.url)
            error(muteall.request.body)
            error(muteall.text)
            raise e
        time.sleep(1)
        #查询会议状态，check全体禁言
        info(u'查询会议状态，check全体禁言')

        meetingStatus2 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus2.status_code, 200, msg=u'check全体禁言')
            self.assertRegexpMatches(meetingStatus2.text,'"muteStatus":1,"device":{"id":'+self.NE60number_id,msg=u'check全体禁言')
        except Exception, e:
            error(e)
            error(meetingStatus2.url)
            error(meetingStatus2.request.body)
            error(meetingStatus2.text)
            raise e
        time.sleep(1)
        #全体解除禁言
        info(u'全体解除禁言')
        url_unmuteall = ('https://'+ self.ip+ conf_conferenceControl_unmuteall['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        unmuteall = requests_sig(conf_conferenceControl_unmuteall['method'], url_unmuteall,'',self.token, verify=False)
        try:
            self.assertEqual(unmuteall.status_code, 200, msg=u'全体解除禁言')
        except Exception, e:
            error(e)
            error(unmuteall.url)
            error(unmuteall.request.body)
            error(unmuteall.text)
            raise e
        time.sleep(1)
        #查询会议状态，check全体解除禁言
        info(u'查询会议状态，check全体解除禁言')

        meetingStatus3 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus3.status_code, 200, msg=u'查询会议状态，全体解除禁言')
            self.assertRegexpMatches(meetingStatus3.text,'"muteStatus":0,"device":{"id":'+self.NE60number_id,msg=u'查询会议状态,全体解除禁言')

        except Exception, e:
            error(e)
            error(meetingStatus3.url)
            error(meetingStatus3.request.body)
            error(meetingStatus3.text)
            raise e
        time.sleep(1)
        #设置主画面
        info(u'设置主画面')
        url_mainImage = ('https://'+ self.ip+ conf_conferenceControl_mainImage['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"id":self.NE60number_id,"type":self.NE60number_type}
        mainImage = requests_sig(conf_conferenceControl_mainImage['method'], url_mainImage,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(mainImage.status_code, 200, msg=u'设置主画面')
        except Exception, e:
            error(e)
            error(mainImage.url)
            error(mainImage.request.body)
            error(mainImage.text)
            raise e
        time.sleep(1)

        #查询会议状态，check主画面
        info(u'查询会议状态，check主画面')
        meetingStatus4 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus4.status_code, 200, msg=u'查询会议状态，主画面')
            self.assertRegexpMatches(meetingStatus4.text,'"mainImage":{"id":'+self.NE60number_id,msg=u'查询会议状态，主画面')
        except Exception, e:
            error(e)
            error(meetingStatus4.url)
            error(meetingStatus4.request.body)
            error(meetingStatus4.text)
            raise e
        time.sleep(1)

        #踢人
        info(u'踢人')
        url_disconnect = ('https://'+ self.ip+ conf_conferenceControl_disconnect['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = [{"id":self.NE60number_id,"type":self.NE60number_type}]
        disconnect = requests_sig(conf_conferenceControl_disconnect['method'], url_disconnect,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(disconnect.status_code, 200, msg=u'踢人')
        except Exception, e:
            error(e)
            error(disconnect.url)
            error(disconnect.request.body)
            error(disconnect.text)
            raise e
        time.sleep(1)
        #查询会议状态，踢人
        info(u'查询会议状态，踢人')
        meetingStatus5 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus5.status_code, 200, msg=u'查询会议状态，踢人')
            self.assertNotRegexpMatches(meetingStatus5.text,self.NE60number,msg=u'查询会议状态，踢人')

        except Exception, e:
            error(e)
            error(meetingStatus5.url)
            error(meetingStatus5.request.body)
            error(meetingStatus5.text)
            raise e
        time.sleep(1)

    def test_conferenceControl_b(self):

        #邀请入会
        info(u'邀请入会')
        url_invitation = 'https://'+ self.ip+ conf_conferenceControl_invitation['uri'] + '?enterpriseId=' + self.enterpriseId
        data = {"callNumber": self.cloudroom1_number,"deviceList":[{"number":self.NE60number},{"number":self.ME40number}]}
        invitation = requests_sig(conf_conferenceControl_invitation['method'], url_invitation,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(invitation.status_code, 200, msg=u'邀请入会')
        except Exception, e:
            error(e)
            error(invitation.url)
            error(invitation.request.body)
            error(invitation.text)
            raise e
        time.sleep(10)
        #查询会议状态
        info(u'查询会议状态')
        url_meetingStatus = ('https://'+ self.ip+ conf_conferenceControl_meetingStatus['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        meetingStatus = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus.status_code, 200, msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,self.ME40number,msg=u'查询会议状态')
            self.assertRegexpMatches(meetingStatus.text,self.NE60number,msg=u'查询会议状态')
        except Exception, e:
            error(e)
            error(meetingStatus.url)
            error(meetingStatus.request.body)
            error(meetingStatus.text)
            raise e
        time.sleep(1)
        #禁言
        info(u'禁言')
        url_mute = ('https://'+ self.ip+ conf_conferenceControl_mute['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = [{"id":self.NE60number_id,"type":self.NE60number_type}]
        mute = requests_sig(conf_conferenceControl_mute['method'], url_mute,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(mute.status_code, 200, msg=u'禁言')
        except Exception, e:
            error(e)
            error(mute.url)
            error(mute.request.body)
            error(mute.text)
            raise e
        time.sleep(1)
        #查询会议状态，check禁言
        meetingStatus2 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus2.status_code, 200, msg=u'查询会议状态,禁言')
            self.assertRegexpMatches(meetingStatus2.text,'"muteStatus":0,"device":{"id":'+self.ME40number_id,msg=u'查询会议状态,禁言')
            self.assertRegexpMatches(meetingStatus2.text,'"muteStatus":1,"device":{"id":'+self.NE60number_id,msg=u'查询会议状态,禁言')

        except Exception, e:
            error(e)
            error(meetingStatus2.url)
            error(meetingStatus2.request.body)
            error(meetingStatus2.text)
            raise e
        time.sleep(1)
        #解除禁言
        info(u'解除禁言')
        url_unmute = ('https://'+ self.ip+ conf_conferenceControl_unmute['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = [{"id":self.NE60number_id,"type":self.NE60number_type}]
        unmute = requests_sig(conf_conferenceControl_unmute['method'], url_unmute,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(unmute.status_code, 200, msg=u'解除禁言')
        except Exception, e:
            error(e)
            error(unmute.url)
            error(unmute.request.body)
            error(unmute.text)
            raise e
        time.sleep(1)
        #查询会议状态，check解除禁言
        info(u'查询会议状态，check解除禁言')
        meetingStatus3 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus3.status_code, 200, msg=u'查询会议状态，check解除禁言')
            self.assertRegexpMatches(meetingStatus3.text,'"muteStatus":0,"device":{"id":'+self.ME40number_id,msg=u'查询会议状态,check解除禁言')
            self.assertRegexpMatches(meetingStatus3.text,'"muteStatus":0,"device":{"id":'+self.NE60number_id,msg=u'查询会议状态,check解除禁言')
        except Exception, e:
            error(e)
            error(meetingStatus3.url)
            error(meetingStatus3.request.body)
            error(meetingStatus3.text)
            raise e
        time.sleep(1)
        #屏幕分享授权
        info(u'屏幕分享授权')
        url_authShare = ('https://'+ self.ip+ conf_conferenceControl_authShare['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"isAll": False,"device": {"id": self.NE60number_id,"type": self.NE60number_type}}

        authShare = requests_sig(conf_conferenceControl_authShare['method'], url_authShare,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(authShare.status_code, 200, msg=u'屏幕分享授权')
        except Exception, e:
            error(e)
            error(authShare.url)
            error(authShare.request.body)
            error(authShare.text)
            raise e
        time.sleep(1)
        #会议锁定
        info(u'会议锁定')
        url_lock = ('https://'+ self.ip+ conf_conferenceControl_lock['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        lock = requests_sig(conf_conferenceControl_lock['method'], url_lock,'',self.token, verify=False)
        try:
            self.assertEqual(lock.status_code, 200, msg=u'会议锁定')
        except Exception, e:
            error(e)
            error(lock.url)
            error(lock.request.body)
            error(lock.text)
            raise e
        time.sleep(1)
        #会议解锁
        info(u'会议解锁')
        url_unlock = ('https://'+ self.ip+ conf_conferenceControl_unlock['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        unlock = requests_sig(conf_conferenceControl_unlock['method'], url_unlock,'',self.token, verify=False)
        try:
            self.assertEqual(unlock.status_code, 200, msg=u'会议解锁')
        except Exception, e:
            error(e)
            error(unlock.url)
            error(unlock.request.body)
            error(unlock.text)
            raise e
        time.sleep(1)
        #发送会议通知
        info(u'发送会议通知')
        url_sendMsg = ('https://'+ self.ip+ conf_conferenceControl_sendMsg['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"devices": [{"id": self.NE60number_id,"type": self.NE60number_type}],"meetingSubtitle": {"content": "测试消息推送","location": "bottom","action": "push","scroll": "1"}}
        sendMsg = requests_sig(conf_conferenceControl_sendMsg['method'], url_sendMsg,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sendMsg.status_code, 200, msg=u'发送会议通知')
        except Exception, e:
            error(e)
            error(sendMsg.url)
            error(sendMsg.request.body)
            error(sendMsg.text)
            raise e
        time.sleep(5)
        #取消发送会议通知
        info(u'取消发送会议通知')
        url_sendMsg = ('https://'+ self.ip+ conf_conferenceControl_sendMsg['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"devices": [{"id": self.NE60number_id,"type": self.NE60number_type}],"meetingSubtitle": {"content": "aaaaa","location": "bottom","action": "cancel","scroll": "1"}}

        sendMsg2 = requests_sig(conf_conferenceControl_sendMsg['method'], url_sendMsg,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(sendMsg2.status_code, 200, msg=u'取消发送会议通知')
        except Exception, e:
            error(e)
            error(sendMsg2.url)
            error(sendMsg2.request.body)
            error(sendMsg2.text)
            raise e
        time.sleep(5)
        #向终端发送字幕
        info(u'向终端发送字幕')
        url_subtitle = ('https://'+ self.ip+ conf_conferenceControl_subtitle['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"content":"时Aa","targets":[{"deviceId":self.ME40number_id,"deviceType":self.ME40number_type}]}

        subtitle= requests_sig(conf_conferenceControl_subtitle['method'], url_subtitle,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(subtitle.status_code, 200, msg=u'向终端发送字幕')
        except Exception, e:
            error(e)
            error(subtitle.url)
            error(subtitle.request.body)
            error(subtitle.text)
            raise e
        time.sleep(5)
        #开始多画面配置ME40
        info(u'开始多画面配置')
        url_startMultiImage = ('https://'+ self.ip+ conf_conferenceControl_startMultiImage['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {
	"deviceId": self.ME40number_id,
	"type": self.ME40number_type,
	"broadcast": False,
	"mlayout": {
	"mode": "2-1"}

}

        startMultiImage= requests_sig(conf_conferenceControl_startMultiImage['method'], url_startMultiImage,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(startMultiImage.status_code, 200, msg=u'开始多画面配置')
        except Exception, e:
            error(e)
            error(startMultiImage.url)
            error(startMultiImage.request.body)
            error(startMultiImage.text)
            raise e
        time.sleep(1)

        #停止多画面配置ME40
        info(u'停止多画面配置')
        url_stopMultiImage = ('https://'+ self.ip+ conf_conferenceControl_stopMultiImage['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number
        data = {"deviceId":self.ME40number_id,"type":self.ME40number_type}
        stopMultiImage= requests_sig(conf_conferenceControl_stopMultiImage['method'], url_stopMultiImage,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(stopMultiImage.status_code, 200, msg=u'停止多画面配置')
        except Exception, e:
            error(e)
            error(stopMultiImage.url)
            error(stopMultiImage.request.body)
            error(stopMultiImage.text)
            raise e
        time.sleep(1)
        #批量查询云会议室号
        info(u'批量查询云会议室号')
        url_meetingInfo = 'https://'+ self.ip+ conf_conferenceControl_meetingInfo['uri'] + '?enterpriseId=' + self.enterpriseId
        data = [self.cloudroom1_number,self.cloudroom2_number]
        meetingInfo = requests_sig(conf_conferenceControl_meetingInfo['method'], url_meetingInfo,data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(meetingInfo.status_code, 200, msg=u'批量查询云会议室号')
            #self.assertRegexpMatches(meetingInfo.text,'"meetingRoomNumber":"'+self.cloudroom1_number+'","meetingRoomState":"incall"',msg=u'批量查询企业云会议室')
            #self.assertRegexpMatches(meetingInfo.text,'"meetingRoomNumber":"'+self.cloudroom2_number+'","meetingRoomState":"idle"',msg=u'批量查询企业云会议室')
            info(meetingInfo.text)
        except Exception, e:
            error(e)
            error(meetingInfo.url)
            error(meetingInfo.request.body)
            error(meetingInfo.text)
            raise e
        time.sleep(1)
        #根据云会议号查询企业的当前会议
        info(u'根据云会议号查询企业的当前会议')
        url_currentMeeting = 'https://'+ self.ip+ conf_conferenceControl_currentMeeting['uri'] + self.cloudroom1_number + '&enterpriseId=' + self.enterpriseId
        currentMeeting = requests_sig(conf_conferenceControl_currentMeeting['method'], url_currentMeeting,'',self.token, verify=False)
        try:
            self.assertEqual(currentMeeting.status_code, 200, msg=u'根据云会议号查询企业的当前会议')
            self.assertRegexpMatches(currentMeeting.text,'"participantCount":2',msg=u'根据云会议号查询企业的当前会议')
            self.assertRegexpMatches(currentMeeting.text,'"meetingRoomNumber":"'+self.cloudroom1_number,msg=u'根据云会议号查询企业的当前会议')

        except Exception, e:
            error(e)
            error(currentMeeting.url)
            error(currentMeeting.request.body)
            error(currentMeeting.text)
            raise e
        time.sleep(1)
        #按企业ID查询会议信息
        info(u'按企业ID查询会议信息')
        url_meetingRoomInfo = ('https://' + self.ip + conf_conferenceControl_meetingRoomInfo['uri'] + '?enterpriseId=' + self.enterpriseId) % self.enterpriseId
        meetingRoomInfo = requests_sig(conf_conferenceControl_meetingRoomInfo['method'], url_meetingRoomInfo,'',self.token, verify=False)
        try:
            self.assertEqual(meetingRoomInfo.status_code, 200, msg=u'按企业ID查询会议信息')
            self.assertRegexpMatches(meetingRoomInfo.text,'"meettingRoomName":"test_.*"',msg=u'根据云会议号查询企业的当前会议')

        except Exception, e:
            error(e)
            error(meetingRoomInfo.url)
            error(meetingRoomInfo.request.body)
            error(meetingRoomInfo.text)
            raise e
        time.sleep(1)
        #挂断
        info(u'挂断')
        url_hangup = ('https://' + self.ip + conf_conferenceControl_hangup['uri'] + '?enterpriseId=' + self.enterpriseId) % self.ME40number
        hangup = requests_sig(conf_conferenceControl_hangup['method'], url_hangup,'',self.token, verify=False)
        try:
            self.assertEqual(hangup.status_code, 200, msg=u'挂断')
        except Exception, e:
            error(e)
            error(hangup.url)
            error(hangup.request.body)
            error(hangup.text)
            raise e
        time.sleep(5)
        #查询会议状态，check挂断
        meetingStatus4 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus4.status_code, 200, msg=u'查询会议状态，check挂断')
            self.assertNotRegexpMatches(meetingStatus4.text,self.ME40number,msg=u'查询会议状态，check挂断')
            self.assertRegexpMatches(meetingStatus4.text,self.NE60number,msg=u'查询会议状态，check挂断')
        except Exception, e:
            error(e)
            error(meetingStatus4.url)
            error(meetingStatus4.request.body)
            error(meetingStatus4.text)
            raise e
        time.sleep(1)
        #结束会议
        info(u'结束会议')
        url_end = ('https://' + self.ip + conf_conferenceControl_end['uri'] + '?enterpriseId=' + self.enterpriseId) % self.cloudroom1_number

        end = requests_sig(conf_conferenceControl_end['method'], url_end,'',self.token, verify=False)
        try:
            self.assertEqual(end.status_code, 200, msg=u'结束会议')
        except Exception, e:
            error(e)
            error(end.url)
            error(end.request.body)
            error(end.text)
            raise e
        time.sleep(1)
        #查询会议状态，check结束会议
        info(u'查询会议状态，check结束会议')

        meetingStatus5 = requests_sig(conf_conferenceControl_meetingStatus['method'], url_meetingStatus,'',self.token, verify=False)
        try:
            self.assertEqual(meetingStatus5.status_code, 200, msg=u'查询会议状态，check结束会议')
            self.assertRegexpMatches(meetingStatus5.text,'"deviceStatusList":\[\]',msg=u'查询会议状态，check结束会议')

        except Exception, e:
            error(e)
            error(meetingStatus5.url)
            error(meetingStatus5.request.body)
            error(meetingStatus5.text)
            raise e
        time.sleep(1)

if __name__ == '__main__':
    info(' start')


    unittest.main()
