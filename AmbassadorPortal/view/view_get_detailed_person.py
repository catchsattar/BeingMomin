import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connections
from portal_utils import *

from AmbassadorPortal.models import locality_mapping, people
from BeingMomin import config

logger = logging.getLogger('django')


# cursor.execute(
#     "SELECT id, name FROM AmbassadorPortal_people where locality_id = %s and father_id = 0 and id IN ( SELECT father_id from AmbassadorPortal_people )",
#     [locality_id])


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_get_detailed_person(request):
    response = {}
    body = None
    try:
        body_unicode = request.body.decode('utf-8')
        body = ast.literal_eval(body_unicode)
        person_id = body['personId']
        response["status"] = 0
        response["message"] = ""

        response["data"] = get_person_info(person_id)

    except Exception as e:
        response = {"status": 1}
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')


def get_person_info(person_id):
    person_info = {}
    person = get_person_from_id(person_id)
    # person_info["personId"] = person.id
    # person_info["fatherId"] = father_id
    person_info["name"] = person.name
    profile_url= str(person.profile_pic)
    if len(profile_url) > 0 :
       person_info["profilePicUrl"] = config.BASE_URL + profile_url
    person_info["gender"] = person.gender
    person_info["maritalStatus"] = person.marital_status
    person_info["profession"] = person.profession
    person_info["isAlive"] = person.alive_flag
    person_info["educationKey"] = person.education_key
    person_info["educationDeatils"] = person.education_details

    extra_details = []
    if person.email is not None and person.email.__len__() > 0:
        emailDetail = {}
        emailDetail["order"] = 1
        emailDetail["info"] = "Email at " + person.email
        extra_details.append(emailDetail)

    if person.mobile is not None and person.mobile.__len__() > 0:
        mobileDetail = {}
        mobileDetail["order"] = 2
        mobileDetail["info"] = "Contact on " + person.mobile
        extra_details.append(mobileDetail)

    if person.dob is not None :
        dobDetail = {}
        dobDetail["order"] = 3
        dobDetail["info"] = "Born on " + person.dob.strftime("%d %b, %Y")
        extra_details.append(dobDetail)

    if person.locality_id is not None:
        localityDetail = {}
        localityDetail["order"] = 4
        localityDetail["info"] = "Lives in " + person.locality.locality_key
        extra_details.append(localityDetail)

    person_info["extraDetails"] = extra_details

    relations = []

    close_ones_obj = {}
    close_ones_obj["order"] = 1
    close_ones_obj["group"] = "Close Ones"
    close_ones = []
    father_detail = {}
    father_detail["order"] = 1
    father_detail["relation"] = "Father"
    if person.father_id is not None and person.father_id != 0:
        father_detail["id"] = person.father_id
        father_detail["name"] = get_person_name_from_id(person.father_id)
    else:
        father_detail["id"] = 0
        father_detail["name"] = "Not recorded"

    close_ones.append(father_detail)

    mother_detail = {}
    mother_detail["order"] = 2
    mother_detail["relation"] = "Mother"
    if person.mother_id is not None and person.mother_id != 0:
        mother_detail["id"] = person.mother_id
        mother_detail["name"] = get_person_name_from_id(person.mother_id)
    else:
        mother_detail["id"] = 0
        mother_detail["name"] = "Not recorded"
    close_ones.append(mother_detail)

    if person.marital_status != "Single" :
        partner_detail = {}
        partner_detail["order"] = 3
        if person.life_partner_id is not None and person.life_partner_id != 0:
            partner_detail["id"] = person.life_partner_id
            partner_detail["name"] = get_person_name_from_id(person.life_partner_id)
            if person.gender == "Male":
                partner_detail["relation"] = "Wife"
            else:
                partner_detail["relation"] = "Husband"
        else:
            partner_detail["id"] = 0
            partner_detail["name"] = "Not recorded"
            partner_detail["relation"] = "life partner"

        close_ones.append(partner_detail)

    close_ones_obj["members"] = close_ones

    relations.append(close_ones_obj)

    if person.father_id!=0 :
        sibling_obj, siblings_count = get_siblings(person.id, person.father_id)
        if siblings_count > 0 :
            relations.append(sibling_obj)

    children_obj, children_count = get_children(person_id)
    if children_count > 0 :
        relations.append(children_obj)

    person_info["family"]= relations

    return person_info


def get_children(person_id):
    children_detail_obj = {}
    children_detail_obj["order"] = "3"
    children_detail_obj["group"] = "Children/Heirs"

    children = []
    children_array = people.objects.filter(father_id=person_id).values('id', 'name', 'gender')
    list_of_children = list(children_array)
    for index, child in enumerate(list_of_children):
        if child["gender"] == "Male":
            child["relation"] = "Son"
        else:
            child["relation"] = "Daughter"
        del child["gender"]
        child["order"] = index
        children.append(child)
    children_detail_obj["members"] = children

    return children_detail_obj, len(children)


def get_siblings(person_id, father_id):
    sibling_detail_obj={}
    sibling_detail_obj["order"]=2
    sibling_detail_obj["group"]="Siblings"

    siblings=[]
    siblings_array = people.objects.filter(father_id = father_id).values('id', 'name', 'gender')
    list_of_siblings= list(siblings_array)

    for index,sibling in enumerate(list_of_siblings) :
        if sibling["id"] != person_id :
            if sibling["gender"] == "Male":
                sibling["relation"] = "Brother"
            else:
                sibling["relation"] = "Sister"
            del sibling["gender"]
            sibling["order"]= index
            siblings.append(sibling)

    sibling_detail_obj["members"]= siblings
    return sibling_detail_obj, len(siblings)
