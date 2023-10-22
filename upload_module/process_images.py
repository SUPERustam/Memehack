import subprocess
import urllib.request
import sys

import ocr
sys.path.append('.')
import util
from db import func_db as fdb


# https://vk.com/album-206845783_00


@util.timeit
def parse_vk_album(link: str, *filename: (str | None)) -> None:
    if filename:
        f = open(filename, 'w')
        subprocess.run(f"gallery-dl -g {link}".split(), stdout=f)
        f.close()
        return
        

@util.timeit
def to_vk_link(link: str) -> str:
    pass


@util.timeit
def pipeline(filename: str):
    with open(filename, 'r') as f:
        imgs = f.readlines()
    
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    for img in imgs[:2]:  # todo: remove slice
        img = img[:-1] # string end up with '\n'
        urllib.request.urlretrieve(img, 'upload_module/pipeline_image.jpg')

        text_cyr = util.normalization_text(ocr.image2text(ocr_cyr, 'upload_module/pipeline_image.jpg'))
        text_en = util.normalization_text(ocr.image2text(ocr_en, 'upload_module/pipeline_image.jpg'))


if "__main__" == __name__:
    pipeline('upload_module/file.txt')