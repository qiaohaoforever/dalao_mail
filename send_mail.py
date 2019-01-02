# -*- coding: UTF-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import smtplib
import traceback
import time
import csv
import xlwt
from datetime import datetime, timedelta
from jinja2 import Template
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('dalao_mail'))
base_path = os.getcwd()+'/'

mail_host = 'email.qq.com'
mail_from = 'xxxxxxx@qq.com'
mail_pwd = 'xxxxxxxxx'

me = ['abc@qq.com']    

def addAttach(msg, file_path):    
    attach = MIMEText(open(base_path + file_path, 'rb').read(), 'base64', 'utf-8') 
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename='+file_path
    msg.attach(attach)

def unicode_csv_reader(csv_path, dialect=csv.excel, **kwargs):
    with open(base_path + csv_path) as f:
        csv_reader = csv.reader(f, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

def make_email(to_list, subject, content, attach_paths):
    msg = MIMEMultipart('related') ##采用related定义内嵌资源的邮件
    msgtext = MIMEText(content,_subtype='html',_charset='utf-8') ##_subtype有plain,html等格式，避免使用错误
    msg.attach(msgtext)
    if len(attach_paths) != 0:
        for attach_path in attach_paths:
            addAttach(msg, attach_path)
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = ";".join(to_list)
    return msg

def sendMail(to_list, subject, content, attach_paths):
    msg = make_email(to_list, subject, content, attach_paths)
    try:
        server = smtplib.SMTP(mail_host, 25)
        server.ehlo()
        server.login(mail_from, mail_pwd)      
        server.sendmail(mail_from, to_list, msg.as_string())  
        server.quit() ##断开smtp连接
        print "邮件发送成功"
    except Exception, e:
        print "失败"+str(e)

if __name__=='__main__':
    yesterday = sys.argv[1]
    subject = '{} 日报'.format(yesterday)
    attach_lists = ['b.html', 'c.html']
    csv_lists = ['b', 'c']
    tables = {}
    for csv_list in csv_lists:
        reader = unicode_csv_reader(csv_list+'.csv')
        tables[csv_list] = list(reader)
    template = env.get_template('template.html')
    content = template.render(day=yesterday, data0=tables['b'], data1=tables['c'])
    sendMail(all_list, subject, content, attach_lists)
