from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

# manager
from .managers import UserManager

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FilteringResultProductMap(models.Model):
    filtering_result = models.ForeignKey('FilteringResults', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    tea = models.ForeignKey('Teas', models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filtering_result_product_map'


class FilteringResults(models.Model):
    survey_result = models.ForeignKey('SurveyResults', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filtering_results'


class MypageInfo(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    class_field = models.CharField(db_column='class', max_length=255)  # Field renamed because it was a Python reserved word.
    mileage = models.PositiveIntegerField()
    coupon = models.PositiveIntegerField()
    order_history = models.PositiveIntegerField()
    delivery = models.PositiveIntegerField()
    review = models.PositiveIntegerField()
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mypage_info'


class Questionnaires(models.Model):
    version = models.CharField(max_length=255)
    questions = models.CharField(max_length=1000)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionnaires'


class SurveyResults(models.Model):
    survey_responses = models.CharField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaires, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_results'


class Teas(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    flavor = models.CharField(max_length=255, blank=True, null=True)
    caffeine = models.CharField(max_length=45)
    efficacies = models.CharField(max_length=255, blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    site_url = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    stock = models.CharField(max_length=64, blank=True, null=True)
    sell_count = models.PositiveIntegerField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teas'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class UserBuyProduct(models.Model):
    user_id = models.CharField(max_length=255)
    tea = models.ForeignKey(Teas, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_buy_product'


class UserClickProduct(models.Model):
    user_id = models.CharField(max_length=255)
    tea = models.ForeignKey(Teas, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_click_product'


class UserWishProduct(models.Model):
    user_id = models.CharField(max_length=255)
    tea = models.ForeignKey(Teas, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_wish_product'


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True)
    birth = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'users'

class UsersGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    users_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_groups'


class UsersUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    users_id = models.IntegerField(blank=True, null=True)
    permission_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_user_permissions'


# class OutstandingToken(models.Model):
#     id = models.BigAutoField(primary_key=True, serialize=False)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
#     )

#     jti = models.CharField(unique=True, max_length=255)
#     token = models.TextField()
#     created_at = models.DateTimeField(null=True, blank=True)
#     expires_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'token_blacklist_outstandingtoken'


# class BlacklistedToken(models.Model):
#     id = models.BigAutoField(primary_key=True, serialize=False)
#     token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE)
#     blacklisted_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         managed = False
#         db_table = 'token_blacklist_blacklistedtoken'

# admin customizing

class TeasAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'name', 'price', 'stock']
    list_display_links = ['id', 'name']


class SurveyResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'survey_responses']
    list_display_links = ['id', 'user']


class SurveyResults2Admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'survey_responses']
    list_display_links = ['id', 'user']


class FilteringResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'survey_result']
    list_display_links = ['id', 'survey_result']


class FilteringResultProductMapAdmin(admin.ModelAdmin):
    list_display = ['id', 'filtering_result', 'tea']
    list_display_links = ['id', 'filtering_result', 'tea']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'age']
    list_display_links = ['id', 'name']

# Register your models here.
