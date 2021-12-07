from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from numpy.core.numeric import _correlate_dispatcher
from pharmasee.models import TimestampedModel

import os
import sys
import datetime
import uuid
from PIL import Image
import numpy as np
import requests
import json
import cv2

color_dict={
    'blue_color' : (255, 0, 0),
    'green_color' : (0, 255, 0),
    'red_color' : (0, 0, 255),
    'white_color' : (255, 255, 255)
}

def make_path(type, filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime(f'pill_ai/{type}/%Y/%m/%d')
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s"%(uuid.uuid4().hex, suffix, ext)
    return os.path.join(filepath, filename)

def file_upload_path_input(instance, filename):
    return make_path('input', filename)

def file_upload_path_output(instance, filename):
    return make_path('output', filename)

def file_upload_path_for_db(instance, filename):
    pass

class DnnImage(TimestampedModel):
    input_image = models.ImageField(upload_to=file_upload_path_input)
    output_image = models.ImageField(upload_to=file_upload_path_output, blank=True, null=True)
    correct = models.BooleanField(default=False)
    status_mesg = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.predict_pills()
        super(DnnImage ,self).save(*args, **kwargs)

    def predict_pills(self, *args, **kwargs):
        output_image, correct, status_mesg = predict(self.input_image)

        self.output_image = InMemoryUploadedFile(
            file=output_image,
            field_name='ImageField',
            name=self.input_image.name,
            content_type='image/jpeg',
            size=sys.getsizeof(output_image),
            charset=None
        )

        self.correct = correct
        self.status_mesg = status_mesg

def predict(img):
    img = Image.open(img)
    h, w = img.height, img.width
    img = img.convert('RGB').resize((512, 512))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    
    data = json.dumps({
        "instances": img.tolist()
    })
    headers = {"content/type": "application/json"}

    response = requests.post('http://localhost:8501/v1/models/pills_model:predict', data=data, headers=headers)
    
    predictions = response.json()['predictions'][0]
    opencv_img = cv2.cvtColor(np.squeeze(img), cv2.COLOR_RGB2BGR)
    draw_label_for_single_image(opencv_img, predictions, None, 0.8)
    opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
    
    img = np.array(opencv_img)
    img = Image.fromarray(img)
    img = img.resize((w, h))
    return (img_to_bytes(img), False, "모든 약을 알맞게 챙기셨습니다.") 

def img_to_bytes(img):
    output = BytesIO()
    img.save(output, format='JPEG', quality=100)
    output.seek(0)
    return output

def draw_label_for_single_image(img, output_dict, selection, score_threshold=0.5):
  #인식을 위한 미니멈 Threshold
  MIN_SCORE_THRESHOLD=score_threshold

  #output_dict/detection_boxes : 검출한 박스들, 사진의 비율로 이루어져잇음 ( 0<x<1)
  #output_dict/detection_scores : 검출한 박스의 유사도 점수
  boxes=np.squeeze(output_dict['detection_boxes'])
  scores=np.squeeze(output_dict['detection_scores'])

  bboxes=boxes[scores > MIN_SCORE_THRESHOLD]
  #img 높이와 너비 저장
  img_height, img_width, img_c= img.shape

  box_list=[]
  for box in bboxes:
    y_min, x_min, y_max, x_max= box
    box_list.append([x_min*img_width, x_max*img_width, y_min*img_height, y_max*img_height])

  #Cricle 그리는 방법
  for x in box_list:
    cv2.circle(img,(int((x[0]+x[1])/2),int((x[2]+x[3])/2)), 50, color_dict['green_color'], 12)

  #x 그리는 방법
  for x in box_list:
    cv2.line(img, (int(x[0]),int(x[3])), (int(x[1]),int(x[2])), color_dict['red_color'], 12)
    cv2.line(img, (int(x[0]),int(x[2])), (int(x[1]),int(x[3])), color_dict['red_color'], 12) 

  return img