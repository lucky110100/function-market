# -*- coding:utf-8 -*-
import paramiko
import time

def handler(event, context):
    main()


def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")

    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sshClient.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = sshClient.exec_command(execmd)
    # print stdout.read()
    stdin.write("Y") # Generally speaking, the first connection, need a simple interaction.
    print stdout.read()
    # sshClient.exec_command("echo 'hahahahahah' > /tmp/haha.log")
    stdin, stdout, stderr = sshClient.exec_command("cat /tmp/haha.log")
    print stdout.read()
    stdin, stdout, stderr = sshClient.exec_command("scp /tmp/haha.log root@11.11.11.11:/tmp")
    # print stdout.read()
    stdin.write("yes")
    print stderr.read()
    print stdout.read()
    stdin.write(password)

    sshClient.close()

def test_paramiko_interact(hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        channel = ssh.invoke_shell()
        time.sleep(0.1)

        # channel.send("su - \n")
        # buff = ''
        # while not buff.endswith('Password: '):
        #     resp = channel.recv(9999)
        #     buff += resp.decode('utf-8')
        # print(buff)

        channel.send("scp /tmp/haha.log root@11.11.1.1:/tmp\n")
        buff = ''
        while True:
            time.sleep(0.2)
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
            if 'yes/no' in buff:
                channel.send('yes\r') # 【坑3】 如果你使用绝对路径，则会在home路径建立文件夹导致与预期不符
                buff = ''
            elif buff.endswith('password: '):
                channel.send(password)
                channel.send('\n')
                buff = ''
                break

        resp = channel.recv(9999)
        buff += resp.decode('utf-8')

        while not buff.endswith('# '):  # 当指令执行结束后，Linux窗口会显示#，等待下条指令，所以可以用作识别全部输出结束的标志。
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
        # print(buff)

        print("------end------")

        # 查看是否切换成功
        channel.send("whoami")
        channel.send("\n")
        buff = ''
        while not buff.endswith('# '):
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
        print(buff)
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException:
        print('Failed to login. ip username or password not correct.')
        ssh.close()
        exit(-1)

def test_paramiko_interact_copy(hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        channel = ssh.invoke_shell()
        time.sleep(0.1)

        channel.send("scp /tmp/haha.log root@11.11.1.1:/tmp\n")
        buff = ''
        while True:
            time.sleep(0.2)
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
            if 'yes/no' in buff:
                channel.send('yes\r') # 【坑3】 如果你使用绝对路径，则会在home路径建立文件夹导致与预期不符
                buff = ''
            elif buff.endswith('password: '):
                channel.send(password)
                channel.send('\n')
                break

        buff = ''
        while not buff.endswith('$ '):  # 当指令执行结束后，Linux窗口会显示#，等待下条指令，所以可以用作识别全部输出结束的标志。
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
        print(buff)
        print("------end------")

        channel.close()
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException:
        print('Failed to login. ip username or password not correct.')
        ssh.close()
        exit(-1)

def main():

    hostname = '11.11.11.11'
    port = 22
    username = 'centos'
    password = 'passwd'
    execmd = "hostname"

    # sshclient_execmd(hostname, port, username, password, execmd)
    # test_paramiko_interact(hostname, port, username, password)
    test_paramiko_interact_copy(hostname, port, username, password)


# if __name__ == "__main__":
#     main()