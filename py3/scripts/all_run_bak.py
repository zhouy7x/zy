#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author:lhj
@file: all_run.py
@time: 2018/12/11
"""
from sys import argv
import datetime
import os

MEMSIZE = '8g'
now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
print(now)


def remove_lock(param):
    rm_lock_cmd = "rm /tmp/opengrok-repo-sync-%s.lock -rf" % param
    os.system(rm_lock_cmd)


def run_schedule(param):
    schedule_dict = {
        'v8': 'python /scripts/schedule_v8.py > /log/v8/schedule_%s-%s.log 2>&1 &' % (param, now),
        'chrome': 'python /scripts/schedule_chrome.py > /log/chrome/schedule_%s-%s.log 2>&1 &' % (param, now),
        'tf': 'python /scripts/schedule_tf.py > /log/tf/schedule_%s-%s.log 2>&1 &' % (param, now)
    }
    # create log directory.
    if not os.path.exists('/log/%s' % param):
        os.mkdir('/log/%s' % param)
    # reomove lock file
    remove_lock(param)
    # run schedule script.
    print(schedule_dict[param])
    os.system(schedule_dict[param])


def check_run_stat(param):
    command = r'ps aux | grep -E "python" | grep -E "schedule_%s.py" | grep -v grep' % param
    data_list = os.popen(command).read().splitlines()
    # print(data_list)
    if not data_list:
        return 0
    else:
        pid_list = map(lambda x: x.split()[1], data_list)
        print("WARNING: %s repository synchronization is already running, its PID is: " % param + ",".join(pid_list))
        return 1


def index_file(mem_size=MEMSIZE):
    cmd = "python3 index.py %s" % mem_size
    return os.system(cmd)


def check_tomcat_status(foo):
    def _inside():
        cmd = "ps uax | grep tomcat | grep java | grep start | grep -v grep"
        ret = os.popen(cmd).read()
        if ret:
            return foo()
        else:
            print("tomcat is already running!")
            return 0
    return _inside


@check_tomcat_status
def start_tomcat():
    cmd = "/bin/bash /usr/local/tomcat/bin/startup.sh"
    return os.system(cmd)


def get_available_memory():
    cmd = "cat /proc/meminfo | grep MemAvailable"
    try:
        free_mem = int(os.popen(cmd).read().split()[1])
    except Exception as e:
        print(e)
        free_mem_final = '8g'
    else:
        kw = 'k'
        if free_mem > 1024:
            kw = 'm'
            free_mem = free_mem / 1024
            if free_mem > 1024:
                kw = 'g'
                free_mem = free_mem / 1024
        free_mem_final = str(int(free_mem * 0.9)) + kw
    print(free_mem_final)
    return free_mem_final


def main(params):
    if not params:
        params = ['v8', 'chrome', 'tf']
    print(params)

    for param in params:
        if param.lower() in ['v8', 'chrome', 'tf']:
            if not check_run_stat(param.lower()):
                run_schedule(param.lower())

        else:
            print('ERROR: Wrong args %s!' % param)
            continue


if __name__ == '__main__':
    # startup tomcat.
    if not start_tomcat():
        # get server's available memory size.
        size = get_available_memory()
        # index opengrok source.
        if not index_file(size):
            # startup real-time update scripts.
            main(argv[1:])
        else:
            print("WARNING: Index failed and exit!")
    else:
        print("WARNING: Startup tomcat failed and exit!")

