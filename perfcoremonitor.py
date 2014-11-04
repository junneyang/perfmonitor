#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import re
import os
import time
from com.cmdLib import *
from com.logLib import *
from com.msgSend import *

def coremonitor(dst_dir,rsv_list,monitor_time):
    monitor_time=int(monitor_time)*60
    if(monitor_time == 0):
        while 1:
            file_reg=r"^core.*$"
            print file_reg
            file_list=os.listdir(dst_dir)
            print file_list
            core_file_list=[]
            for item in file_list:
                if(re.match(file_reg,item)):
                    core_file_list.append(item)
            print core_file_list
            if(len(core_file_list) != 0):
                print("casting core.")
                print(core_file_list)
                msgSend(rsv_list,'casting core file: '+','.join(core_file_list))
                return
            time.sleep(1)
    else:
        for i in xrange(monitor_time):
            file_reg=r"^core.*$"
            print file_reg
            file_list=os.listdir(dst_dir)
            print file_list
            core_file_list=[]
            for item in file_list:
                if(re.match(file_reg,item)):
                    core_file_list.append(item)
            print core_file_list
            if(len(core_file_list) != 0):
                print("casting core.")
                print(core_file_list)
                msgSend(rsv_list,'casting core file: '+','.join(core_file_list))
                return
            time.sleep(1)


if __name__ == '__main__':
    if(len(sys.argv) != 4):
        print("""======================================================================================
|                              Usage Instructions                                    |
======================================================================================""")
        print("""|  usage              : python perfcoremonitor.py dst_dir rsv_list monitor_time""")
        print("""|  example            : python perfcoremonitor.py ./output/laplace 18665817689,13612866267 1""")
        print("""======================================================================================""")
        sys.exit()

    dst_dir=sys.argv[1]
    #print dst_dir
    rsv_list=sys.argv[2].split(",")
    #print rsv_list
    monitor_time=sys.argv[3]

    coremonitor(dst_dir,rsv_list,monitor_time)

