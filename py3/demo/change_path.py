#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author:lhj
@time:2018/12/26
"""
import os


if __name__ == '__main__':
    # grep -nr "/home/user/work/chromium-arm" /home/user/work/awfy > arm.txt 2>&1 &
    kv = {
        'x64': "\/home\/user\/work\/chromium_repos",
        'arm': "\/home\/user\/work\/chromium-arm",
        'glm': "\/home\/user\/work\/chromium_glm_repos"
    }

    for k,v in kv.items():
        with open('%s.txt'%k) as f:
            data = f.readlines()
        path_list = map(lambda x: x[:x.find(':')], data)
        # replace all host to localhost.
        for path in path_list:
            cmd = 'perl -pi -e "s/%s/%s/g" %s' % (v, "\/home\/user\/work\/repos\/chrome\/%s"%k, path)
            print(cmd)
            os.system(cmd)
