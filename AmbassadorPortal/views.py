# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from AmbassadorPortal.view.view_get_localities import view_get_localities
from view.view_add_person import view_add_person
from view.view_sign_up_ambassador import view_sign_up_ambassador
from view.view_locality_ambassadors import view_locality_ambassadors
from view.view_search_person import view_search_person
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


@csrf_exempt
def search_person(request):
    return view_search_person(request)

@csrf_exempt
def add_person(request):
    return view_add_person(request)

def get_localities(request):
    return view_get_localities(request)



