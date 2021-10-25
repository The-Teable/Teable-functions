from django.urls import path
from django.contrib import admin
from polls.views import TeaListAPI

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post_view),
    path('api/tea/', TeaListAPI.as_view()),
]
