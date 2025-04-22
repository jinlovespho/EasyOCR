import os 
import cv2
import json
import numpy as np
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

# font 설치 apt install fonts-nanum -y
font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", size=15)

for img, ann in zip(imgs, anns):
    img_id = img.split('.')[0]
    ann_id = ann.split('.')[0]
    assert img_id == ann_id, 'img and ann must be the same'

    img_path = f'{file_path}/{img}'
    ann_path = f'{file_path}/{ann}'

    # Load original image to get dimensions
    img_pil = Image.open(img_path)
    img_w, img_h = img_pil.size

    # Create blank white canvas for visualization
    canvas_w = img_w
    canvas_h = img_h
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # Load JSON annotation
    with open(ann_path, 'r') as f:
        ann = json.load(f)

    if 'fullTextAnnotation' in ann['responses'][0].keys():
        pages = ann['responses'][0]['fullTextAnnotation']['pages'][0]
    blocks = pages['blocks']

    # Inside your drawing loop:
    for blk in blocks:
        for paragraph in blk['paragraphs']:
            for word in paragraph['words']:
                text = ''.join([s['text'] for s in word['symbols']])
                box_normalized = word['boundingBox']['normalizedVertices']

                if any(('x' not in v or 'y' not in v) for v in box_normalized):
                    continue

                box = [(int(v['x'] * img_w), int(v['y'] * img_h)) for v in box_normalized]

                x0 = min(box[0][0], box[2][0])
                y0 = min(box[0][1], box[2][1])
                x1 = max(box[0][0], box[2][0])
                y1 = max(box[0][1], box[2][1])
                box_w = x1 - x0
                box_h = y1 - y0

                # Get font that fits inside the box
                fitting_font = get_fitting_font(text, box_w, box_h)

                draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0), width=1)
                draw.text((x0 + 1, y0 + 1), text, font=fitting_font, fill=(0, 0, 0))

    # Combine original image and the canvas side-by-side
    combined = Image.new("RGB", (img_w * 2, img_h), (255, 255, 255))
    combined.paste(img_pil, (0, 0))
    combined.paste(canvas, (img_w, 0))

    combined.save(f'./vis/googleocr/googleocr_{img_id}.jpg')
    


# import os 
# import cv2
# import json
# import numpy as np
# import requests
# import easyocr
# from PIL import Image, ImageDraw, ImageFont


# file_path='/media/dataset1/jinlovespho/ocr_plantynet/data/000000030633-01'
# files = os.listdir(file_path)

# imgs = sorted([img for img in files if img.endswith('png')])
# anns = sorted([ann for ann in files if ann.endswith('json')])

# # font 설치 apt install fonts-nanum -y
# font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", size=15)

# for img, ann in zip(imgs, anns):
#     img_id = img.split('.')[0]
#     ann_id = ann.split('.')[0]
#     assert img_id == ann_id, 'img and ann must be the same'

#     img_path = f'{file_path}/{img}'
#     ann_path = f'{file_path}/{ann}'

#     # load img 
#     # img = cv2.imread(img_path)      # h w 3
#     img_pil = Image.open(img_path)
#     draw = ImageDraw.Draw(img_pil)
    
#     img_w, img_h = img_pil.size

#     # load json ann
#     with open(ann_path, 'r') as f:
#         ann = json.load(f)

#     pages = ann['responses'][0]['fullTextAnnotation']['pages'][0]

#     property = pages['property']
#     width = pages['width']
#     height = pages['height']
#     blocks = pages['blocks']
#     conf = pages['confidence']

#     text = ann['responses'][0]['fullTextAnnotation']['text'].split('\n')


#     for blk in blocks:
#         for paragraph in blk['paragraphs']:
#             for word in paragraph['words']:
#                 text = ''.join([s['text'] for s in word['symbols']])
#                 box_normalized = word['boundingBox']['normalizedVertices']

#                 # Skip if any vertex doesn't have both 'x' and 'y'
#                 if any(('x' not in v or 'y' not in v) for v in box_normalized):
#                     continue

#                 box = [(int(v['x'] * img_w), int(v['y'] * img_h)) for v in box_normalized]

#                 x0 = min(box[0][0], box[2][0])
#                 y0 = min(box[0][1], box[2][1])
#                 x1 = max(box[0][0], box[2][0])
#                 y1 = max(box[0][1], box[2][1])
#                 draw.rectangle([x0, y0, x1, y1], outline=(0,255,0), width=1)
#                 draw.text(box[1], text, font=font, fill=(0,255,0))

#     img_pil.save(f'./vis/googleocr/googleocr_{img_id}.jpg')
    
# breakpoint()