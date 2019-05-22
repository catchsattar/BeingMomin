import logging
import json
import ast

from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse

from AmbassadorPortal.models import people
from AmbassadorPortal.view.portal_utils import get_locality_from_name

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_add_person(request):
    response = {"Status": 0}
    body = None

    try:
        # body_unicode = request.body.decode('utf-8')
        # body = ast.literal_eval(body_unicode)

        body= request.POST
        full_name = body.get('fullName')
        dob = body.get('dob')
        email = body.get('email')
        mobile_number = body.get('mobileNumber')
        gender = body.get('gender')
        marital_status = body.get('maritalStatus')
        life_partner_id = body.get('lifePartnerId')
        education_key = body.get('educationLevel')
        education_details = body.get('educationDetails')
        locality_key = body.get('localityKey')
        home_address = body.get('homeAddress')
        father_id = body.get('fatherId')
        mother_id = body.get('motherId')
        alive_flag= body.get('aliveFlag')
        profession= body.get('profession')
        profile_name = body.get('profileName')

        file= request.FILES['profileFile']
        if(file.size > 10):
           fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
           filename = fs.save(profile_name, file)
           profile_url = fs.url(filename)
        else:
            profile_url="/BeingMomin/media/images/profiles/default_profile.jpg"



        people_obj = people(name=full_name, mobile= mobile_number,dob=dob, email=email, gender=gender,marital_status=marital_status,
                            life_partner_id=life_partner_id,education_key=education_key, education_details=education_details,profile_pic = profile_url,
                            locality=get_locality_from_name(locality_key),father_id=father_id,mother_id=mother_id,alive_flag=alive_flag, profession=profession)

        people_obj.save()


    except Exception as e:
        response = {"Status": 1}
        logger.error("Body of Request is'{0}' and Exception is '{1}'".format(body, e), exc_info=True)

    return HttpResponse(json.dumps(response), content_type='application/json')
