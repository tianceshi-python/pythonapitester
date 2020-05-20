#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urlparse
import re
import hashlib
import base64
import urllib
import hmac
import json
import os

class Get_signature_url(object):
    def __init__(self,method,req_url,req_data,token):
        self.method = method
        self.req_url = req_url
        self.req_data = req_data
        self.token = token

    def parse_url(self):
        test1=urlparse.urlparse(self.req_url)
        ttt = urlparse.parse_qs(test1.query)
        newdict = dict((x,ttt[x][0]) for x in ttt.keys())
        newdict_sort = sorted(newdict.items(), key=lambda e:e[0])
        new_query = urllib.urlencode(newdict_sort)
        API = re.split('/v\d+/', test1.path)
        return API,new_query


    def hash_body(self):
        data_to_send = self.req_data[0:100]
        hash = hashlib.sha256()
        hash.update(data_to_send)
        body = hash.digest()
        body_base64 = base64.b64encode(body)
        return body_base64

    def get_list(self):
        body_b64 = self.hash_body()
        parse_url_reult = self.parse_url()
        llist = '\n'.join([self.method, parse_url_reult[0][1], parse_url_reult[1], body_b64])
        return llist

    def Get_signature(self):
        llist = self.get_list()
        Hmac_sha256 = hmac.new(self.token, llist, digestmod=hashlib.sha256).digest()
        signature = urllib.quote_plus(base64.b64encode(Hmac_sha256))
        return signature
    def get_url(self):
        signature = self.Get_signature()
        last_url = self.req_url + '&signature='+signature
        return last_url

if __name__=="__main__":
    method = 'POST'
    uurl = 'https://182.92.199.157/api/rest/external/v1/callbacks?enterpriseId=3e816492058911e7a31d000c29971af5'
    token = '426739735a32d27eb7d5e38cac4b808f3817c2fbc106a9bde695395553510e6a'
    timestart = 1530424800
    timeend = 1530524800
    data = '一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三'
    print len(data)
    data1 = {"handlerUrl": "aaaa","callbackEvent":"NewCallPush"}
    datatmp = {
"isAll":True,
 "device": {
                "id": "22117954",
                "type": "2"
            }
}
    data_dumps = json.dumps(datatmp, sort_keys=True,ensure_ascii=False)
    print data_dumps
    testprd = Get_signature_url('GET','https://cloud.xylink.com/api/rest/external/v1/deviceInfo?enterpriseId=e608e0f43963706372c006235c79d01890e82966','','9d3aca500c37c47b89c80e374f8b8388b102e1a0c0c84bddc182cc5cb213c4cd')
    testprd2 = Get_signature_url('GET',
                            'https://cloud.xylink.com/api/rest/external/v1/conferenceControl/910057573901/meetingStatus?enterpriseId=e608e0f43963706372c006235c79d01890e82966','',
                            '9d3aca500c37c47b89c80e374f8b8388b102e1a0c0c84bddc182cc5cb213c4cd')
    testprd3 = Get_signature_url('PUT',
                            'https://cloud.xylink.com/api/rest/external/v1/conferenceControl/9000383751/content/authShare?enterpriseId=e608e0f43963706372c006235c79d01890e82966',data_dumps,
                            '9d3aca500c37c47b89c80e374f8b8388b102e1a0c0c84bddc182cc5cb213c4cd',)
    #print testprd.get_url()
    #print testprd2.get_url()
    print testprd3.get_url()