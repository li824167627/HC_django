import json
import time

from django.core import serializers
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import HttpResponse
from create_data.models import book, status
from create_data.models import hostinfo
import pytz
import paramiko
from datetime import date, timedelta
from create_data.main.service import chose_sql

tz = pytz.timezone('Asia/Shanghai')


@require_http_methods(["POST"])
def applynotify(request):
    response = {}
    try:
        print(request.body)
        postBody = request.body
        Status = json.loads(postBody)['param']['creditStatus']
        loanRequestNo = json.loads(postBody)['param']['loanRequestNo']
        creditValidity = json.loads(postBody)['param']['creditValidity']
        a = status(loan_request_no=loanRequestNo,payment_status=Status,Ctime=creditValidity)
        a.save()
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
        response['date'] = {'loanRequestNo':loanRequestNo,'Status':Status}
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)

@require_http_methods(["GET"])
def query_sql(request):
    response = {}
    try:
        phone = request.GET.get('phone')
        sql = f"SELECT pre_customer_no FROM `bs_yzt_hczd`.cust_pre_info WHERE contact_info='{phone}'"
        pre_customer_no = chose_sql("yzt", sql)[0][0]
        sql2 = f"SELECT * FROM bs_yzt_hczd.cust_extend WHERE pre_customer_no = '{pre_customer_no}';"
        data = chose_sql("yzt", sql2)
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
        response['data'] = data
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(['GET'])
def index(request):
    return HttpResponse('这是我创建的view')


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book_name = request.GET.get('book_name')
        if(book_name==""):
            response['respmsg'] = '请输入书名'
            response['respcode'] = '666666'
        else:
            b = book(bookname=book_name)
            b.save()
            response['respmsg'] = 'success'
            response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        sta = status.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", sta))
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(["POST"])
def del_books(request):
    response = {}
    try:
        print(request.body)
        postBody = request.body
        id = json.loads(postBody)['pk']
        id = status(id=id)
        id.delete()
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(["POST"])
def edit_books(request):
    response = {}
    try:
        print(request.body)
        postBody = request.body
        id = json.loads(postBody)['pk']
        new_bookname = json.loads(postBody)['bookname']
        data = book(id=id)
        data.bookname = new_bookname
        data.createtime = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        data.save()
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_time(request):
    response = {}
    try:
        print(request.GET)
        hostname = request.GET.get('show_time')
        print("hostname"+hostname)
        # 实例化ssh客户端
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 获取服务器信息

        # 连接服务器
        ssh.connect(hostname=hostname, port=22, username='liyanan', password='yySp6LXJ6tcUAf')
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
        time_struct = time.strptime(res,'%a %b %d %H:%M:%S CST %Y')
        print(time_struct)
        times = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        print(request, " : ", times)
        response['data'] = times
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
        print(response)
    return JsonResponse(response)


@require_http_methods(["GET"])
def host(request):
    response = {}
    try:
        sh = hostinfo.objects.filter()
        response['options'] = json.loads(serializers.serialize("json", sh))
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


@require_http_methods(["POST"])
def time_date(request):
    response = {}
    try:
        print(request.body)
        postBody = request.body
        host_name = json.loads(postBody)['hn']
        print(host_name)
        #h = hostinfo.objects.filter(hostname=host_name)
        h = hostinfo.objects.get(hostname=host_name)
        # 实例化ssh客户端
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 获取服务器信息

        # 连接服务器
        ssh.connect(hostname=h.hostname, port=h.port, username=h.user, password=h.password)
        # 设置两天后的时间
        afterDay = date.today() + timedelta(days=+2)

        cmd = f'date'  # 设置时间并写入bios
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # exec_command 返回的对象都是类文件对象
        # stdin 标准输入 用于向远程服务器提交参数，通常用write方法提交
        # stdout 标准输出 服务器执行命令成功，返回的结果  通常用read方法查看
        # stderr 标准错误 服务器执行命令错误返回的错误值  通常也用read方法
        result = stdout.read() or stderr.read()
        ssh.close()
        res = result.decode().strip()
        print(res)
        time_struct = time.strptime(res, '%a %b %d %H:%M:%S CST %Y')
        times = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        response['data'] = times
        response['respmsg'] = 'success'
        response['respcode'] = '000000'
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)

@require_http_methods(["POST"])
def set_server_time(request):
    # 获取POST请求参数
    postBody = request.body
    host_name = json.loads(postBody)['hn']
    new_time = json.loads(postBody)['new_time']
    h = hostinfo.objects.get(hostname=host_name)
    print(new_time,"++++++++++",host_name)
    try:
        # 连接远程服务器
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=h.hostname, port=h.port, username=h.user, password=h.password)

        # 格式化需要修改的时间
        time_struct = time.strptime(new_time, '%Y-%m-%dT%H:%M:%S.000Z')
        new_time = time.strftime("%a %b %d %H:%M:%S CST %Y", time_struct)
        print(new_time)
        # 查询当前时间
        cmd = f'sudo -s date'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read() or stderr.read()
        res = result.decode().strip()
        time_struct = time.strptime(res, '%a %b %d %H:%M:%S CST %Y')
        print(time_struct)
        befor_time = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        # 执行修改时间的命令
        cmd = f'sudo date -s "{new_time}"'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read() or stderr.read()
        res = result.decode().strip()
        time_struct = time.strptime(res, '%a %b %d %H:%M:%S CST %Y')
        print(time_struct)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        #查询当前时间
        cmd = f'sudo -s date'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read() or stderr.read()
        ssh.close()
        res = result.decode().strip()
        time_struct = time.strptime(res, '%a %b %d %H:%M:%S CST %Y')
        print(time_struct)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        # 构造JSON格式的响应
        response = {
            'status': 'success',
            'respcode':'000000',
            'message': f'Server time changed from {befor_time} to {current_time}.',
            'data': current_time
        }
    except Exception as e:
        response['respmsg'] = str(e)
        response['respcode'] = '999999'
    return JsonResponse(response)


