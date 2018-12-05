import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse

from AmbassadorPortal.models import locality_mapping

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes((AllowAny,))
def view_locality_ambassadors(request):
    response = {}
    body = None

    try:
        response["Status"] = 0
        locality_list = locality_mapping.objects.values('locality_key', 'tahsil', 'district', 'state',
                                                        'user__first_name', 'user__last_name', 'user__mobile_no',
                                                        'user__email', 'user__address', 'user__profile_pic')

        ambassadors=[]

        ambssadorList=list(locality_list)
        for amb in ambssadorList :
            ambDict= {
                "localityKey":amb["locality_key"],
                "name": amb["user__first_name"]+amb["user__last_name"],
                "mobileNo": amb["user__mobile_no"],
                "email": amb["user__email"],
                "address": amb["user__address"],
                "profilePic": amb["user__profile_pic"],
                "tahsil": amb["tahsil"],
                "district": amb["district"],
                "state": amb["state"]
            }
            ambassadors.append(ambDict)

        response["ambassadors"]= ambassadors

    except Exception as e:
     response = {"Status": 1}
     logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)


    return HttpResponse(json.dumps(response), content_type='application/json')
