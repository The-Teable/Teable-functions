from django.db import models
from django.contrib import admin


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
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
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
    tea = models.ForeignKey('Teas', models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filtering_result_product_map'


class FilteringResults(models.Model):
    survey_result = models.OneToOneField('SurveyResults', models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filtering_results'


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
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaires, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'survey_results'


class SurveyResults2(models.Model):
    survey_responses = models.CharField(max_length=5000, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaires, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'survey_results_2'


class Teas(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    flavor = models.CharField(max_length=255, blank=True, null=True)
    caffeine = models.CharField(max_length=45)
    efficacies = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    site_url = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    stock = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teas'


class Users(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

# admin customizing


class TeasAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'name', 'price']
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
