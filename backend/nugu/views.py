from pharmasee.models import Reminder, Pill
from pharmasee.serializers import PillSerializer
from accounts.models import User

from rest_framework import status
from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
# from rest_framework import exceptions
# from rest_framework.exceptions import APIException
# from django.http import Http404

@api_view(['POST'])
def answer_taken_pills(request):
    try:
        version = request.data.get('version')
        action = request.data.get('action')
        action_name = action.get('actionName')
        params = action.get('parameters')
        # output = dict(zip(params.keys(), [val.get('value') for val in params.values()]))
        output = dict(zip(params.keys(), ["killme" for val in params.values()]))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if action_name != "answer.taken_pills":
        return Response(status=status.HTTP_400_BAD_REQUEST)

    context = {
        "version": version,
        "resultCode": "OK",
        "output": output,
        "directives":[]
    }
    return Response(context)
