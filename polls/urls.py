from django.urls import path, include, re_path
from django.contrib import admin
from polls.views import TeaListAPI, put
from django.views.generic import TemplateView
from . import views


class HomeTemplateView(TemplateView):
    template_name = 'index.html'


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
    path('post/', views.post_view),
    path('api/tea/', TeaListAPI.as_view()),
    path('api/email/', put)
]
