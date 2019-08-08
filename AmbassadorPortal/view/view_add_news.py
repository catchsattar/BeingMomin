import logging
import json
import ast

from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse

from AmbassadorPortal.models import people, news_room
from AmbassadorPortal.view.portal_utils import get_locality_from_name

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_add_news(request):
    response = {"Status": 0}
    body = None

    try:
        body = request.POST
        newsTitle = body.get('newsTitle')
        newsDescription = body.get('newsDescription')
        newsDate = body.get('newsDate')
        newsCategory = body.get('newsCategory')
        taggedPerson = body.get('taggedPersons')
        userId = body.get('userId')
        localityId = body.get('localityId')

        print("tagged id :"+taggedPerson)

        file = request.FILES.get('newsAttachment')
        if (file != None and file.size > 10):
            fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
            filename = fs.save(file.name, file)
            profile_url = fs.url(filename)
        else:
            profile_url = "/BeingMomin/media/images/profiles/default_attachment.jpg"

        news_obj = news_room(locality_id=localityId, news_date=newsDate, news_title=newsTitle,
                             news_description=newsDescription,
                             news_category=newsCategory, tagged_persons=taggedPerson, new_attachment=profile_url,
                             user_id=userId, verified=False, currently_show=False)

        news_obj.save()


    except Exception as e:
        response = {"Status": 1}
        response["message"] = "Something wrong with server"
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')
