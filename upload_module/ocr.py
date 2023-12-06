import sys

from paddleocr import PaddleOCR

import util

def setup_paddleocr():
    ocr_cyr = PaddleOCR(use_angle_cls=True, lang='cyrillic')
    ocr_en = PaddleOCR(use_angle_cls=True, lang='en')
    yield ocr_cyr, ocr_en

def image2text(ocr_model: PaddleOCR, img_path: str) -> str:
    result = ocr_model.ocr(img_path, cls=False)
    try:
        if result[0]:
            a = " ".join((t[1][0] for t in result[0]))
        else:
            return ''
    except Exception:
        print(result)
        sys.exit(1)
    return a


def main():
    img_path = 'ocr_images/eng1.png'
    ocr_cyr, ocr_en = next(setup_paddleocr())
    
if "__main__" == __name__:
    main()