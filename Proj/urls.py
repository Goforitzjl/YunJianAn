"""Proj URL Configuration

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
from django.urls import path, re_path
from django.views.static import serve

from Proj import settings
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_valid_image/', views.get_valid_image),  # 获取图形验证码
    path('login/', views.login),  # 登录
    path('register/', views.register),  # 注册
    path('index/', views.index),  # 首页
    path("updatecode/",views.updatecode),  #修改密码
    re_path(r'staff/(?P<keyword>.*)$', views.staff),
    re_path(r'administrator/(?P<keyword>.*)$', views.administrator),
    re_path(r'firm/(?P<keyword>.*)$', views.firm),
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 获取media资源
    # re_path(r'static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),  # 获取static资源

    path('logout/', views.logout),
    path("introduce/",views.introduce)

]
