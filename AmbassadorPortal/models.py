# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

User.add_to_class('mobile_no', models.CharField(max_length=13, blank=False, unique=True))
User.add_to_class('qualification', models.CharField(max_length=400))
User.add_to_class('address', models.TextField(max_length=500, blank=True))
User.add_to_class('mobile_verified', models.BooleanField(default=False))
User.add_to_class('finalized', models.BooleanField(default=False))
User.add_to_class('profile_pic',  models.CharField(max_length=400, default="/media/images/profiles/default_profile_pic.png"))



class people(models.Model):
    name = models.CharField(max_length=300),
    dob = models.CharField(max_length=15)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=7)
    marital_status = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    education_key = models.CharField(max_length=40)
    education_details = models.TextField()
    address_key = models.CharField(max_length=50)
    alive_flag = models.BooleanField()
    father_id = models.IntegerField()
    mother_id = models.IntegerField()
    profile_pic = models.ImageField(upload_to='media/images/profiles/', default='media/images/profiles/default.png', blank=True )
    life_partner_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)




class locality_mapping(models.Model):
    user = models.ForeignKey(User)
    locality_key = models.CharField(max_length=400)
    tahsil = models.CharField(max_length=400)
    district = models.CharField(max_length=400)
    state = models.CharField(max_length=400)
    class Meta(object):
        managed = False
        db_table = 'SocietyApp_locality_mapping'





