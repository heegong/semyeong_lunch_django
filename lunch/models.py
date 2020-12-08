from django.db import models

# Create your models here.
class user_info(models.Model):
    user_ip = models.CharField(max_length=50)
    connect_time = models.CharField(max_length=50)


class lunch_log(models.Model):
    log_time = models.CharField(max_length=50)
    today_lunch = models.TextField()