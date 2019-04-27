"""
This view is used for login the user and generate the json file for
that user which user is belong in survey app.
"""
import ast
import json
import logging
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from AmbassadorPortal.models import people
from portal_utils import get_person_from_id

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_search_person(request):
    """
    This view is used for login and generates json for user access.
    :param request: contain username and password of user.
    :return: json for generate UI dynamically.
    """
    response = {}
    body = None
    try:
        body_unicode = request.body.decode('utf-8')
        body = ast.literal_eval(body_unicode)
        search_name = body['searchName']
        locality = body['locality']
        gender = body['gender']

        response["Status"] = 0

        persons_array = people.objects.filter(name__icontains=search_name, gender=gender,
                                              locality_id__locality_key= locality).values('id','name','locality__locality_key','father_id')

        persons = []
        persons_list = list(persons_array)

        for person in persons_list:
            personDict = {
                "id":person["id"],
                "name": person["name"],
                "locality" : person["locality__locality_key"],
                "father":  get_person_from_id(person["father_id"]).name
            }
            persons.append(personDict)

        response["persons"]=persons

    except Exception as e:
        response = {"Status": 1}
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')
