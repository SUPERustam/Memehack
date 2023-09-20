from paddleocr import PaddleOCR
import os
import sys
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang='en')
img_path = 'i.jpg'

result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)
