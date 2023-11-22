# coding: utf-8
# author: hmk

from django.urls import path, re_path, include
from . import views, views_sfpt

urlpatterns = [
    path('index', views.index),
    path('add_book', views.add_book),
    path('show_books', views.show_books),
    path('del_books', views.del_books),
    path('edit_books', views.edit_books),
    path('show_time', views.show_time),
    path('host', views.host),
    path('time_date', views.time_date),
    path('set_server_time', views.set_server_time),
    path('query_sql', views.query_sql),
    path('examine', views_sfpt.examine),
    path('applynotify', views.applynotify)
]
