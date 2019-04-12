"""
This view is used for login the user and generate the json file for
that user which user is belong in survey app.
"""
import ast
import json

import logging
import traceback

from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from AmbassadorPortal.models import locality_mapping

logger = logging.getLogger('django')

@api_view(['POST'])
@permission_classes((AllowAny,))
def view_sign_in(request):
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
        username = body['Username']
        password = body['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.finalized:
                user_obj = User.objects.filter(username=user)

                locality_obj = locality_mapping.objects.get(user_id=user_obj)
                key = locality_obj.locality_key

                response["Status"] = 0
                response['Username'] = username
                response['Locality'] = key

                user = User.objects.get(username=username)
                # Generating token for access another view.
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response["Token"] = token

            else:
                response = {"Status": 3}
        else:
            # Not login access.
            response = {"Status": 2}
    except Exception as e:
        response = {"Status": 1}
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')

