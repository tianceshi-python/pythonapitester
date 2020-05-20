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

#接口配置（配置与测试数据分离）。接口配在这里，数据从excel获取。这里配置对应 http://123.57.12.62/meeting/rest-api-create-conf/中的 1-8
conf_create_meeting_v1 = {'method': 'GET','uri': '/api/rest/external/v1/create_meeting'}
conf_get_meeting_info_by_roomno = {'method': 'GET','uri': '/api/rest/external/v1/meetingInfo/%s'}
conf_modify_meeting_info_by_roomno = {'method': 'PUT','uri': '/api/rest/external/v1/meetingInfo/%s'}
conf_delete_meeting_info_by_roomno = {'method': 'DELETE','uri': '/api/rest/external/v1/meetingInfo/%s'}
conf_get_room_list_by_type = {'method': 'GET','uri': '/api/rest/external/v1/conference/cloudConference'}
conf_create_meeting_v2 = {'method': 'POST','uri': '/api/rest/external/v2/create_meeting'}
conf_get_room_batch = {'method': 'PUT','uri': '/api/rest/external/v1/meetingInfo/batch'}
conf_get_sdkroom_list_by_ext = {'method': 'GET','uri': '/api/rest/external/v1/meetingInfo/%s/meetingRoomInfo'}


class create_meeting_v1(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.enterpriseId = allconf['enterprise']['enterpriseid']
        self.ip = allconf['enterprise']['sdk_ip']
        self.token = str(allconf['enterprise']['token'])
        self.headers_json = {'content-type': 'application/json'}
    @staticmethod
    def getTestFunc(testdata):
        def func(self):
            self.basecase(testdata)
        return func
    @staticmethod
    def getTestFunc_v2(testdata):
        def func(self):
            self.basecase_creatv2(testdata)
        return func
    def basecase(self,casedata):
        #创建会议v1，改，查，删
        start_time = (int(time.time())+600)*1000
        end_time = start_time + 1200000
        end_time2 = end_time + 100000
        params = casedata['params'] % ('start_time','end_time')
        #老方法，解析conf文件 #备份
        #params = dict(cf.items("case1"))['params'] % ('start_time','end_time','self.enterpriseId')
        url_creat_v1 = 'https://'+ self.ip+ conf_create_meeting_v1['uri'] + '?enterprise_id=' + self.enterpriseId + '&' + urllib.urlencode(eval(params))
        #创建会议
        info(u'创建会议v1')
        creat_v1 = requests_sig(conf_create_meeting_v1['method'], url_creat_v1, casedata['data'],self.token, verify=False)
        #断言response code
        if casedata.has_key('assert_code') and (casedata['assert_code'] != ''):
            try:
                self.assertEqual(creat_v1.status_code, casedata['assert_code'],msg=u'创建会议v1')
            except Exception, e:
                error(e)
                error(creat_v1.url)
                error(creat_v1.request.body)
                error(creat_v1.text)
                raise e
        # 正则断言response text
        if casedata.has_key('assert_tex_reg') and (casedata['assert_tex_reg'] != ''):
            regtextall = casedata['assert_tex_reg'].split(',,,')
            for regtext in regtextall:
                try:
                    self.assertRegexpMatches(creat_v1.text, regtext, msg=u'创建')
                    info('check ok:      '+regtext)
                except Exception, e:
                    error(e)
                    error(creat_v1.url)
                    error(creat_v1.request.body)
                    error(creat_v1.text)
                    raise e
        #json断言 预留
        if casedata.has_key('assert_json') and (casedata['assert_json'] != ''):
            #d1 = jsonpath.jsonpath(get_room_batch.json(),expr='$..?(@.autoRecord==False).meettingRoomName')
            pass
        time.sleep(1)
        #查询会议
        info(u'查询会议')
        room_no = creat_v1.json()['meetingNumber']
        url_get_meeting_info_by_roomno = ('https://' + self.ip + conf_get_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        get_meeting_info_by_roomno = requests_sig(conf_get_meeting_info_by_roomno['method'], url_get_meeting_info_by_roomno, '',self.token, verify=False)
        if casedata.has_key('assert_tex_reg_que') and (casedata['assert_tex_reg_que'] != ''):
            regtextqueall = casedata['assert_tex_reg_que'].split(',,,')
            for regtext in regtextqueall:
                try:
                    self.assertRegexpMatches(get_meeting_info_by_roomno.text, regtext, msg=u'查询会议')
                except Exception, e:
                    error(e)
                    error(creat_v1.url)
                    error(creat_v1.request.body)
                    error(creat_v1.text)
                    raise e
        time.sleep(1)
        #修改会议
        info(u'修改会议')

        url_modify_meeting_info_by_roomno = ('https://' + self.ip + conf_modify_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        data = {
                "meettingRoomName": "测试修改",
                "meetingRoomState": "idle",
                "autoMute":"2",
                "smartMutePerson": 3,
                "autoRecord": True,
                "expireTime":end_time2,
                "password":"123456",
                "meetingControlPwd":"654321",
                "recordAddDeviceName":True,
                "onlyRecordMainImage":True
                }

        modify_meeting_info_by_roomno = requests_sig(conf_modify_meeting_info_by_roomno['method'], url_modify_meeting_info_by_roomno, data,self.token, verify=False,headers=self.headers_json)
        try:
            self.assertEqual(modify_meeting_info_by_roomno.status_code, 200, msg=u'修改会议')
        except Exception, e:
            error(e)
            error(modify_meeting_info_by_roomno.url)
            error(modify_meeting_info_by_roomno.request.body)
            error(modify_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)
        #修改后查询会议
        info(u'修改后查询会议')
        url_get_meeting_info_by_roomno = ('https://' + self.ip + conf_get_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        get_meeting_info_by_roomno = requests_sig(conf_get_meeting_info_by_roomno['method'], url_get_meeting_info_by_roomno, '',self.token, verify=False)
        try:
            self.assertEqual(get_meeting_info_by_roomno.status_code, 200, msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, room_no, msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, '"meetingRoomState":"idle"', msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, '"autoMute":2', msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, '"autoRecord":true', msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, '"recordAddDeviceName":true', msg=u'修改后查询会议')
            self.assertRegexpMatches(get_meeting_info_by_roomno.text, '"onlyRecordMainImage":true', msg=u'修改后查询会议')
        except Exception, e:
            error(e)
            error(get_meeting_info_by_roomno.url)
            error(get_meeting_info_by_roomno.request.body)
            error(get_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)
        #删除会议室
        info(u'删除会议')

        url_delete_meeting_info_by_roomno = ('https://' + self.ip + conf_delete_meeting_info_by_roomno[
            'uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        delete_meeting_info_by_roomno = requests_sig(conf_delete_meeting_info_by_roomno['method'],url_delete_meeting_info_by_roomno, '', self.token, verify=False)
        try:
            self.assertEqual(delete_meeting_info_by_roomno.status_code, 200, msg=u'删除会议')
        except Exception, e:
            error(e)
            error(modify_meeting_info_by_roomno.url)
            error(modify_meeting_info_by_roomno.request.body)
            error(modify_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)
        #删除后查询会议
        info(u'删除后查询会议')

        url_get_meeting_info_by_roomno = ('https://' + self.ip + conf_get_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        get_meeting_info_by_roomno = requests_sig(conf_get_meeting_info_by_roomno['method'], url_get_meeting_info_by_roomno, '',self.token, verify=False)
        try:
            self.assertEqual(get_meeting_info_by_roomno.status_code, 204, msg=u'删除后查询会议')
            #self.assertRegexpMatches(get_meeting_info_by_roomno.text, 'invalid cloud meeting number', msg='删除后查询')
        except Exception, e:
            error(e)
            error(get_meeting_info_by_roomno.url)
            error(get_meeting_info_by_roomno.request.body)
            error(get_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)

    def test_get_room_list(self):
        cloudroom1 = eval(allconf['enterprise']['cloudroom1'])
        cloudroom2 = eval(allconf['enterprise']['cloudroom2'])
        #查询企业云会议室
        info(u'查询企业云会议室')
        url_get_room_list_by_type = 'https://' + self.ip + conf_get_room_list_by_type['uri'] + '?enterpriseId=' + self.enterpriseId + '&page=1&size=20&type=ENTERPRISE_CONFERENCE'
        get_room_list_by_type = requests_sig(conf_get_room_list_by_type['method'], url_get_room_list_by_type, '',self.token, verify=False)
        try:
            self.assertEqual(get_room_list_by_type.status_code, 200, msg=u'查询企业云会议室')
            self.assertRegexpMatches(get_room_list_by_type.text, ('"meetingNumber":"%s","displayName":"%s"') % (cloudroom1["meetingNumber"],cloudroom1["displayName"].decode('UTF-8')), msg=u'查询企业云会议室')
            self.assertRegexpMatches(get_room_list_by_type.text, ('"meetingNumber":"%s","displayName":"%s"') % (cloudroom2["meetingNumber"],cloudroom2["displayName"].decode('UTF-8')), msg=u'查询企业云会议室')

        except Exception, e:
            error(e)
            error(get_room_list_by_type.url)
            error(get_room_list_by_type.request.body)
            error(get_room_list_by_type.text)
            raise e
        time.sleep(1)

        #查询sdk会议室
        info(u'查询sdk会议室')
        url_get_room_list_by_typesdk = 'https://' + self.ip + conf_get_room_list_by_type['uri'] + '?enterpriseId=' + self.enterpriseId + '&page=1&size=20&type=SDK'
        get_room_list_by_typesdk = requests_sig(conf_get_room_list_by_type['method'], url_get_room_list_by_typesdk, '',self.token, verify=False)
        try:
            self.assertEqual(get_room_list_by_typesdk.status_code, 200, msg=u'查询sdk会议室')
            self.assertRegexpMatches(get_room_list_by_typesdk.text, 'test_', msg=u'查询sdk会议室')

        except Exception, e:
            error(e)
            error(get_room_list_by_typesdk.url)
            error(get_room_list_by_typesdk.request.body)
            error(get_room_list_by_typesdk.text)
            raise e
        time.sleep(1)

    def test_batch_get_room(self):
        cloudroom1 = eval(allconf['enterprise']['cloudroom1'])
        cloudroom2 = eval(allconf['enterprise']['cloudroom2'])
        data = [cloudroom1["meetingNumber"],cloudroom2["meetingNumber"]]
        #查询企业云会议室
        info(u'批量查询企业云会议室')

        url_get_room_batch = 'https://' + self.ip + conf_get_room_batch['uri'] + '?enterpriseId=' + self.enterpriseId
        get_room_batch = requests_sig(conf_get_room_batch['method'], url_get_room_batch, data,self.token, verify=False,headers=self.headers_json)

        try:
            self.assertEqual(get_room_batch.status_code, 200, msg=u'批量查询企业云会议室')
            #self.assertRegexpMatches(get_room_batch.text,cloudroom1["meetingNumber"],msg=u'批量查询企业云会议室')
            #self.assertRegexpMatches(get_room_batch.text,cloudroom2["meetingNumber"],msg=u'批量查询企业云会议室')
            info(get_room_batch.text)
        except Exception, e:
            error(e)
            error(get_room_batch.url)
            error(get_room_batch.request.body)
            error(get_room_batch.text)
            raise e
        time.sleep(1)

    def test_get_sdkroom_list(self):
        #查询企业sdk会议室
        info(u'查询企业sdk会议室')
        url_get_sdkroom_list = 'https://' + self.ip + (conf_get_sdkroom_list_by_ext['uri']) % self.enterpriseId + '?enterpriseId=' + self.enterpriseId
        get_sdkroom_list = requests_sig(conf_get_sdkroom_list_by_ext['method'], url_get_sdkroom_list, "",self.token, verify=False)
        try:
            self.assertEqual(get_sdkroom_list.status_code, 200, msg=u'查询企业sdk会议室')
            self.assertRegexpMatches(get_sdkroom_list.text,'test_',msg=u'查询企业sdk会议室')
        except Exception, e:
            error(e)
            error(get_sdkroom_list.url)
            error(get_sdkroom_list.request.body)
            error(get_sdkroom_list.text)
            raise e
        time.sleep(1)
    def basecase_creatv2(self,casedata):
        #创建会议v1，改，查，删
        start_time = (int(time.time())+600)*1000
        end_time = start_time + 1200000
        end_time2 = end_time + 100000
        datas = eval(casedata['data'] % (start_time,end_time))
        #datas = {"autoMute": 0, "configs": {"autoRecord": True}, "controlPassword": "123456", "endTime": 1546348864000, "maxParticipant": 10, "meetingName": "creatv2", "requirePassword": False, "startTime": 1546347664000}
        url_creat_v2 = 'https://'+ self.ip+ conf_create_meeting_v2['uri'] + '?enterpriseId=' + self.enterpriseId
        #创建会议
        info(u'创建会议v2')
        creat_v2 = requests_sig(conf_create_meeting_v2['method'], url_creat_v2, datas,self.token, verify=False ,headers=self.headers_json)
        #断言response code
        if casedata.has_key('assert_code') and (casedata['assert_code'] != ''):
            try:
                self.assertEqual(creat_v2.status_code, casedata['assert_code'],msg=u'创建会议v2')
            except Exception, e:
                error(e)
                error(creat_v2.url)
                error(creat_v2.request.body)
                error(creat_v2.text)
                raise e
        # 正则断言response text
        if casedata.has_key('assert_tex_reg') and (casedata['assert_tex_reg'] != ''):
            regtextall = casedata['assert_tex_reg'].split(',,,')
            for regtext in regtextall:
                try:
                    self.assertRegexpMatches(creat_v2.text, regtext, msg=u'创建会议v2')
                    info('check ok:      '+regtext)
                except Exception, e:
                    error(e)
                    error(creat_v2.url)
                    error(creat_v2.request.body)
                    error(creat_v2.text)
                    raise e
        #json断言 预留
        if casedata.has_key('assert_json') and (casedata['assert_json'] != ''):
            #d1 = jsonpath.jsonpath(get_room_batch.json(),expr='$..?(@.autoRecord==False).meettingRoomName')
            pass
        time.sleep(1)
        #查询会议
        info(u'查询会议')
        room_no = creat_v2.json()['meetingNumber']
        url_get_meeting_info_by_roomno = ('https://' + self.ip + conf_get_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        get_meeting_info_by_roomno = requests_sig(conf_get_meeting_info_by_roomno['method'], url_get_meeting_info_by_roomno, '',self.token, verify=False)
        if casedata.has_key('assert_tex_reg_que') and (casedata['assert_tex_reg_que'] != ''):
            regtextqueall = casedata['assert_tex_reg_que'].split(',,,')
            for regtext in regtextqueall:
                try:
                    self.assertRegexpMatches(get_meeting_info_by_roomno.text, regtext, msg=u'查询会议')
                except Exception, e:
                    error(e)
                    error(get_meeting_info_by_roomno.url)
                    error(get_meeting_info_by_roomno.request.body)
                    error(get_meeting_info_by_roomno.text)
                    raise e
        time.sleep(1)
        #删除会议室
        info(u'删除会议室')

        url_delete_meeting_info_by_roomno = ('https://' + self.ip + conf_delete_meeting_info_by_roomno[
            'uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        delete_meeting_info_by_roomno = requests_sig(conf_delete_meeting_info_by_roomno['method'],url_delete_meeting_info_by_roomno, '', self.token, verify=False)
        try:
            self.assertEqual(delete_meeting_info_by_roomno.status_code, 200, msg=u'删除会议室')
        except Exception, e:
            error(e)
            error(delete_meeting_info_by_roomno.url)
            error(delete_meeting_info_by_roomno.request.body)
            error(delete_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)
        #删除后查询会议
        info(u'删除后查询会议')

        url_get_meeting_info_by_roomno = ('https://' + self.ip + conf_get_meeting_info_by_roomno['uri'] + '?enterpriseId=' + self.enterpriseId) % room_no
        get_meeting_info_by_roomno = requests_sig(conf_get_meeting_info_by_roomno['method'], url_get_meeting_info_by_roomno, '',self.token, verify=False)
        try:
            self.assertEqual(get_meeting_info_by_roomno.status_code, 204, msg=u'删除后查询')
            #self.assertRegexpMatches(get_meeting_info_by_roomno.text, 'invalid cloud meeting number', msg='删除后查询')
        except Exception, e:
            error(e)
            error(get_meeting_info_by_roomno.url)
            error(get_meeting_info_by_roomno.request.body)
            error(get_meeting_info_by_roomno.text)
            raise e
        time.sleep(1)





#传入excel
def __generateTestCases(case_data_all):
    for casedata in case_data_all:
        if casedata['version'] == 'v1':
            setattr(create_meeting_v1, 'test_%s' % casedata['case_name'],create_meeting_v1.getTestFunc(casedata))
        elif casedata['version'] == 'v2':
            setattr(create_meeting_v1, 'test_creatv2_%s' % casedata['case_name'],create_meeting_v1.getTestFunc_v2(casedata))


#test_func_%s_%s 这里用来定义testcase名称
#读取数据，动态生成testcase
ddd = get_data(dir_case, u'创建会议')
__generateTestCases(ddd)


if __name__ == '__main__':
    info(' start')


    unittest.main()
