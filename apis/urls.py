from django.urls import path, include
from django.contrib import admin
from django.urls.conf import re_path
# from apis.views import send_email
from .views import FilteringResultsView, QuestionnairesView, SendEmail, SurveyResultsView, UsersView, UserBuyProductView, UserClickProductView
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

users_list = UsersView.as_view({
    'post': 'create',
})

users_detail = UsersView.as_view({
    'put': 'update',
})

survey_results_create = SurveyResultsView.as_view({
    # 'get': 'list',
    'post': 'create',
})

survey_results_update = SurveyResultsView.as_view({
    # 'get': 'list',
    'put': 'update',
    'patch': 'partial_update'
})

survey_results_per_user = SurveyResultsView.as_view({
    'get': 'list'
})

survey_results_detail = SurveyResultsView.as_view({
    'get': 'retrieve'
})

# survey_results_2_create = SurveyResults2View.as_view({
#     # 'get': 'list',
#     'post': 'create',
# })

# survey_results_2_update = SurveyResults2View.as_view({
#     # 'get': 'list',
#     'put': 'update',
#     'patch': 'partial_update'
# })

# survey_results_2_per_user = SurveyResults2View.as_view({
#     'get': 'list'
# })

# survey_results_2_detail = SurveyResults2View.as_view({
#     'get': 'retrieve'
# })


questionnaires_list = QuestionnairesView.as_view({
    'get': 'list'
})

filtering_results_list = FilteringResultsView.as_view({
    'post': 'create',
})

filtering_results_detail = FilteringResultsView.as_view({
    'get': 'list'
})

user_buy_product_create = UserBuyProductView.as_view({
    'post': 'create',
})

user_click_product_create = UserClickProductView.as_view({
    'post': 'create',
})

send_email_list = SendEmail.as_view()

urlpatterns = format_suffix_patterns([
    path('', views.index),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    # users
    path('users/new/', users_list, name='users_list'),
    re_path('users/(?P<userId>.+)/$', users_detail, name="users_detail"),
    
    # survey_results
    path('survey-results/all/', survey_results_per_user, name='survey_results_per_user'),
    re_path('survey-results/all/(?P<userId>.+)/$', survey_results_per_user, name='survey_results_per_user'),
    path('survey-results/<int:pk>/', survey_results_detail, name='survey_results_list'),
    path('survey-results/new/', survey_results_create, name='survey_results_create'),
    path('survey-results/update/', survey_results_update, name='survey_results_update'),

    # survey_results_2
    # path('survey-results-2/all/', survey_results_2_per_user, name='survey_results_2_per_user'),
    # re_path('survey-results-2/all/(?P<userId>.+)/$', survey_results_2_per_user, name='survey_results_2_per_user'),
    # path('survey-results-2/<int:pk>/', survey_results_2_detail, name='survey_results_2_list'),
    # path('survey-results-2/new/', survey_results_2_create, name='survey_results_2_create'),
    # path('survey-results-2/update/', survey_results_2_update, name='survey_results_2_update'),

    # questionnaires
    re_path('^questionnaires/', questionnaires_list, name='questionnaires_list'),
    re_path('^questionnaires/(?P<version>.+)/$', questionnaires_list, name='questionnaires_list'),

    # filtering_results
    path('filtering-results/new/', filtering_results_list, name='filtering_results_list'),
    re_path('filtering-results/(?P<filteringId>.+)/$', filtering_results_detail, name='filtering_results_detail'),

    # user_buy_product
    path('user-buy-product/new/', user_buy_product_create, name='user_buy_product_create'),

    # user_click_product
    path('user-click-product/', user_buy_click_create, name='user_click_product_create'),

    # sending email
    path('send-email/', send_email_list, name='send_email_list'),

])
