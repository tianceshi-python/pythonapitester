#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import ConfigParser
import smtplib
import sys,os
sys.path.append('../')
from public.log import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
#cf = ConfigParser.ConfigParser()
#cf.read(os.path.normpath(file))
#mail = dict(cf.items("mail"))
#print mail
from public.readconf import allconf
mail = allconf["mail"]

def sendmail(msgg, files):
#    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    mail_host = mail["mail_host"]
    mail_user = mail["mail_user"]
    mail_pass = mail["mail_pass"]
    rec_user = mail["rec_user"]

    print rec_user
    msg = MIMEMultipart()
    msg['Subject'] = mail["subject"]
    msg['From'] = mail_user
    msg['To'] = rec_user
    msg.attach(MIMEText(msgg, _subtype='html', _charset='utf-8'))
    for file in files:
        print file
        html = MIMEApplication(open(file, 'rb').read())
        html.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        msg.attach(html)

    try:
        server = smtplib.SMTP_SSL()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, rec_user.split(','), msg.as_string())
        server.close()
        return True
    except Exception as e:
        error(e)