# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from view.view_sign_up_ambassador import view_sign_up_ambassador
from view.view_locality_ambassadors import view_locality_ambassadors
from view.view_signin import view_sign_in
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def sign_up_ambassador(request):
    return view_sign_up_ambassador(request)


@csrf_exempt
def sign_in(request):
    return view_sign_in(request)


@csrf_exempt
def locality_ambassadors(request):
    return view_locality_ambassadors(request)



