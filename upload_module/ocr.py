from paddleocr import PaddleOCR


def setup_paddleocr():
    ocr_cyr = PaddleOCR(use_angle_cls=True, lang='cyrillic')
    ocr_en = PaddleOCR(use_angle_cls=True, lang='en')
    yield ocr_cyr, ocr_en


def image2text(ocr_model: PaddleOCR, img_path: str) -> list:
    result = ocr_model.ocr(img_path, cls=False)
    return result[0]


def main():
    img_path = 'ocr_images/eng1.png'
    ocr_cyr, ocr_en = next(setup_paddleocr())

    result = image2text(ocr_cyr, img_path) 
    result2 = image2text(ocr_en, img_path)

    with open('upload_module/ans.txt', 'w') as t, open('upload_module/ans2.txt', 'w') as t1:
        t.write(str(result))
        t1.write(str(result2))


if "__main__" == __name__:
    main()
