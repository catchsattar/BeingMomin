import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connections

from AmbassadorPortal.models import locality_mapping, people
from BeingMomin import config

logger = logging.getLogger('django')

# cursor.execute(
#     "SELECT id, name FROM AmbassadorPortal_people where locality_id = %s and father_id = 0 and id IN ( SELECT father_id from AmbassadorPortal_people )",
#     [locality_id])


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_get_families(request):

    response = {}
    body = None
    try:
        body_unicode = request.body.decode('utf-8')
        body = ast.literal_eval(body_unicode)
        locality_id = body['localityId']

        response["status"] = 0
        ancestors = []
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT id, name FROM AmbassadorPortal_people where gender='Male' and locality_id = %s and father_id = 0 and id IN ( SELECT father_id from AmbassadorPortal_people ) "
                           " UNION SELECT id, name FROM AmbassadorPortal_people as people_a where gender='Male' and locality_id = %s and (SELECT locality_id from AmbassadorPortal_people as people_b where people_b.id = people_a.father_id ) != %s and id IN ( SELECT father_id from AmbassadorPortal_people )",[locality_id, locality_id, locality_id])

            for row in cursor.fetchall():
                ancestorDict= {
                    "ancestorId": row[0],
                    "ancestorName" : row[1]
                }
                ancestors.append(ancestorDict)

        response["localities"]=  ancestors

        print(response)

    except Exception as e:
     response = {"status": 1}
     logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)


    return HttpResponse(json.dumps(response), content_type='application/json')
