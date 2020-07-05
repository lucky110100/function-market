# -*-coding:utf-8 -*-
import pexpect
import sys

def ssh_cmd(ip, user, passwd, cmd):
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
    r = ''
    try:
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
    except pexpect.EOF:
        ssh.close()
    else:
        r = ssh.read()
        ssh.expect(pexpect.EOF)
        ssh.close()
    return r

def ssh_cmd3(ip, user, passwd):
    ssh = pexpect.spawn('ping -c 1 11.11.1.1')
    ssh.logfile = sys.stdout
    # r = ''
    try:
        ssh.expect([']#'])
        ssh.sendline('ls -al')


        ssh.expect([']#'])
        ssh.close()
    except pexpect.EOF:
        ssh.close()

def ssh_cmd2(ip, user, passwd):
    ssh = pexpect.spawn('ssh %s@%s' % (user, ip))
    ssh.logfile = sys.stdout
    # r = ''
    try:
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
        ssh.expect([']#'])
        ssh.sendline('ls -al')
        # print(ssh.read())
        # print(ssh.after)
        # print(ssh.before)
        # if i == 0:
        # ssh.wait()
        # ssh.expect([']#'])
        # ssh.sendline('sleep 3')

        ssh.expect([']#'])
        ssh.sendline('echo "hhhhh" > /tmp/haha.log')
        # print(ssh.before)

        ssh.expect([']#'])
        ssh.sendline('ls -l /tmp')

        # ssh.expect([']#'])
        # ssh.sendline('scp /tmp/haha.log ceont@11.11.1.1:/tmp')

        ssh.expect([']#'])
        ssh.sendline('scp /tmp/haha.log centos@117.78.22.161:/tmp')
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect(['password: '])
            ssh.sendline(passwd)

        # ssh.expect([']#'])
        # ssh.sendline('scp /tmp/haha.log ceont@11.11.1.1:/tmp')

        ssh.expect([']#'])
        ssh.close()
    except pexpect.EOF:
        ssh.close()
    # else:
    #     r = ssh.read()
    #     ssh.expect(pexpect.EOF)
    #     ssh.close()
    # return r

# hosts = '''
# 192.168.0.12:smallfish:1234:df -h,uptime
# 192.168.0.13:smallfish:1234:df -h,uptime
# '''
hosts = '11.11.11.11:root:123456:df -h,uptime'

ssh_cmd3('', '', '')

# for host in hosts.split("\n"):
#     if host:
#         ip, user, passwd, cmds = host.split(":")
#
#         # for cmd in cmds.split(","):
#         #     print "-- %s run:%s --" % (ip, cmd)
#         #     print ssh_cmd2(ip, user, passwd)
#         print ssh_cmd2(ip, user, passwd)
