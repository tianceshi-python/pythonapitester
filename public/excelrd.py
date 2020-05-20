#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ConfigParser
import xlrd
import os,sys
sys.path.append('../')
from public.readconf import allconf

dir_case = allconf["testcase"]["casefile"]
#dir_case = os.path.join(os.path.dirname(os.path.dirname(__file__)),testcase['casefile'])
#读取按sheet名称读取excel：
#excel内容：
#A1	B1	C1	D1	D1   #列名
#A2	B2	C2	D2	E2   #case1
#A3	B3	C3	D3	E3   #case2
#返回：[{u'A1': u'A2', u'C1': u'C2', u'B1': u'B2', u'D1': u'D2,,,E2'}, {u'A1': u'A3', u'C1': u'C3', u'B1': u'B3', u'D1': u'D3,,,E3'}]


def get_data(dir_case, sheet_name):
    data = xlrd.open_workbook(dir_case)
    table = data.sheet_by_name(sheet_name)
    nor = table.nrows
    nol = table.ncols
    datelist = []
    for i in range(1, nor):
        dict = {}
        for j in range(nol):
            title = table.cell_value(0, j)
            value = table.cell_value(i, j)
            if dict.has_key(title):
                #dict[title] += [value]
                dict[title] += ",,,"
                dict[title] += value
            else:
                #dict[title] = [value]
                dict[title] = value
        datelist += [dict]
    return datelist

if __name__=="__main__":
    ddd =  get_data(dir_case,u'样例')
    print ddd
    for i in ddd:
        print i