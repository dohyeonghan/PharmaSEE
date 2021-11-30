from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response

import os
import pandas

# bulk_create()
def populate_pills(csv_url):
    df = pandas.read_csv(csv_url)
    print(df.head())
    

@api_view(['POST'])
def pill_ai_identify(request):
    csv_url = os.path.join(settings.STATIC_ROOT, 'csv/sample_btm.csv')
    populate_pills(csv_url)
    return Response({})