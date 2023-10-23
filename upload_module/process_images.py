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
    conn = psycopg2.connect(
            dbname="memehackdb",
            user="postgres",
            host="localhost",
            port=5432
        )
    # try:
    #     conn = psycopg2.connect(
    #         dbname="memehackdb",
    #         user="root",
    #         host="localhost",
    #         port=5432
    #     )
    # except psycopg2.Error as error:
    #     print("I was unable to connect to the database MemeHackDB!\n"
    #           "Error: {error}")
    #     sys.exit(1)
    
    # initialization
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    cur = conn.cursor()

    # write links
    length_of_links = []

    with Popen(f"gallery-dl -g {link}".split(), stdout=PIPE, universal_newlines=True) as process:
        stp = 0
        for img in process.stdout:
            if stp == 3:
                break
            stp += 1

            img = img[:-1]  # string end up with '\n'
            
            length_of_links.append(img)

            urllib.request.urlretrieve(img, 'upload_module/pipeline_image.jpg')

            text_ru = util.normalization_text(ocr.image2text(
               ocr_cyr, 'upload_module/pipeline_image.jpg'))
            text_en = util.normalization_text(ocr.image2text(
               ocr_en, 'upload_module/pipeline_image.jpg'))


            fdb.insert_image(cur, vk=img)
            img_id = cur.fetchone()
            fdb.insert_text(cur, img_id, text_ru, text_en)
    
    print(f"{length_of_links=}")    
    conn.commit()
    cur.close()
    conn.close()


if "__main__" == __name__:
    pipeline('https://vk.com/album-206845783_00')