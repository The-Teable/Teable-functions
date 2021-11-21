from django.contrib import admin
from . import models


admin.site.register(models.FilteringResultProductMap,
                    models.FilteringResultProductMapAdmin)
admin.site.register(models.FilteringResults, models.FilteringResultsAdmin)
admin.site.register(models.Questionnaires)
admin.site.register(models.SurveyResults, models.SurveyResultsAdmin)
admin.site.register(models.SurveyResults2, models.SurveyResults2Admin)
admin.site.register(models.Teas, models.TeasAdmin)
admin.site.register(models.Users, models.UsersAdmin)
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
