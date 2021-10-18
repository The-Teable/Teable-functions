from django.urls import path

from . import views
urlpatterns = [
  path('', views.index, name='index'),
  path('post/', views.post_view),
  path('add/', views.add),
]