from django.db import models

# Create your models here.
class Job(models.Model):
    area = models.CharField(verbose_name="区", max_length=20)
    salary = models.CharField(verbose_name="薪资", max_length=20)
    eduction = models.CharField(verbose_name="学历", max_length=10)
    exp = models.CharField(verbose_name="经验", max_length=20)
    position = models.CharField(verbose_name="职位", max_length=20)
