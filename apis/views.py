# from django.shortcuts import render
from datetime import datetime, timezone
from email import header
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from sqlalchemy import JSON
from apis.serializers import FilteringResultsSerializer, MainFilteringResultsSerializer, QuestionnairesSerializer, SurveyResultSerializer, ThemeFilteringSerializer, BestSellingSerializer, UserSerializer, UserBuyProductSerializer, UserClickProductSerializer
from .models import FilteringResultProductMap, FilteringResults, Questionnaires, SurveyResults, Teas, Users, UserBuyProduct, UserClickProduct
# import import_ipynb
# import filtering_algorithm
from .lib import common_filtering
from rest_framework.views import APIView
from rest_framework import viewsets
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from rest_framework import serializers
import csv
from django.core import serializers as djangoSerializers
import json

# 테마 필터링 알고리즘
from .lib import theme_filtering, bestselling_filtering, teave_filtering

# Create your views here.


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


def index(request):
    return HttpResponse("hello, we are pirates")


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'user_id': created_instance.id}, status=200, headers=headers)

    def get_object(self):
        pk = self.kwargs['userId'] if self.kwargs else None
        queryset = self.filter_queryset(self.get_queryset())
        if pk:
            obj = queryset.get(pk=pk)
            return obj
        return queryset


class SurveyResultsView(viewsets.ModelViewSet):
    queryset = SurveyResults.objects.all()
    serializer_class = SurveyResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'survey_id': created_instance.id}, status=200, headers=headers)

    def get_queryset(self):
        user_id = self.kwargs['userId'] if self.kwargs else None
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

# 설문조사 결과
# class SurveyResults2View(viewsets.ModelViewSet):
#     queryset = SurveyResults2.objects.all()
#     serializer_class = SurveyResult2Serializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         created_instance = serializer.save()
#         headers = self.get_success_headers(serializer.data)
#         return Response({'survey_id': created_instance.id}, status=200, headers=headers)

#     def get_queryset(self):
#         user_id = self.kwargs['userId'] if self.kwargs else None
#         if user_id:
#             return SurveyResults.objects.filter(user_id=user_id)
#         return super().get_queryset()

#     def get_object(self):
#         pk = self.kwargs['pk'] if self.kwargs else None
#         queryset = self.filter_queryset(self.get_queryset())
#         if (len(queryset) > 0) and (self.request.query_params.get('surveyId')):
#             obj = queryset.get(pk=self.request.query_params.get('surveyId'))
#             return obj
#         if pk:
#             obj = queryset.get(pk=pk)
#             return obj
#         return queryset


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
                            'image_url': tea.image_url, 'site_url': tea.site_url, 'price': tea.price, 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
            return Response(teas)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        return Response({'filtering_id': created_instance.id}, status=200)

# 메인페이지에서 보여주는 Tea 추천 결과
class MainFilteringResultView(viewsets.ModelViewSet):
    queryset = Teas.objects.all()
    serializer_class = MainFilteringResultsSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id'] if self.kwargs else None
        if user_id:
            teave_filtering_result_map = teave_filtering(user_id)
            teas = []
            for result in teave_filtering_result_map:
                tea_id = result.tea_id
                tea = Teas.objects.get(id=tea_id)
                teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                            'image_url': tea.image_url, 'site_url': tea.site_url, 'price': tea.price, 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
            return Response(teas)

class ThemeFilteringView(viewsets.ModelViewSet):
    queryset = Teas.objects.all()
    serializer_class = ThemeFilteringSerializer

    def list(self, request, *args, **kwargs):
        theme = self.kwargs['theme'] if self.kwargs else None
        if theme:
            theme_filtering_result_map = theme_filtering(theme)
            teas = []
            for result in theme_filtering_result_map:
                tea_id = result.tea_id
                tea = Teas.objects.get(id=tea_id)
                teas.append({"id": tea.id, "name": tea.name, "brand": tea.brand, 'type': tea.type, 'flavor': tea.flavor, 'caffeine': tea.caffeine, 'efficacies': tea.efficacies,
                            'image_url': tea.image_url, 'site_url': tea.site_url, 'price': tea.price, 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
            return Response(teas)

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
                        'image_url': tea.image_url, 'site_url': tea.site_url, 'price': tea.price, 'stock': tea.stock, 'create_date': tea.create_date, 'update_date': tea.update_date})
        return Response(teas)

class UserBuyProductView(viewsets.ModelViewSet):
    queryset = UserBuyProduct.objects.all()
    serializer_class = UserBuyProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save(user_id = request.data['user_id'], tea_id = request.data['tea_id'])
        for tea_id in request.data['tea_id']:
            tea = Teas.objects.get(id=tea_id)
            Teas.objects.filter(id=tea_id).update(sell_count = tea.sell_count + 1)
        return Response({'user_buy_product_id': created_instance.id}, status=200)
        
class UserClickProductView(viewsets.ModelViewSet):
    queryset = UserClickProduct.objects.all()
    serializer_class = UserClickProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save(user_id = request.data['user_id'], tea_id = request.data['tea_id'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'user_click_product_id': created_instance.id}, status=200, headers=headers)