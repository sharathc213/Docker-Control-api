from . import views
from django.contrib import admin
from django.urls import path,include



urlpatterns = [
   path('',views.apiOverview,name='apiOverview'),
   path('getimages',views.getImages,name='getImages'),
   path('startimage',views.startImage,name='startImage'),
   path('getcontainers',views.getContainers,name='getContainers'),
   path('startcontainer',views.startContainer,name='startContainer'),
   path('stopcontainer',views.stopContainer,name='stopContainer'),
   path('deletecontainer',views.deleteContainer,name='deleteContainer'),
   path('deletecontainers',views.deleteContainers,name='deleteContainers'),
   #  path('deletei',views.deletei,name='deletei'),
   #  path('containers',views.container,name='container'),
   #  path('getcontainers',views.getcontainers,name='getcontainers'),
   #  path('getimages',views.getimages,name='getimages'),
   #  path('stopc',views.stopc,name='stopc'),
   #  path('deletec',views.deletec,name='deletec'),
   #  path('console',views.console,name='console'),
   #  path('startc',views.startc,name='startc'),
   
]
