#coding:utf8
from django.conf.urls import url

from .import views

app_name='comments'
#给这个评论的 URL 模式规定命名空间，即 app_name = 'comments'

urlpatterns=[url(r'^comment/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment')]

#视图函数需要和 URL 绑定