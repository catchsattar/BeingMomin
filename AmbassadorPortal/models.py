# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

User.add_to_class('mobile_no', models.CharField(max_length=13, default=None, blank=False, unique=True))
User.add_to_class('qualification', models.CharField(max_length=400, default=None))
User.add_to_class('address', models.TextField(max_length=500, blank=True))
User.add_to_class('mobile_verified', models.BooleanField(default=False))
User.add_to_class('finalized', models.BooleanField(default=False))
User.add_to_class('profile_pic',  models.CharField(max_length=400, default="/BeingMomin/media/images/profiles/default_profile.jpg"))



class locality_mapping(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User)
    locality_key = models.CharField(max_length=400)
    tahsil = models.CharField(max_length=400)
    district = models.CharField(max_length=400)
    state = models.CharField(max_length=400)
    class Meta(object):
        db_table = 'AmbassadorPortal_locality_mapping'

class people(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=300, default="")
    dob = models.DateField()
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=7)
    marital_status = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    education_key = models.CharField(max_length=40)
    education_details = models.TextField()
    locality = models.ForeignKey(locality_mapping , default=1)
    alive_flag = models.BooleanField()
    father_id = models.IntegerField()
    mother_id = models.IntegerField()
    profile_pic = models.ImageField(upload_to='BeingMomin/media/images/profiles/', default='/BeingMomin/media/images/profiles/default_profile.jpg', blank=True )
    life_partner_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    class Meta(object):
        db_table = 'AmbassadorPortal_people'


class news_room(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    locality = models.ForeignKey(locality_mapping, default=1)
    news_date = models.DateField()
    news_title = models.CharField(max_length=400)
    news_description = models.TextField()
    news_category = models.CharField(max_length=400)
    new_attachment = models.ImageField(upload_to='BeingMomin/media/images/news_attachment/', blank=True )
    verified  = models.BooleanField()
    currently_show = models.BooleanField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)










