# from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Users, Teas
import numpy as np
import pandas as pd
import json
import os

# Create your views here.

def index(request):
  print(request)
  return HttpResponse("hello, world. you're at the spolls index.")

def add(request):
  # print(request)

  temps = Teas.objects.all()
  tt = []
  for temp in temps:
    print(temp.name, temp.id)
    tt.append(temp.name)
  print(temps)
  new_entry = Teas(id=4, name="bla", flavor="blaa", caffeine="none", efficacy_num="3", create_date=datetime)
  new_entry.save()
  return HttpResponse("this is add page")

def post_view(request):
  location = os.path.join(os.path.dirname(os.path.dirname(__file__)),'polls/assets/teaable.csv')
  meta = pd.read_csv(location)
  df = pd.DataFrame(meta)
  hyo = '1'
  caff ='X'
  hyang = '2'
  print(df.dtypes)

  df.insert(2,'splithyo',df.효능번호.str.split(','))
  df.insert(5,'splithyang',df.향기준.str.split(','))
  print(df.dtypes)

  def hyo_check(nations):
    n_list = []
    
    for nation in nations:
        if nation == hyo:
            n_list.append(True)
        else:
            n_list.append(False)
            
    if np.sum(n_list)>=1:
        return True
    
    else :
        return False

  def hyang_check(nations):
    n1_list = []
    
    for nation in nations:
        if nation == hyang:
            n1_list.append(True)
        else:
            n1_list.append(False)
            
    if np.sum(n1_list)>=1:
        return True
    
    else :
        return False

  df.splithyo[:10].apply(hyo_check)
  df.splithyang.apply(hyang_check)
  df.splithyo.apply(hyo_check).sum()
  (df.효능번호 =='1').sum()
  df.splithyang.apply(hyang_check).sum()

  cond = (df.splithyo.apply(hyo_check )) 
  cond1 = (df.splithyang.apply(hyang_check ))
  cond2 = df.카페인 == caff
  Kr_df = df[cond &cond1 &cond2]
  print('필터링 출력값: ', Kr_df.shape)
  print('차품목', Kr_df.차품목)
  return HttpResponse(meta)
  # return HttpResponse(temps)
