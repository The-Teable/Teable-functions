from django.urls import path, include, re_path
from django.contrib import admin
<<<<<<< Updated upstream
from polls.views import TeaListAPI, put
=======
from polls.views import TeaListAPI
from django.views.generic import TemplateView
>>>>>>> Stashed changes

from . import views


class HomeTemplateView(TemplateView):
    template_name = 'index.html'


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
    path('post/', views.post_view),
    path('api/tea/', TeaListAPI.as_view()),
    path('api/email/', put)
]
