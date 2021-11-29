from pharmasee.models import Reminder, Pill
from pharmasee.serializers import PillSerializer
from accounts.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import Http404
import json # 직접 request.data 를 parse하기 위해 필요

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication, ))
def get_nugu_request(request, foramt=None):
    if request.method == 'GET':
        print("연결 성공")

        action = request.query_params['action']
        action_name = action.get('actionName')

        if action_name == "ask.not_taken_pills":
            answer_not_taken_pills(request)

def answer_not_taken_pills(request):
    # context = {
    #     "resultCode": "OK",
    #     "output": request.
    # }

    print(request.data)
