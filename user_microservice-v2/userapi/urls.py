from django.urls import path
from userapi import views

urlpatterns = [
    path('api/v1/db/read', views.readDb, name='read'),
    path('api/v1/db/write', views.writeDb, name='write'),
    path('api/v1/users', views.createUser, name='createUser'),
    path('api/v1/users/<str:username>', views.removeUser, name='removeUser'),
    path('api/v1/db/clear', views.clearDb, name='clear'),
    path('api/v1/_count', views.countHttp, name='countHttpRequests')
]
