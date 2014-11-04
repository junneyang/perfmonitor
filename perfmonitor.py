#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import datetime
import time
import psutil

from com.cmdLib import *
from com.logLib import *

class perfmonitor(object):
    def __init__(self, pid_list, monitor_time):
        self.pid_list = pid_list
        self.monitor_time = monitor_time
        self.perflog = "./perflog/"
        self.perfimg = "./perfimg/"
        status,output=cmd_execute("rm " + self.perflog + "*")
    def perfrunner(self):
        try:
            monitorsecond = self.monitor_time * 60
            begintime = (int)(time.time())
            p_list = []
            for pid in self.pid_list:
                p_list.append(psutil.Process(int(pid)))
            while(((int)(time.time()) - begintime) <= monitorsecond):
                for p in p_list:
                    name = p.name()
                    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    memusage = p.memory_info().rss/1024.0/1024.0
                    cpuusage = p.cpu_percent()
                    memusagestr = current + "\t" + str(memusage) + "\n"
                    cpuusagestr = current + "\t" + str(cpuusage) + "\n"

                    memusagestr_filepath = self.perflog + "mem" + "-" + name + "-" + str(p.pid) + ".log"
                    cpuusagestr_filepath = self.perflog + "cpu" + "-" + name + "-" + str(p.pid) + ".log"

                    fp=open(memusagestr_filepath,"a")
                    fp.write(memusagestr)
                    fp.close()
                    fp=open(cpuusagestr_filepath,"a")
                    fp.write(cpuusagestr)
                    fp.close()

                time.sleep(1)

            now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
            cmdstr = "tar -czf perflog." + now + ".tar.gz " + self.perflog
            status,output = cmd_execute(cmdstr)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("""======================================================================================
|                              Usage Instructions                                    |
======================================================================================""")
        print("""|  usage              : python perfmonitor.py PIDList MonitorTime""")
        print("""|  example            : python perfmonitor.py 1846,3252 1""")
        print("""======================================================================================""")
        sys.exit()
    pid_list = sys.argv[1].split(",")
    #print pid_list
    monitor_time = int(sys.argv[2])
    perfm = perfmonitor(pid_list, monitor_time)
    perfm.perfrunner()

