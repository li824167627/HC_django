import os
from time import sleep
import time
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from create_data.models import hostinfo
import datetime
import pytz
import paramiko

tz = pytz.timezone('Asia/Shanghai')

@require_http_methods(["GET"])
def examine(request):
    response = {}
    try:
        order_no = request.GET.get('order_no')
        #host_name = json.loads(postBody)['hn']
        print('+++++++++++++'+order_no)
        #当前日期
        current_date = datetime.datetime.now().strftime('%Y%m%d')
        #当前月份
        current_month = datetime.datetime.now().strftime('%Y%m')
        #目标路径
        remote_path = f'/WLSJ01/return/50/202309/test'
        print(order_no+'++++'+current_month+'+++++++++'+current_date)
        host_name = '10.150.30.234'
        #h = hostinfo.objects.filter(hostname=host_name)
        h = hostinfo.objects.get(hostname=host_name)

        # 实例化ssh客户端
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接服务器
        ssh.connect(hostname=h.hostname, port=h.port, username=h.user, password=h.password)

        # 切换到sudo su权限
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo su')

        stdin, stdout, stderr = ssh.exec_command(f'cp /home/bohai/local_file/WLSJ01_202309211508390_10_001.pdf /home/bohai/remote_file/WLSJ01_{order_no}_10_001.pdf')
        # 建立SFTP连接
        transport = ssh.get_transport()
        sftp = transport.open_sftp_client()

        # 连接SFTP服务器
        sftp_command = 'sftp -oPort=23229 WLSJTest@175.25.49.73'
        sftp_shell = ssh.invoke_shell()
        sftp_shell.send(sftp_command + '\n')
        # 确保SFTP连接成功
        output = sftp_shell.recv(65535).decode('utf-8')
        print(output)
        i=1
        # 定义一个函数，用于检查条件是否成立
        def check_condition():
            # 这里假设条件不成立
            condition = 'password' in sftp_shell.recv(65535).decode('utf-8')
            # 模拟检查条件的过程
            time.sleep(1)
            # 返回条件是否成立的结果
            return condition

        # 使用while循环等待条件成立
        while not check_condition():
            # 打印提示信息
            print("条件还没有成立，继续等待...",i)
            # 暂停1秒钟
            time.sleep(1)
            i = i+1
        # 条件成立后执行的代码
        print("条件已经成立！",output)
        sftp_shell.send('puan0314\n')
        sleep(2)
        # 查询当前路径
        sftp_shell.send('pwd\n')
        output = sftp_shell.recv(65535).decode()
        current_path = output.strip().split('\n')[-1]
        print('当前路径:', current_path)

        #创建新文件夹
        sftp_shell.send(f'mkdir /WLSJ01/return/50/{current_month}/{current_date}\n')
        sleep(1)
        #上传pdf文件
        sftp_shell.send(f'put /home/bohai/remote_file/WLSJ01_{order_no}_10_001.pdf /WLSJ01/return/50/{current_month}/{current_date}\n')
        sleep(3)
        # 关闭SFTP连接和SSH连接
        sftp_shell.close()
        #sftp.mkdir('/WLSJ01/return/50/202309/test')
        #sftp.put(f'/home/bohai/remote_file/WLSJ01_{order_no}_10_001.pdf', f'/WLSJ01/return/50/{current_month}/{current_date}')
        sftp.close()

        # 创建sfpt目录
        #ssh.exec_command(f'mkdir /WLSJ01/return/50/{current_month}/{current_date}/test\n')


        # 上传pdf到sfpt服务器
        #ssh.exec_command(f'put /home/bohai/remote_file/WLSJ01_{order_no}_10_001.pdf /WLSJ01/return/50/{current_month}/{current_date}\n')

        # 关闭SSH连接
        ssh.close()

        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
        print(str(e))
    return JsonResponse(response)