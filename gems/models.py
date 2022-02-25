from django.db import models
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .generator import token_generator
from django.utils.translation import ugettext_lazy as _
import datetime
datetime.date.today()
import boto3
from decouple import config, Csv



class gemsMeta(models.Model):
    metaID = models.IntegerField(default = 0,
                               blank=True,
                               null=True)
    name = models.CharField(max_length=150,
                              blank=True,
                              null=True)
    description = models.CharField(max_length=500,
                              blank=True,
                              null=True)
    image_file = models.FileField(upload_to='gems/',
                              blank=True,
                              null=True)
    image = models.CharField(max_length=35000,
                              blank=True,
                              null=True)
    background = models.IntegerField(default = 0,
                               blank=True,
                               null=True)
    is_anon = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % (self.metaID)

class twitterConnection(models.Model):
    meta_data = models.ForeignKey(gemsMeta,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    twitter = models.CharField(max_length=150,
                              blank=True,
                              null=True)
    user_id= models.CharField(max_length=100)
    twitter_ref = models.CharField(max_length=30,
                              blank=True,
                              null=True)
    last_updated = models.DateTimeField(blank=True,
                              null=True)

    def save(self, *args, **kwargs):
        # This to check if it creates a new or updates an old instance
        if self.pk is None:
            self.twitter_ref = token_generator.make_token(8)
        super(twitterConnection, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.twitter)


class TwitterToken(models.Model):
    session_id = models.CharField(max_length=50, unique=True)
    oauth_token= models.CharField(max_length=150)
    oauth_secret= models.CharField(max_length=150)
    user_id= models.CharField(max_length=100)
    user_name= models.CharField(max_length=100)