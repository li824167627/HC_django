from django.db.utils import ConnectionHandler
from django.utils.connection import ConnectionProxy
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


def chose_sql(basename, sql):
    connections = ConnectionHandler()
    connection = ConnectionProxy(connections, basename)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        print("data:", data)
    finally:
        cursor.close()
        connection.close()
    return data