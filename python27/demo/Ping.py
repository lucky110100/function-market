# -*- coding: utf-8 -*-

import subprocess
import traceback
import platform

def ping(host):
    '''ping 1次指bai定du地zhi址dao'''

    if platform.system()=='Windows':
        cmd = 'ping -n %d %s'%(1,host)
    else:
        cmd = 'ping -c %d %s'%(1,host)
    try:
        p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (stdoutput,erroutput) = p.communicate()
        print stdoutput
    except Exception, e:
        traceback.print_exc()
    if platform.system()=='Windows':
        return stdoutput.find('Received = 1')>=0
    else:
        return stdoutput.find('1 packets received')>=0
if __name__ == "__main__":
    print ping('baidu.com')