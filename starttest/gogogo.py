#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
import requests
import os,shutil,datetime,sys

sys.path.append('../')
from public import HTMLTestRunnerNEW as HTMLTestRunner
from public.log import *
from public.sendmail import *
from public import HTMLTestRunnerCN


if __name__=='__main__':
    print os.path.dirname(__file__)
    info('starttest')
    discover = unittest.defaultTestLoader.discover('../testcase',pattern="test*.py",top_level_dir=None)
    #discover = unittest.defaultTestLoader.discover('../testcase',pattern="test_creat_sdkroom.py",top_level_dir=None)


    fp = open("../report/result.html", "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'自动化测试报告,测试结果如下：',description=u'用例执行情况：')
    #runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp,title=u'自动化测试报告,测试结果如下：',description=u'用例执行情况：')

    runner.run(discover)
    fp.close()
    f = open("../report/result.html", "rb")
    msg = f.read()
    f.close()
    time = datetime.datetime.now().strftime('%m%d%H')
    result_html = "../report/result"+datetime.datetime.now().strftime('%m%d%H')+".html"
    result_log = "../log/run"+datetime.datetime.now().strftime('%m%d%H')+".log"
    shutil.copyfile("../report/result.html", result_html)  # 移动文件
    shutil.copyfile("../log/run.log", result_log)  # 移动文件
    sendmail(msg,[result_html,result_log])