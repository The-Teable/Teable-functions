from django.contrib import admin
from . import models

# admin customizing


class TeasAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name']

# Register your models here.


admin.site.register(models.FilteringResultProductMap)
admin.site.register(models.FilteringResults)
admin.site.register(models.Questionnaires)
admin.site.register(models.SurveyResults)
admin.site.register(models.Teas, TeasAdmin)
admin.site.register(models.Users)
admin.site.register(models.DjangoSession)
admin.site.register(models.DjangoMigrations)
admin.site.register(models.AuthGroup)
admin.site.register(models.AuthGroupPermissions)
admin.site.register(models.AuthPermission)
admin.site.register(models.AuthUser)
admin.site.register(models.AuthUserGroups)
admin.site.register(models.DjangoAdminLog)
admin.site.register(models.DjangoContentType)
admin.site.register(models.AuthUserUserPermissions)
