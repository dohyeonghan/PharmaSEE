from rest_framework import response
from pharmasee.models import Reminder, Pill
from pharmasee.serializers import PillSerializer
from accounts.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

import pprint
import datetime

version = ""
action = {}
action_name = ""
params = {}
output = {}

def parse_play_request(body):
    global version, action, action_name, params, output
    try:
        version = body.get('version')
        action = body.get('action')
        action_name = action.get('actionName')
        params = action.get('parameters')
        output = dict(zip(params.keys(), [val.get('value') for val in params.values()]))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def answer_taken_pills(request):
    pprint.pprint(request.data)

    parse_play_request(request.data)

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

    # if len(Reminder.objects.filter(User=~~~)) == 0:
    if len(Reminder.objects.all()) == 0:
        status_mesg = "복용 리스트에 등록된 약이 없습니다."
        context['output']['taken_list'] = taken_list
        context['output']['status_mesg'] = status_mesg
        return Response(context)
    
    qs_taken = Reminder.objects.filter(is_taken_today=True).order_by('taken_time')
    qs_overdue = Reminder.objects.filter(is_taken_today=False).filter(when_to_take__lte=datetime.datetime.now().time())

    num_taken = len(qs_taken)
    num_forgot = len(qs_overdue)
    total_pills = num_taken + num_forgot

    if total_pills == 0:
        status_mesg = "오늘 복용한 약이 없습니다."

    elif num_taken > 0:
        is_late = False
        for obj in qs_taken:
            pill_obj = get_object_or_404(Pill, id=obj.pill_id.id)
            taken_list +=  str(obj.taken_time) + '에 ' + pill_obj.name +  " " + str(obj.dose_taken_today) + "정, "
            
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
    pprint.pprint(request.data)

    parse_play_request(request.data)

    if action_name != "answer.not_taken_pills":
        return Response(status=status.HTTP_400_BAD_REQUEST)

    context = {
        "version": version,
        "resultCode": "OK",
        "output": output,
        "directives":[]
    }

    # 오전 2시에 약 A 2정을 아직 복용하지 않았습니다. 피보호자에게 전화를 거시겠습니까?(overdue)
    # 오후 9시에 약B 3정을 복용해야합니다. (scheduled)
    # 오늘 계획된 모든 약을 먹었습니다. (alll_taken)

    response_mesg = ""
    ask_to_call = 0

    # if len(Reminder.objects.filter(User=~~~)) == 0:
    if len(Reminder.objects.all()) == 0:
        response_mesg = "복용 리스트에 등록된 약이 없습니다."
        context['output']['response_mesg'] = response_mesg
        context['output']['ask_to_call'] = str(ask_to_call)
        return Response(context)
    
    qs_overdue = Reminder.objects.filter(when_to_take__lte=datetime.datetime.now().time()).filter(is_taken_today=False).order_by('when_to_take')
    qs_scheduled = Reminder.objects.filter(when_to_take__gt=datetime.datetime.now().time()).filter(is_taken_today=False).order_by('when_to_take')

    overdue_list = []
    if len(qs_overdue) > 0:
        # if user 가 보호자임
        ask_to_call = 1
        
        for obj in qs_overdue:
            pill_obj = get_object_or_404(Pill, id=obj.pill_id.id)
            pillname_dose_str = pill_obj.name + " " + str(obj.dose) + "정, "
            response_mesg += str(obj.when_to_take) + "에 " + pillname_dose_str
            overdue_list.append(pillname_dose_str)
        
        response_mesg += "을 아직 복용하지 않았습니다."

    if len(qs_scheduled) > 0:
        for obj in qs_scheduled:
            pill_obj = get_object_or_404(Pill, id=obj.pill_id.id)
            response_mesg += str(obj.when_to_take) + "에 " + pill_obj.name + " " + str(obj.dose) + "정, "
        response_mesg += "을 복용할 예정입니다."

    if ask_to_call:
        response_mesg += "피보호자에게 문자를 보내 " + ''.join(overdue_list) + "복용을 상기하시겠습니까?"

    if len(qs_overdue) == 0 and len(qs_scheduled) == 0:
        response_mesg = "오늘 계획된 모든 약을 복용하셨습니다."
    
    context['output']['response_mesg'] = response_mesg
    context['output']['ask_to_call'] = str(ask_to_call)
    
    pprint.pprint(context)
    return Response(context)

@api_view(['POST'])
def answer_total_status(request):
    pass

@api_view(['GET'])
def health(request):
    return Response("OK")