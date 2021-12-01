from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response

from pharmasee.models import Pill

import os
import pandas
import tensorflow as tf
import tensorflow_hub as hub
import warnings
warnings.filterwarnings('ignore')

# bulk_create()
def populate_pills(csv_url):
    df = pandas.read_csv(csv_url)
    

@api_view(['POST'])
def pill_ai_identify(request):
    if Pill.objects.count() < 10:
        csv_url = os.path.join(settings.STATIC_ROOT, 'csv/sample_btm.csv')
        populate_pills(csv_url)

    model_url  = os.path.join(settings.STATIC_ROOT, 'h5/best_model.h5')
    with tf.device('/cpu:0'):
        model = tf.keras.models.load_model(model_url, custom_objects={'KerasLayer': hub.KerasLayer})
    # print(model.summary())

    return Response({})