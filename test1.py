import os 
import cv2
import json
import numpy as np
import requests
import easyocr
from PIL import Image, ImageDraw, ImageFont


file_path='/media/dataset1/jinlovespho/ocr_plantynet/data/000000030633-01'
files = os.listdir(file_path)

imgs = sorted([img for img in files if img.endswith('png')])
anns = sorted([ann for ann in files if ann.endswith('json')])

reader = easyocr.Reader(lang_list=['en','ko'],
                        detect_network="craft", 
                        recog_network='standard'
                        )

# font 설치 apt install fonts-nanum -y
font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", size=15)

for img in imgs:

    img_id = img.split('.')[0]
    img_path = f'{file_path}/{img}'

    result = reader.readtext(img_path)

    img_pil = Image.open(img_path)
    draw = ImageDraw.Draw(img_pil)

    for box, text, conf in result:

        if conf > 0.5:
            color = (0,255,0)
        else:
            color = (255,0,0)

        x0 = min(box[0][0], box[2][0])
        y0 = min(box[0][1], box[2][1])
        x1 = max(box[0][0], box[2][0])
        y1 = max(box[0][1], box[2][1])
        draw.rectangle([x0, y0, x1, y1], outline=color, width=1)
        draw.text(box[1], text, font=font, fill=color)

    img_pil.save(f'./vis/easyocr/easyocr_{img_id}.jpg')
    
breakpoint()