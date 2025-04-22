import os 
import cv2
import json
import numpy as np
import requests
import easyocr
from PIL import Image, ImageDraw, ImageFont

def get_fitting_font(text, box_width, box_height, font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf"):
    max_font_size = min(int(box_height), 20)
    for size in range(max_font_size, 4, -1):
        font = ImageFont.truetype(font_path, size)
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        if text_w <= box_width and text_h <= box_height:
            return font
    return ImageFont.truetype(font_path, 5)


file_path = '/media/dataset1/jinlovespho/ocr_plantynet/data/000000030633-01'
files = os.listdir(file_path)

imgs = sorted([img for img in files if img.endswith('png')])
anns = sorted([ann for ann in files if ann.endswith('json')])

reader = easyocr.Reader(lang_list=['en','ko'],
                        detect_network="craft", 
                        recog_network='standard')

for img in imgs:
    img_id = img.split('.')[0]
    img_path = f'{file_path}/{img}'

    result = reader.readtext(img_path)

    # Load original image
    img_pil = Image.open(img_path).convert("RGB")
    img_w, img_h = img_pil.size

    # Create a blank canvas with the same size, placed to the right
    canvas = Image.new("RGB", (img_w * 2, img_h), (255, 255, 255))
    canvas.paste(img_pil, (0, 0))  # original image on the left
    draw = ImageDraw.Draw(canvas)

    for box, text, conf in result:
        if conf > 0.5:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

        x0 = min(box[0][0], box[2][0])
        y0 = min(box[0][1], box[2][1])
        x1 = max(box[0][0], box[2][0])
        y1 = max(box[0][1], box[2][1])
        box_w = x1 - x0
        box_h = y1 - y0

        # Offset by img_w to draw on the blank canvas to the right
        x0_shifted = x0 + img_w
        x1_shifted = x1 + img_w

        draw.rectangle([x0_shifted, y0, x1_shifted, y1], outline=color, width=1)

        fitting_font = get_fitting_font(text, box_w, box_h)
        draw.text((x0_shifted + 1, y0 + 1), text, font=fitting_font, fill=color)

    canvas.save(f'./vis/easyocr/easyocr_side_{img_id}.jpg')
