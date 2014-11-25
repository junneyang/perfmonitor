#!/usr/bin/env python
#-*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

import sys
import os
sys.path.append("%s/../"%os.path.dirname(os.path.realpath(__file__)))

def mail_send(subject,attach_file,content,from_mail_addr,to_mail_addr,mail_server):
    mail = MIMEMultipart()
    mail["Subject"] = subject

    att = MIMEText(open(attach_file, 'rb').read(), 'base64', 'gb2312')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = "attachment; filename="+attach_file    #这里的filename可以任意写，写什么名字，邮件中显示什么名字
    mail.attach(att)

    content = MIMEText(content,'html','utf-8')
    mail.attach(content)


    mail["From"]=from_mail_addr
    mail["To"]=to_mail_addr
    smtp=smtplib.SMTP(mail_server)
    smtp.sendmail(mail["From"], mail["To"].split(","), mail.as_string())
    smtp.quit()

if __name__ == '__main__':
    subject = u"【内存监控】内存监控曲线图"
    attach_file = u"monitorimg.tar.gz"
    content = u""
    from_mail_addr = u"XXX"
    to_mail_addr = u"XXX"
    mail_server = u"XXX"

    mail_send(subject,attach_file,content,from_mail_addr,to_mail_addr,mail_server)

