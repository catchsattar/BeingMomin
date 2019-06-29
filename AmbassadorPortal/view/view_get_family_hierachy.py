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
def view_get_family_hierachy(request):

    response = {}
    body = None
    try:
        body_unicode = request.body.decode('utf-8')
        body = ast.literal_eval(body_unicode)
        person_id = body['personId']
        response["status"] = 0

        response["data"]= get_person_info(0, person_id)

    except Exception as e:
     response = {"status": 1}
     logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)


    return HttpResponse(json.dumps(response), content_type='application/json')


def get_person_info(father_id, person_id):
    person_info = {}
    person = get_person_from_id(person_id)
    person_info["personId"] = person.id
    person_info["fatherId"] = father_id
    person_info["name"]= person.name
    person_info["gender"] = person.gender
    if person.gender == "Male" :
      if person.life_partner_id is not  None and person.life_partner_id != 0 :
         person_info["wifeName"]=get_person_name_from_id(person.life_partner_id)
         person_info["wifeId"] = person.life_partner_id

      person_info["children"]= get_children(person.id)

    return person_info


def get_children(person_id):
    children=[]
    children_array = people.objects.filter(father_id=person_id).values('id')
    list_of_children = list(children_array)
    for child in list_of_children :
        children.append(get_person_info(person_id,child["id"]))

    return children













