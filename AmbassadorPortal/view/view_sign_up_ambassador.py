import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse


logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_sign_up_ambassador(request):
    response = {}
    body = None

    try:
        body_unicode = request.body.decode('utf-8')
        body = ast.literal_eval(body_unicode)

        mobile_number = body['mobileNumber']
        email=body['email']
        full_name = body['fullName']
        qualification = body['qualification']
        address = body['address']

        user = User.objects.create_user(username= mobile_number, password="samdroid",
                                        mobile_no=mobile_number , email=email,
                                        first_name=full_name.split()[0],last_name=full_name.split()[1],
                                        qualification=qualification,address=address)
        user.save()
        response["Status"] = 0

    except Exception as e:
     response = {"Status": 1}
     logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)


    return HttpResponse(json.dumps(response), content_type='application/json')
