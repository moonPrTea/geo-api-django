from django.contrib import admin
from django.urls import path

from geoapi.views import LoginApi, LogoutApi, PointsCreateApi, PointsSearchApi, MessageCreateApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/login', LoginApi.as_view()), 
    path('api/accounts/logout', LogoutApi.as_view()),
    path('api/points', PointsCreateApi.as_view()),
    path('api/points/search', PointsSearchApi.as_view()),
    path('api/points/messages', MessageCreateApi.as_view())
]
