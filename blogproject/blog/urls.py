#coding:utf8
from django.conf.urls import url
from . import views
from django.views.generic import ListView,DetailView


app_name='blog'
#告诉 Django 这个 urls.py 模块是属于 blog 应用的，
# 这种技术叫做视图函数命名空间，因为一个工程下其他应用可能有相同文件名的视图函数
# 我们看到 blog\urls.py 目前有两个视图函数，
# 并且通过 name 属性给这些视图函数取了个别名，
# 分别是 index、detail

urlpatterns=[url(r'^$',views.IndexView.as_view(),name='index'),
             url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'),
#(?P<pk>[0-9]+) 表示命名捕获组，其作用是从用户访问的 URL 里把括号内匹配的字符串捕获并作为关键字参数传给其对应的视图函数PostDetailView
             url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(), name='archives'),
             url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category')
]
#如果访问 /archives/2017/3/,archives 视图函数的实际调用为：archives(request, year=2017, month=3)

#正则表达式部分会被后面传入的参数 pk 替换

# 目前有四个视图函数,通过 name 属性给这些视图函数取了个别名分别是 index、detail、archives、category
#第一个参数 正则表达式 是网址，第二个参数views.index是处理函数 name作为处理函数 index 的别名

