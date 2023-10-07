from PIL import Image
import pytesseract as tsr
import sys
import os

# print(tsr.get_languages())

print('eng1.png')
print(tsr.image_to_string('images/eng1.png', 'rus2+eng2+snum'))
print('rus1.png')
print(tsr.image_to_string('images/rus1.png', 'rus2+eng2+snum'))

# images = os.listdir('images/')
# for im in images:
#     if im == '.DS_Store':
#         continue
#     text = tsr.image_to_string('images/' + im, 'rus2+eng2+snum')
#     with open(f"answers/{im[:im.rfind('.')]}_advance.txt", mode='w') as write_file:
#         write_file.write(text)

#     text = tsr.image_to_string('images/' + im, 'rus1+eng1+snum')
#     with open(f"answers/{im[:im.rfind('.')]}.txt", 'w') as write_file:
#         write_file.write(text)
