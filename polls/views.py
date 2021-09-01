# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Users, Teas

# Create your views here.

def index(request):
  print(request)
  return HttpResponse("hello, world. you're at the polls index.")

def post_view(request):
  temps = Teas.objects.all()
  tt = []
  for temp in temps:
    print(temp.name, temp.id)
    tt.append(temp.name)
  print(temps)
  return HttpResponse(tt)
  # return HttpResponse(temps)
