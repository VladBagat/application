from PIL import Image, ImageDraw
import pytesseract as ts
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

img = Image.open(r'TextParser\testing\test6.png')

scale = 1             

img = img.resize((img.size[0]*scale, img.size[1]*scale), 3)

#img = img.convert('L')

#img = img.point(lambda x: 0 if x < 170 else 255, '1')               
custom_config = r'--oem 3 -l jpn_vert tessedit_char_whitelist=0123456789'

d = ts.image_to_data(img, lang='jpn_vert', output_type=Output.DICT, config=custom_config)

print(d)

draw = ImageDraw.Draw(img)

for i in range(4, len(d['level'])):
    x = d['left'][i]
    y = d['top'][i]
    w = d['width'][i]
    h = d['height'][i]
    
    # Draw rectangle
    draw.rectangle([x, y, x + w, y + h], outline="green", width=3)

img.show()

result = ''

for char in d['text']: 
    result += char

print(result)