# from django.shortcuts import render
from datetime import datetime, timezone
from email import header
from urllib import response
from urllib.request import Request
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
import jwt
import my_settings
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from sqlalchemy import JSON, false
from apis.serializers import (
    MyPageInfoSerializer, SignUpSerializer, LogInSerializer,
    FilteringResultsSerializer, MainFilteringResultsSerializer, QuestionnairesSerializer, SurveyResultSerializer, 
    ThemeFilteringSerializer, BestSellingSerializer, UserSerializer, UserBuyProductSerializer, UserWishProductSerializer,
    UserClickProductSerializer
)
from .models import FilteringResultProductMap, FilteringResults, MypageInfo, Questionnaires, SurveyResults, Teas, Users, UserBuyProduct, UserClickProduct, UserWishProduct
# import import_ipynb
# import filtering_algorithm
from .lib import common_filtering, theme_filtering
from rest_framework.views import APIView
from rest_framework import viewsets, generics, serializers
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import csv
from django.core import serializers as djangoSerializers
import json

# django auth
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated


# 필터링 알고리즘
from .lib import theme_filtering, bestselling_filtering, teave_filtering

# Create your views here.

# send email
class SendEmail(APIView):
    def get(self, serializer):
        return Response("이메일 전송 API", status=200)

    def post(self, serializer):
        data = self.request.data
        try:
            toEmail = data['to_email']
            fromEmail = data['from_email']
            TitleEmail = data["title"]
            ContentEmail = data['content']

            msg = MIMEText(ContentEmail)
            msg['From'] = fromEmail
            msg['To'] = toEmail
            msg['Subject'] = TitleEmail

            # Daum SMTP
            conn = SMTP_SSL("smtp.daum.net:465")
            conn.ehlo()

            loginId = 'connect@teave.co.kr'
            loginPassword = 'ekdmadyd1!'
            conn.login(loginId, loginPassword)

            conn.sendmail(fromEmail, toEmail, msg.as_string())
            conn.close()
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response(e, status=500)

# django auth
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = LogInSerializer
    
class SignUpView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    # id duplicate check
    def check(self, request, *args, **kwargs):
        is_duplicate = False
        user_id = request.GET['user_id']
        if user_id:
            if Users.objects.filter(user_id = user_id).exists():
                is_duplicate = True
            return Response({'is_duplicate' : is_duplicate}, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        MypageInfo.objects.create(user_id = request.data['user_id'], user_class='녹차', create_date = datetime.now())
        return Response(status=201, headers=headers)

class LogInView(viewsets.ModelViewSet):
    serializer_class = LogInSerializer

    def Login(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        access = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        res = JsonResponse({
            # 'user' : (model_to_dict(user)),
            'access' : access,
        })
        res.set_cookie('refresh', refresh, secure=True, httponly=True)
        return res

class MyPageInfoView(viewsets.ModelViewSet):
    queryset = MypageInfo.objects.all()
    serializer_class = MyPageInfoSerializer

    def list(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        if user_id:
            mypage = MypageInfo.objects.filter(
                user_id=user_id)
            mypage_info = []
            mypage_info.append({"user_class": mypage.user_class, "mileage": mypage.mileage, "coupon": mypage.coupon, 'order_history': mypage.order_history, 'delivery': mypage.delivery, 'review': mypage.review})
            return Response(mypage_info)


class SurveyResultsView(viewsets.ModelViewSet):
    queryset = SurveyResults.objects.all()
    serializer_class = SurveyResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'survey_id': created_instance.id}, status=201, headers=headers)

    def get_queryset(self):
        user_id = self.kwargs['user_id'] if self.kwargs else None
        if user_id:
            return SurveyResults.objects.filter(user_id=user_id)
        return super().get_queryset()

    def get_object(self):
        pk = self.kwargs['pk'] if self.kwargs else None
        queryset = self.filter_queryset(self.get_queryset())
        if (len(queryset) > 0) and (self.request.query_params.get('surveyId')):
            obj = queryset.get(pk=self.request.query_params.get('surveyId'))
            return obj
        if pk:
            obj = queryset.get(pk=pk)
            return obj
        return queryset

class QuestionnairesView(viewsets.ModelViewSet):
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesSerializer

    def get_queryset(self):
        version = self.kwargs['version'] if self.kwargs else None
        if version:
            return Questionnaires.objects.filter(version=version)
        return super().get_queryset()

# tea Test 결과
class FilteringResultsView(viewsets.ModelViewSet):
    queryset = FilteringResults.objects.all()
    serializer_class = FilteringResultsSerializer

    def list(self, request, *args, **kwargs):
        filtering_result_id = self.kwargs['filteringId'] if self.kwargs else None
        if filtering_result_id:
            result_map = FilteringResultProductMap.objects.filter(
                filtering_result_id=filtering_result_id)
            teas = []
            for result in result_map:
                tea_id = result.tea_id
                tea = Teas.objects.get(id=tea_id)
                teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                            'image_url': tea.image_url, 'site_url': tea.site_url, 'price': int(tea.price), 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
            return Response(teas)

    def create(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        request.data['user_id'] = user_id
        print(request.data) # user_id를 header에서 받아오려고 함.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        return Response({'filtering_id': created_instance.id}, status=201)

# 메인페이지에서 보여주는 Tea 추천 결과
class MainFilteringResultView(viewsets.ModelViewSet):
    queryset = Teas.objects.all()
    serializer_class = MainFilteringResultsSerializer

    def list(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        if user_id:
            teave_filtering_result_map = teave_filtering.get_filtering_tea(user_id)
            teas = []
            for result in teave_filtering_result_map['tea_id']:
                tea_id = result
                tea = Teas.objects.get(id=tea_id)
                teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 
                            'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                            'price': int(tea.price)})
            return Response(teas)

class ThemeFilteringView(viewsets.ModelViewSet):
    queryset = Teas.objects.all()
    serializer_class = ThemeFilteringSerializer

    def list(self, request, *args, **kwargs):
        theme_list = ['winter']
        tea_list = []
        for theme in theme_list:
            theme_filtering_result_map = theme_filtering.theme_filtering(theme)
            teas = {}
            teas['theme'] = theme
            teas['tea_info'] = []
            print(theme_filtering_result_map)
            for i in range(len(theme_filtering_result_map)):
                result = theme_filtering_result_map.iloc[i]
                teas['tea_info'].append(({"id": result['id'], "name": result['name'], "brand": result.brand, 'type': result.type, 'flavor': result.flavor, 'caffeine': result.caffeine, 'efficacies': result.efficacies,
                            'image_url': result.image_url, 'price': int(result.price), 'stock': result.stock}))
            tea_list.append(teas)
        return Response(tea_list)


class BestSellingView(viewsets.ModelViewSet):
    queryset = Teas.objects.all()
    serializer_class = BestSellingSerializer

    def list(self, request, *args, **kwargs):
        bestselling_filtering_result_map = bestselling_filtering()
        teas = []
        for result in bestselling_filtering_result_map:
            tea_id = result.tea_id
            tea = Teas.objects.get(id=tea_id)
            teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                        'image_url': tea.image_url, 'site_url': tea.site_url, 'price': int(tea.price), 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
        return Response(teas)

class UserBuyProductView(viewsets.ModelViewSet):
    queryset = UserBuyProduct.objects.all()
    serializer_class = UserBuyProductSerializer

    def create(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id = user_id, tea_id = request.data['tea_id'])
        self.perform_create(serializer)
        return Response(status=201)
        
class UserClickProductView(viewsets.ModelViewSet):
    queryset = UserClickProduct.objects.all()
    serializer_class = UserClickProductSerializer

    def create(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save(user_id = user_id, tea_id = request.data['tea_id'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'user_click_product_id': created_instance.id}, status=201, headers=headers)

class UserWishProductView(viewsets.ModelViewSet):
    queryset = UserWishProduct.objects.all()
    serializer_class = UserWishProductSerializer

    # def info(self, request, *args, **kwargs):
    #     # user_id = self.kwargs['user_id'] if self.kwargs else None
    #     # if user_id:
    #     #     result_map = UserWishProduct.objects.filter(user_id=user_id)
    #     #     tea_ids = []
    #     #     for tea_id in result_map['tea_id']:
    #     #         tea_ids.append(int(tea_id))
    #     #     return Response(tea_ids)

    def list(self, request, *args, **kwargs):
        user_id = request.GET['user_id']
        if user_id:
            result_map = UserWishProduct.objects.filter(user_id=user_id)
            teas = []
            for tea_id in result_map['tea_id']:
                tea = Teas.objects.get(id=tea_id)
                teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 
                            'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                            'price': int(tea.price)})
            return Response(teas)

    def create(self, request, *args, **kwargs):
        token_str = str.replace(request.headers['Authorization'], 'Bearer ', '')
        payload = jwt.decode(token_str, my_settings.SECRET_KEY , algorithms=['HS256'])
        user_id = payload['user_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save(user_id = user_id, tea_id = request.data['tea_id'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'user_wish_product_id': created_instance.id}, status=201, headers=headers)


    def delete(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        tea_id = request.data['tea_id']
        data = UserWishProduct.objects.get(user_id=user_id, tea_id=tea_id)
        data.delete()
        return Response(status=204)

def index(request):
    return HttpResponse("hello, we are pirates")