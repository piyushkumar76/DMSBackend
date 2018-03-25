
from django.contrib import admin
from django.urls import path
from serve import views as Sviews
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse


urlpatterns = [
    path('StationInsert/',Sviews.StationInsert),
    path('RequestInsert/',Sviews.RequestInsert),
    path('GetRequests/',Sviews.GetRequests),
    path('GetStations/',Sviews.GetStations),
    path('Login/',Sviews.Login),
    path('Logout/',Sviews.Logout),
    path('AcceptRequest/',Sviews.AcceptRequest),
    path('GetPastRequests/',Sviews.GetPastRequests),
    path('GetSingleRequest/', Sviews.GetSingleRequest),
    path('admin/', admin.site.urls),


#### URLs To handle Redis ####
    path('SeeRedis/',lambda request : render(request, 'SeeRedis.html', {'table':[{'key':i,'value':cache.get(i),'ttl':str(cache.ttl(i))} for i in cache.keys('*')]})),
    path('EmptyRedis/', lambda request: render(request,'SeeRedis.html',{'eval':cache.clear()})),
    path('RemoveFromRedis/<key>', lambda request,key: render(request,'SeeRedis.html',{'eval':cache.delete(key)})),
    path('SetInRedis/<key>/<value>', lambda request, key,value: render(request, 'SeeRedis.html', {'eval':cache.set(key,value)}))
]
