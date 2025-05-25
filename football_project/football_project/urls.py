"""
URL configuration for football_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls import include
from football.views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    # 注册的
    path('register/', register,name='register'),
    path('register/submit/', submit,name='submit'),

    # 讨论区的
    path('home/discuss/', discussion_list,name='discussion_list'), 
    path('like_article/', like_article,name='like_article'),
    path('home/discuss/<int:article_id>/', article_detail, name='article_detail'),

    # 约战的
    path('home/battle/', battle_view,name='battle_view'),

    # === 新增赛事直播 URL ===
    path('home/live/', live_streams_view, name='live_streams'),

    # === 新增足球文化-简史 URL ===
    path('home/culture/history/', culture_history_view, name='culture_history'),

    # 大数据
    path('home/bigdata/', bigdata_view, name='bigdata_view'),
    
    # 登录的
    path('', login,name='login'),
    path('home/', index,name='index'),  

    # === 新增创建约战 和 查看我的约战 URLs ===
    path('home/battle/create/', create_match_view, name='create_match'),
       # 查看我的约战列表 (我报名的)
    path('home/battle/my_matches/', my_matches_view, name='my_matches'),
    # 查看我发布的约战列表
    path('home/battle/my_matches/created/', my_created_matches_view, name='my_created_matches'),
    path('home/battle/signup/', battle_signup_submit, name='battle_signup_submit'), # 处理报名模态框提交的 URL
    # 新增查看我的约战详情页面 (包含报名者列表)

    path('home/battle/my_matches/<int:match_id>/', my_match_detail_view, name='my_match_detail'),

    # 删除约战 URL (处理 POST 请求)
    path('home/battle/delete/<int:match_id>/', delete_match_view, name='delete_match'),

    # === 新增足球文化介绍详情 URL ===
    path('home/culture/', culture_detail_view, name='culture_detail'),
    # === 新增发表帖子 URL ===
    path('home/discuss/create/', create_article_view, name='create_article'),


]
