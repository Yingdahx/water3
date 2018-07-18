"""water URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from water_app import views
from django.conf.urls import url

# from apscheduler.schedulers.blocking import  BlockingScheduler
from water_app.management.commands import day

import debug_toolbar

urlpatterns = [
    
    path('admin/', admin.site.urls),

    #警报
    path('all/',views.all),
    #6个模块
    #社区页面
    path('',views.com_login),
    path('com_login/',views.com_login),
    path('com_index/',views.com_index),
    path('information/',views.information),
    path('login_out', views.login_out),
    #
    path('index/',views.index),
    path('day/',views.day),
    path('police_day/',views.police_day),
    path('month/',views.month),
    path('police_month/',views.police_month),
    path('Week/',views.Week),
    path('police_Week/',views.police_Week),

    #子页面
    url(r'^details/$',views.details), 
    #文章方面的接口
    path('article/',views.article),

    #用户和权限
    path('member/',views.member),
    #物品类型
    path('equipmentType/',views.equipmentType),

    #数据获取接收测试
    path('login/',views.login),
    path('getdata/',views.getdata),
    path('analysis/',views.analysis),
    path('api/data/push/',views.push),
    path('api/data/push/v2/',views.pushv2),


    # 公告接口 && 接口规范
    # insert/condition(0)/obj && select/condition/ && update/condition/obj && delete/condition/
    url(r'^notice/(?P<action>insert|delete|update|select)/$', views.notice, name='notice'),
    # 区域管理接口
    url(r'(?P<model>area|street|village)/(?P<action>insert|select|delete|update)/$',views.place,name='place'),
    # 
    path('getProvince/',views.getProvince),

    # demo
    url(r'^demo/(?P<haha>.+)/$',views.demo),

    url(r'^__debug__/', include(debug_toolbar.urls)),

    #app接口
    path('notices_list/',views.notices_list),
    path('knowledge_list/',views.knowledge_list),
    path('event_list/',views.event_list),
    path('app_login/',views.app_login),
    path('password_change/',views.password_change),
    path('chang_get_code/',views.chang_get_code),
    path('phone_change/',views.phone_change),
    path('suggestion/',views.suggestion),
    path('knowledge_detail/',views.knowledge_detail),
    path('get_code/',views.get_code),
    path('login_by_phone/',views.login_by_phone),
    path('user/',views.user),
    path('nervous_list/',views.nervous_list),
    path('check_fire/',views.check_fire),
    path('message_list/',views.message_list),
    path('user_change/',views.user_change),
    path('event_type/',views.event_type),
    path('event_detail/',views.event_detail),
    path('login_out/',views.login_out),
    path('auto_login/',views.auto_login),

    
    
   
    


    #test
    
    path('testPic/',views.testPic),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#定时任务
# sched = BlockingScheduler()
# sched.add_job(day.test, 'interval', seconds=5)
# sched.start()
