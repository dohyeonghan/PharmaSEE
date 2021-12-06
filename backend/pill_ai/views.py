from io import StringIO
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from django.core.files import File

from pharmasee.models import Pill
from .forms import UploadFileForm

import os
import pandas as pd
import urllib.request
import threading
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

demo_vitamins = [
    {
        "name": "라이온연질캡슐",
        "effect": "1. 다음 증상의 완화 : 눈의 건조감\n2. 치골의 발육불량\n3. 야맹증\n4. 구루병 예방\n5. 다음 경우의 비타민 A,D의 보급 : 임신 수유기, 병중ㆍ병후 체력저하 때, 발육기, 노년기.",
        "side_effect": "피부(가려움), 소화기(오심, 구토)"
    },
    {
        "name": "슬림비플러스정",
        "effect": "다음 경우의 비타민 D, E, B1, B2의 보급\n- 육체피로\n- 임신 및 수유기\n- 병중 및 병후(병을 앓는 동안이나 회복 후)의 체력저하시\n- 발육기\n- 노년기",
        "side_effect": "에스트로겐을 포함한 경구용 피임제를 복용하는 여성 또는 혈전성 소인이 있는 환자가 비타민 E를 복용할 경우 혈전증의 위험이 증가될 수 있다."
    },
    {
        "name": "쎄쎄250츄정",
        "effect": "다음 경우의 비타민 C, B2, B6, E의 보급\n- 육체피로\n- 임신 및 수유기\n- 병중 및 병후(병을 앓는 동안이나 회복 후)의 체력저하시\n- 잇몸출혈 및 비출혈(코피) 예방\n- 노년기",
        "side_effect": "위부불쾌감, 설사, 변비, 발진, 발적, 구역, 구토, 식욕부진, 복부팽만감"
    },
    {
        "name": "셀카로틴에프연질캡슐",
        "effect": "1. 다음 증상의 완화 : 눈의 건조감\n2. 치골의 발육불량\n3. 야맹증\n4. 구루병 예방\n5. 다음 경우의 비타민 A,D의 보급 : 임신 수유기, 병중ㆍ병후 체력저하 때, 발육기, 노년기.",
        "side_effect": "피부(가려움), 소화기(오심, 구토)"
    },
    {
        "name": "폴비정",
        "effect": "1. 다음 증상의 완화 : 눈의 건조감\n2. 치골의 발육불량\n3. 야맹증\n4. 구루병 예방\n5. 다음 경우의 비타민 A,D의 보급 : 임신 수유기, 병중ㆍ병후 체력저하 때, 발육기, 노년기.",
        "side_effect": "피부(가려움), 소화기(오심, 구토)"
    },
]

demo_pills_images = [
    "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147427858033600191",
    "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/1NSQUaVEnkh",
    "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147427577106000177",
    "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147426564858700089",
    "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/151853642687600047"
]


def populate_pills(csv_url):
    print("Started creating pills")
    df = pd.read_csv(csv_url)
    df = df.dropna(axis=0)

    keys = ["name", "side_effect", "effect"]
    for idx, row in df.iterrows(): 
        result = urllib.request.urlretrieve(row.itemImage)
        byte_file = File(open(result[0], 'rb'))
        vals = [row.itemName, row.seQesitm.replace('<p>', '').replace('</p>', ''), row.efcyQesitm.replace('<p>', '').replace('</p>', '')]
        data_dict = dict(zip(keys, vals))
        obj = Pill(**data_dict)
        obj.image_dir.save(os.path.basename(row.itemImage), byte_file)
        obj.save()

    for idx, data_dict in enumerate(demo_vitamins):
        result = urllib.request.urlretrieve(demo_pills_images[idx])
        byte_file = File(open(result[0], 'rb'))

        obj = Pill(**data_dict)
        obj.image_dir.save(os.path.basename(demo_pills_images[idx]), byte_file)
        obj.save()
    
    print("Pill Create Complete!")
    

def handle_uploaded_file(file):
    pass

@api_view(['POST'])
def pill_ai_identify(request):
    if request.method == 'POST':
        if Pill.objects.count() < 10:
            csv_url = os.path.join(settings.STATIC_ROOT, 'csv/pills.csv')
            t = threading.Thread(target=populate_pills, args=[csv_url])
            t.setDaemon(False)
            t.start()
            return Response({})


        
        # print(request.data.dict().keys())
        file_string = request.data.get('file')
        file_obj = StringIO()
        image = Image.new()
        image.save(file_obj, "png")
        # print(request.POST)
        # print(request.FILES)
        # print(request.FILES['images'])
        # f = request.data.get('file')
        # with open('image.png', 'wb+') as dest:
        #     dest.write(f)
        # image = Image.open(request.data.get('file'))
        # image.save("uploaded_file.png")

        
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     context = handle_uploaded_file(request.FILES['file'])
        #     return Response(context)

    return Response({})
