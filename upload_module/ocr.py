import sys

from paddleocr import PaddleOCR

sys.path.append('.')
import util

def setup_paddleocr():
    ocr_cyr = PaddleOCR(use_angle_cls=True, lang='cyrillic')
    ocr_en = PaddleOCR(use_angle_cls=True, lang='en')
    yield ocr_cyr, ocr_en

def image2text(ocr_model: PaddleOCR, img_path: str) -> list:
    result = ocr_model.ocr(img_path, cls=False)
    return " ".join((t[1][0] for t in result[0]))

def main():
    img_path = 'ocr_images/eng1.png'
    ocr_cyr, ocr_en = next(setup_paddleocr())
    print(util.normalization_text('sdfdsfsf.dff.'))

if "__main__" == __name__:
    main()