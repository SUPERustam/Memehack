import subprocess
from subprocess import Popen, PIPE
import urllib.request
import sys
import psycopg2
import ocr

sys.path.append('.')
from db import func_db as fdb
import util



@util.timeit
def parse_vk_album(link: str, *filename):
    # if filename:
    #     # f = open(filename[0], 'w')
    #     # subprocess.run(f"gallery-dl -g {link}".split(), stdout=f)
    #     # f.close()
    #     f = subprocess.run(args=f"gallery-dl -g {link}".split(),
    #                           universal_newlines=True,
    #                           stdout=subprocess.PIPE)

    #     nmap_lines = f.stdout.splitlines()
    #     print(nmap_lines)
    #     return

    with Popen(f"gallery-dl -g {link}".split(), stdout=PIPE, universal_newlines=True) as process:
        for line in process.stdout:
            l = line.rstrip()




@util.timeit
def to_vk_link(link: str) -> str:
    pass


@util.timeit
def pipeline(link: str):
    # connect to db
    try:
        conn = psycopg2.connect(
            dbname="memehackdb",
            user="artyom",
            host="localhost",
            port=5432
        )
    except psycopg2.Error as error:
        print("I was unable to connect to the database MemeHackDB!\n"
              "Error: {error}")
        sys.exit(1)
    
    # initialization
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    cur = conn.cursor()

    # write links
    length_of_links = []

    with Popen(f"gallery-dl -g {link}".split(), stdout=PIPE, universal_newlines=True) as process:
        stp = 0
        for img in process.stdout:
            stp += 1
            if stp == 3:
                break
            img = img[:-1]  # string end up with '\n'
            
            length_of_links.append(img)

            urllib.request.urlretrieve(img, 'upload_module/pipeline_image.jpg')

            text_ru = util.normalization_text(ocr.image2text(
                ocr_cyr, 'upload_module/pipeline_image.jpg'))
            text_en = util.normalization_text(ocr.image2text(
                ocr_en, 'upload_module/pipeline_image.jpg'))

            fdb.insert_image(cur, vk=img)
            conn.commit()
            fdb.insert_text(cur, img_id= ,text_ru, text_en)
        
        

    conn.commit()
    cur.close()
    conn.close()


if "__main__" == __name__:
    pipeline('https://vk.com/album-206845783_00')
    print('finish')
    # 1. max 35.4 mib, Start time: 2023-10-22 23:32:36.399000
# End time: 2023-10-22 23:33:04.989000
# Total number of allocations: 343764
# Total number of frames seen: 519
    # l = list(parse_vk_album('https://vk.com/album-206845783_00'))
    # print('finish')

    

    # pipeline('upload_module/file.txt')
