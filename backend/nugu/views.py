from pharmasee.models import Reminder, Pill
from pharmasee.serializers import PillSerializer
from accounts.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

import pprint
import datetime

@api_view(['POST'])
def answer_taken_pills(request):
    pprint.pprint(request.data)
    try:
        version = request.data.get('version')
        action = request.data.get('action')
        action_name = action.get('actionName')
        params = action.get('parameters')
        output = dict(zip(params.keys(), [val.get('value') for val in params.values()]))
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

    taken_list = ""
    status_mesg = ""
    
    qs_taken = Reminder.objects.filter(is_taken_today=True)
    qs_forgot = Reminder.objects.filter(is_taken_today=False)

    num_taken = len(qs_taken)
    num_forgot = len(qs_forgot)
    total_pills = num_taken + num_forgot

    if total_pills == 0:
        status_mesg = "복용 예정된 약이 없습니다. 등록을 부탁드립니다"

    elif num_taken > 0:
        is_late = False
        for obj in qs_taken:
            pill_obj = get_object_or_404(Pill, id=obj.pill_id.id)
            taken_list +=  str(obj.when_to_take) + '에 ' + pill_obj.name +  " " + str(obj.dose_taken_today) + "정, "
            
            dummy = datetime.date(1, 1, 1)
            when_to_take = datetime.datetime.combine(dummy, obj.when_to_take)
            taken_time = datetime.datetime.combine(dummy, obj.taken_time)
            diff_hours = int((taken_time - when_to_take).total_seconds() / 3600)
            if diff_hours > 2:
                is_late = True
        taken_list += "을 복용하셨습니다."

        if is_late:
            status_mesg = "2시간 이상 지체하여 복용한 약이 있으니, 주의 부탁드립니다."
        
        if num_forgot > 0:
            status_mesg += "복용을 잊은 약이 있으니, 확인부탁드립니다."
        else:
            status_mesg += "예정된 약을 모두 제시간에 복용하였습니다"

    else:
        status_mesg = "복용을 잊은 약이 있으니, 확인부탁드립니다"

    context['output']['taken_list'] = taken_list
    context['output']['status_mesg'] = status_mesg
    
    pprint.pprint(context)
    return Response(context)

@api_view(['POST'])
def answer_not_taken_pills(request):
    pprint(request.data)
