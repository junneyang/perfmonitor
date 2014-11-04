#!/usr/bin/env python
#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy
import math
import pytz
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import datetime
import time

import sys
import datetime
import time
import os
from com.cmdLib import *
from com.logLib import *

def get_mem_stat_data(filepath):
    fp=open(filepath)
    mem_stat_data=[]
    for line in fp:
        line=line.strip()
        line_list=line.split("\t")
        mem_stat_data.append(line_list)
    fp.close()
    return mem_stat_data

def get_query_period_distribution_plot(stat_type, mem_stat_data, savefile):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xaxis = ax.xaxis
    yaxis = ax.yaxis
    yList=[]
    dateList=[]
    for item in mem_stat_data:
        dateList.append(item[0])
        try:
            assert(type(eval(item[1])) == float or type(eval(item[1])) == int)
            yList.append(item[1])
        except:
            yList.append(0)
    #print dateList
    #print len(dateList)
    #print yList

    '''t=time.strptime(dateList[0], "%Y-%m-%d %H:%M:%S")
    startDate = time.mktime(t)
    t=time.strptime(dateList[len(dateList)-1], "%Y-%m-%d %H:%M:%S")
    endDate = time.mktime(t)
    timestamps=numpy.linspace(startDate,endDate,len(yList))
    est=pytz.timezone('Asia/Shanghai')
    dates=[datetime.datetime.fromtimestamp(ts,est) for ts in timestamps]'''
    dates=[datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S") for item in dateList]
    ax.plot_date(dates,  yList,  'm-',  marker='.',  linewidth=1)

    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d %H:%M:%S') )
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

    name=savefile.split("/")[2].split(".")[0]
    plt.title(name)
    plt.xlabel(u'Time')
    if(stat_type == "mem"):
        plt.ylabel(u'memUsage-MB')
    elif(stat_type == "cpu"):
        plt.ylabel(u'cpuUsage-%')
    plt.grid(True)


    fig.autofmt_xdate()
    plt.savefig(savefile)

if __name__ == '__main__':
    if(len(sys.argv) != 4):
        print("""======================================================================================
|                              Usage Instructions                                    |
======================================================================================""")
        print("""|  usage              : python perfstat.py from_mail_addr to_mail_addr mail_server""")
        print("""|  example            : python perfstat.py yangjun03@baidu.com yangjun03@baidu.com mail2-in.baidu.com""")
        print("""======================================================================================""")
        sys.exit()
    file_dir = "./perflog/"
    img_file_dir = "./perfimg/"
    status,output = cmd_execute("rm "+img_file_dir+"*")
    file_list = os.listdir(file_dir)
    #print file_list
    for item in file_list:

        if(item.split("-")[0] == "cpu"):
            stat_type = "cpu"
        elif(item.split("-")[0] == "mem"):
            stat_type = "mem"
        if(os.path.isfile(file_dir+item)):
            mem_stat_data=get_mem_stat_data(file_dir+item)
            get_query_period_distribution_plot(stat_type, mem_stat_data, img_file_dir + item + ".perf_stat_plot.png")

    from com.email_lib import *
    now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    attach_file = u"perfimg-" + now + ".tar.gz"
    cmdstr="tar -czf "+attach_file+" "+img_file_dir
    status,output=cmd_execute(cmdstr)
    subject = u"【性能监控】性能监控曲线图"

    content = u"性能监控曲线图见附件"
    '''from_mail_addr = u"yangjun03@baidu.com"
    to_mail_addr = u"yangjun03@baidu.com"
    mail_server = u"mail2-in.baidu.com"'''
    from_mail_addr = sys.argv[1]
    to_mail_addr = sys.argv[2]
    mail_server = sys.argv[3]

    mail_send(subject,attach_file,content,from_mail_addr,to_mail_addr,mail_server)

    cmdstr="rm " + attach_file
    status,output=cmd_execute(cmdstr)
