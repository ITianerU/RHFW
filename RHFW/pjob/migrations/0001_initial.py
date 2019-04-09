# Generated by Django 2.2 on 2019-04-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=20, verbose_name='区')),
                ('salary', models.CharField(max_length=20, verbose_name='薪资')),
                ('eduction', models.CharField(max_length=10, verbose_name='学历')),
                ('exp', models.CharField(max_length=20, verbose_name='经验')),
                ('position', models.CharField(max_length=20, verbose_name='职位')),
            ],
        ),
    ]