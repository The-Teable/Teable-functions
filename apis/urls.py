from django.urls import path, include
from django.contrib import admin
from django.urls.conf import re_path

from apis.models import Users
# from apis.views import send_email
from .views import (
    FilteringResultsView, MainFilteringResultView, MyPageInfoView, 
    QuestionnairesView, SendEmail, 
    SurveyResultsView, UsersView, 
    UserBuyProductView, UserClickProductView, UserWishProductView,
    ThemeFilteringView, BestSellingView, 
    #auth
    MyTokenObtainPairView, SignUpView, LogInView
    )
from rest_framework.urlpatterns import format_suffix_patterns

# django auth
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView, TokenBlacklistView
)

from . import views

# sign up
signup_check = SignUpView.as_view({
    'get': 'check',
})

signup_create = SignUpView.as_view({
    'post': 'create',
})

login = LogInView.as_view({
    'post' : 'Login',
})

mypage_info_list = MyPageInfoView.as_view({
    'get': 'list',
})

users_list = UsersView.as_view({
    'get': 'list',
})

users_update = UsersView.as_view({
    'put': 'update',
})

survey_results_create = SurveyResultsView.as_view({
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

questionnaires_list = QuestionnairesView.as_view({
    'get': 'list'
})

filtering_results_detail = FilteringResultsView.as_view({
    'post': 'create',
})

filtering_results_list = FilteringResultsView.as_view({
    'get': 'list'
})

main_filtering_results_list = MainFilteringResultView.as_view({
    'get': 'list'
})

theme_filtering_list = ThemeFilteringView.as_view({
    'get': 'list'
})

bestselling_filtering_list = BestSellingView.as_view({
    'get': 'list'
})

user_buy_product_create = UserBuyProductView.as_view({
    'post': 'create',
})

user_click_product_create = UserClickProductView.as_view({
    'post': 'create',
})

user_wish_product_create = UserWishProductView.as_view({
    'post': 'create',
})

user_wish_product_delete = UserWishProductView.as_view({
    'post': 'delete',
})

user_wish_product_list = UserWishProductView.as_view({
    'get': 'list',
})

user_wish_product_info = UserWishProductView.as_view({
    'get': 'info',
})

send_email_list = SendEmail.as_view()

urlpatterns = format_suffix_patterns([

    # main
    path('', views.index, name = 'main'),

    # auth token
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # auth login/logout
    path('login/', login, name='login'),
    path('logout/', TokenBlacklistView.as_view(), name = 'logout'),

    # mypage
    path('mypage-info/', mypage_info_list, name = 'mypage_info_list'),
    re_path('mypage-info/(?P<user_id>.+)/$', mypage_info_list, name = 'mypage_info_list'),

    # auth signup
    path('signup/', signup_create, name='signup_create'),
    path('signup/check/', signup_check, name = 'signup_check'),
    re_path('signup/check/(?P<user_id>.+)/$', signup_check, name = 'signup_check'),

    # users
    path('users/', users_list, name="users_list"),
    path('users/update/', users_update, name="users_update"),
    
    # survey_results
    path('survey-results/', survey_results_per_user, name='survey_results_per_user'),
    re_path('survey-results/(?P<user_id>.+)/$', survey_results_per_user, name='survey_results_per_user'),
    path('survey-results/<int:pk>/', survey_results_detail, name='survey_results_list'),
    path('survey-results/', survey_results_create, name='survey_results_create'),
    path('survey-results/update/', survey_results_update, name='survey_results_update'),


    # questionnaires
    re_path('^questionnaires/', questionnaires_list, name='questionnaires_list'),
    re_path('^questionnaires/(?P<version>.+)/$', questionnaires_list, name='questionnaires_list'),

    # filtering_results
    path('filtering-results/new/', filtering_results_detail, name='filtering_results_detail'),
    re_path('filtering-results/(?P<filteringId>.+)/$', filtering_results_list, name='filtering_results_list'),

    # main_filtering_results
    path('main-filtering-results/',main_filtering_results_list, name='main_filtering_results_list'),
    re_path('main-filtering-results/(?P<user_id>.+)/$',main_filtering_results_list, name='main_filtering_results_list'),

    # theme_filtering
    path('theme-filtering/', theme_filtering_list, name='theme_filtering_list'),

    # bestselling_filtering
    path('best-selling/', bestselling_filtering_list, name='bestselling_filtering_list'),

    # user_buy_product
    path('user-buy-product/', user_buy_product_create, name='user_buy_product_create'),

    # user_click_product
    path('user-click-product/', user_click_product_create, name='user_click_product_create'),

    # user_wish_product
    path('user-wish-product/', user_wish_product_create, name='user_wish_product_create'),
    path('user-wish-product/delete/', user_wish_product_delete, name='user_wish_product_delete'),
    path('user-wish-product/', user_wish_product_list, name='user_wish_product_list'),
    re_path('user-wish-product/(?P<user_id>.+)/$', user_wish_product_list, name='user_wish_product_list'),
    path('user-wish-product/info/', user_wish_product_info, name='user_wish_product_info'),

    # sending email
    path('send-email/', send_email_list, name='send_email_list'),

])
