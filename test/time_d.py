import time
from datetime import date, timedelta

import paramiko

host_name="10.100.19.228"
port="22"
username="liyanan"
password="yySp6LXJ6tcUAf"
    # 实例化ssh客户端
ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 获取服务器信息

    # 连接服务器
ssh.connect(hostname=host_name, port=port, username=username, password=password)
    # 设置两天后的时间
afterDay = date.today() + timedelta(days=+2)

cmd = f'sudo -s date'  # 设置时间并写入bios
stdin, stdout, stderr = ssh.exec_command(cmd)
    # exec_command 返回的对象都是类文件对象
    # stdin 标准输入 用于向远程服务器提交参数，通常用write方法提交
    # stdout 标准输出 服务器执行命令成功，返回的结果  通常用read方法查看
    # stderr 标准错误 服务器执行命令错误返回的错误值  通常也用read方法
result = stdout.read() or stderr.read()
ssh.close()
res = result.decode().strip()
time_struct = time.strptime(res, '%a %b %d %H:%M:%S CST %Y')
print(time_struct)
times = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
print(time, " : ", times)


