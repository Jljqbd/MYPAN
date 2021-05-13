"""TestWebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django import urls
from django.conf.urls import url
from TestWebapp.views import register,index,login,jump_register,videolist,upload_file,jump_upload,textlist,viewtext,redirect_url,Baidu_login,websocket
from TestWebapp.views import deletefile, stream_video, BingPicture
urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^register', register, name = 'regsiter'),#注册
    url(r'^login', login, name='login'),#登录
    url(r'^jump_register',jump_register, name = 'jum_register'),
    url(r'^videolist',videolist,name='videolist'),
    url(r'^upload_file',upload_file, name='upload_file'),
    url(r'^jump_upload',jump_upload,name='jump_upload'),
    url(r'^textlist',textlist,name='textlist'),
    url(r'^viewtext',viewtext,name='viewtext'),
    url(r'^redirect_url',redirect_url,name='redirect_url'),
    url(r'^Baidu_login',Baidu_login,name='Baidu_login'),
    url(r'websocket',websocket,name='websocket'),
    url(r'^deletefile',deletefile,name='deletefile'),
    url(r'^stream_video',stream_video,name='stream_video'),
    url(r'^BingPicture', BingPicture, name = 'BingPicture'),
]
