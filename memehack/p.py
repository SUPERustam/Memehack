#!/home/codespace/.python/current/bin/python
from paddleocr import PaddleOCR


def setup_paddleocr():
    ocr_cyr = PaddleOCR(use_angle_cls=True, lang='cyrillic')
    ocr_en = PaddleOCR(use_angle_cls=True, lang='en')
    yield ocr_cyr, ocr_en


def image2text(img_path: str, ocr_model: PaddleOCR) -> list:
    result = ocr_model.ocr(img_path, cls=False)
    return result[0]


def main():
    img_path = 'images/rus3_hard.jpg'
    ocr_cyr, ocr_en = next(setup_paddleocr())

    result = image2text(img_path, ocr_cyr)

    with open('ans.txt', 'w') as t:
        t.write(str(result))


if "__main__" == __name__:
    main()
