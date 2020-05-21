#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append('../')
from Getsignatrue import Get_signature_url
import requests
import json

from public.readconf import allconf
enterprise = allconf["enterprise"]
tokendef =  str(enterprise["token"])


def requests_sig(method,url,data,token,*args,**kwargs):
    if data == '':
        data_dumps = data
    else :
        #data_dumps = json.dumps(data, sort_keys=True,ensure_ascii=False)
        data_dumps = json.dumps(data, sort_keys=True)
    newurl = Get_signature_url(method,url,data_dumps,token).get_url()
    if method == 'GET':
        return requests.get(newurl,data_dumps,*args,**kwargs)
    elif method == 'POST':
        return requests.post(newurl,data_dumps,*args,**kwargs)
    elif method == 'PUT':
        return requests.put(newurl,data_dumps,*args,**kwargs)
    elif method == 'DELETE':
        return requests.delete(newurl,*args,**kwargs)


def requests_normal(method,url,data,token,*args,**kwargs):
    if data == '':
        data_dumps = data
    else :
        data_dumps = json.dumps(data, sort_keys=True)
    if method == 'GET':
        return requests.get(url,*args,**kwargs)
    elif method == 'POST':
        return requests.post(url,data_dumps,*args,**kwargs)
    elif method == 'PUT':
        return requests.put(url,data_dumps,*args,**kwargs)
    elif method == 'DELETE':
        return requests.delete(url,*args,**kwargs)

if __name__=="__main__":
    url = 'https://10.170.197.17/api/rest/external/v1/meeting/statistic/enterprise?enterpriseId=965af5a13523731e849d675c28b53b21caeec0d1&timeEnd=1525948299000&timeBegin=1525947840000'

    data = {'enterpriseId': '965af5a13523731e849d675c28b53b21caeec0d1', 'timeBegin': 1525947840000,
            'timeEnd': 1525948299000}
    data3 = { "meetingName": "创建222", "startTime": 1546347664000, "endTime": 1546348864000, "maxParticipant": 10, "requirePassword": False, "controlPassword": "123456", "autoMute": 0, "configs":{  "autoRecord":True }}
    data2 = {
                "meettingRoomName": "测试修改",
                "meetingRoomState": "idle",
                "autoMute":"2",
                "smartMutePerson": 3,
                "autoRecord": True,
                "expireTime":1525948299000,
                "password":"123456",
                "meetingControlPwd":"654321",
                "recordAddDeviceName":True,
                "onlyRecordMainImage":True
                }
    data4 = {"address": "aAa1","autoInvite": 1,"autoRecord": 1,"conferenceControlPassword": "475073","conferenceNumber": "9000746310","details": "aaaaaa1","endTime": 1547044625000,"meetingRoomType": 2,"participants": ["9000746310", "673492"],"password": "111111","startTime": 1547043425000,"title": '11预约测绘aaaa'}
    headers_json = {'content-type': 'application/json'}
    url2 = 'https://cloud.xylink.com/api/rest/external/v1/meetingInfo/910061076087?enterpriseId=e608e0f43963706372c006235c79d01890e82966'
    url3 = 'https://cloud.xylink.com/api/rest/external/v2/create_meeting?enterpriseId=e608e0f43963706372c006235c79d01890e82966'
    url4 = 'https://cloud.xylink.com/api/rest/external/v1/meetingreminders?enterpriseId=e608e0f43963706372c006235c79d01890e82966'
    #get = requests.get(url, params=data, verify=False)
    #gettmp = requests_sig('PUT',url2,data2,tokendef,verify=False,headers=headers_json)
    post_tmp = requests_sig('POST',url4,data4,tokendef,verify=False,headers=headers_json)
    print post_tmp.status_code
    print post_tmp.url
    print post_tmp.text
    print post_tmp.request.body
    print Get_signature_url('GET',url,'',tokendef).Get_signature()