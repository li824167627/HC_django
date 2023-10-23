import json
import re
from datetime import date,datetime
from django.db.utils import ConnectionHandler
from django.utils.connection import ConnectionProxy
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

test = "Set-Cookie: XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; Path=/; HttpOnlyContent-Type: application/jsonTransfer-Encoding: chunkedDate: Mon, 03 Apr 2023 09:10:27 GMTKeep-Alive: timeout=60Connection: keep-alive"

def find(b):
    res = re.findall(r"Set-Cookie: (.+?);",b)
    return res

print(find(test)[0])

def time_format(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    """
    @时间格式转化
    :param time_string:
    :param from_format:
    :param to_format:
    :return:
    """
    time_struct = datetime.strptime(time_string,from_format)
    times = datetime.strftime(to_format, time_struct)
    return times

def query_sql(sql):
    connections = ConnectionHandler()
    connection = ConnectionProxy(connections, "yzt")
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        print("data:", data)
    finally:
        cursor.close()
        connection.close()
    return True, None

#if __name__ == "__main__":
    cst_time='Tue Nov 09 12:12:12 CST 2021'
    #res = json.loads(cst_time)
    #format_time=time_format(cst_time,'%a %b %d %H:%M:%S CST %Y', '%Y-%m-%d %H:%M:%S')
    dt_now = datetime.now()
    date_time = dt_now.strftime("%Y-%m-%d %H:%M:%S,%A,%B")
    time = datetime.strptime(cst_time,'%a %b %d %H:%M:%S CST %Y')
    print(type(dt_now))
    print (date_time)
    print(time)

    sql = "SELECT * FROM bs_yzt_hczd.cust_extend WHERE pre_customer_no = 'Y1506171666321700568';"
    query_sql(sql)