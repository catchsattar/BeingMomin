import logging
import json
import ast

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connections
from portal_utils import *

from AmbassadorPortal.models import locality_mapping, people, news_room
from BeingMomin import config

logger = logging.getLogger('django')





@api_view(['POST'])
@permission_classes((AllowAny,))
def view_get_current_news(request):
    response = {}
    body = None
    try:

        current_news = news_room.objects.filter(verified=True, currently_show=True)
        response["status"]=0
        response["data"]= list(current_news)

    except Exception as e:
        response = {"status": 1}
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')

