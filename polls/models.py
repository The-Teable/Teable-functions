from django.db import models


class Questionnaires(models.Model):
    version = models.CharField(max_length=255)
    questions = models.CharField(max_length=1000)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionnaires'


class SurveyResults(models.Model):
    survey_responses = models.CharField(max_length=5000)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaires, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'survey_results'
        unique_together = (('id', 'user', 'questionnaire'),)


class Teas(models.Model):
    name = models.CharField(max_length=255)
    flavor = models.CharField(max_length=255, blank=True, null=True)
    caffeine = models.CharField(max_length=45)
    efficacy_num = models.PositiveIntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teas'


class UserLikedTeaMap(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    tea = models.ForeignKey(Teas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_liked_tea_map'
        unique_together = (('user', 'tea'),)


class UserWantTeaMap(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    tea = models.ForeignKey(Teas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_want_tea_map'
        unique_together = (('user', 'tea'),)


class Users(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'