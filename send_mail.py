# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from pyecharts import Bar, Line, Grid
from pyecharts import configure
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

#echarts
def echart(echart_name):
    reader = unicode_csv_reader(echart_name+'.csv')
    data = list(reader)
    data_t = map(list, zip(*data[1:]))
    attr = data_t[0]
    name = data[0]
    for i in range(1,len(data_t)):
        #print(name[i],attr,data_t[i])
        bar.add(name[i],attr,data_t[i], is_stack=True)
    bar.render(path=echart_name+'.png')

#插入图片
def addPic(msg, pic_file):
    echart(pic_file)
    fp = open(base_path + pic_file + '.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<'+pic_file+'>')
    msg.attach(msgImage)

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

def add_table(csv_list):
    tables = {}
    for csv_list in csv_lists:
        reader = unicode_csv_reader(csv_list+'.csv')
        tables[csv_list] = list(reader)
    return tables

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
    subject = 'echart test'
    bar = Bar(subject)
    attach_lists = []
    csv_lists = ['b','c']
    pic_lists = ['b']

    tables = add_table(csv_lists)
    template = env.get_template('template.html')
    content = template.render(day=yesterday, data=tables, pic=pic_lists[0])
    sendMail(me, subject, content, attach_lists, pic_lists)
