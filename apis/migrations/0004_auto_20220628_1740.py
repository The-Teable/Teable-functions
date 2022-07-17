# Generated by Django 3.1.6 on 2022-06-28 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_userbuyproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserClickProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_click_product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserWishProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_wish_product',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='SurveyResults2',
        ),
    ]