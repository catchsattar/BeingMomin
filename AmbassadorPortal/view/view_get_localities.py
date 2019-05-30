import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse

from AmbassadorPortal.models import locality_mapping
from BeingMomin import config

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes((AllowAny,))
def view_get_localities(request):
    response = {}
    body = None

    try:
        response["status"] = 0
        # locality_list = locality_mapping.objects.all().values_list('locality_key', flat=True)
        locality_list = locality_mapping.objects.values('id','locality_key')

        localities = []
        locality_list = list(locality_list)

        for locality in locality_list:
            locality_dict = {
                "localityId" : locality["id"],
                "localityName": locality["locality_key"]
            }
            localities.append(locality_dict)

        response["localities"]= localities

        print(response)

    except Exception as e:
     response = {"status": 1}
     logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)


    return HttpResponse(json.dumps(response), content_type='application/json')
