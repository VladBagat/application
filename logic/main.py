from PIL import Image, ImageDraw
import pytesseract as ts
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

img = Image.open(r'test1.png')

scale = 1             

img = img.resize((img.size[0]*scale, img.size[1]*scale), 3)
            
vertical_config = r'--oem 3 -l jpn_vert tessedit_char_whitelist=0123456789'
horizontal_config = r'--oem 3 -l jpn tessedit_char_whitelist=0123456789'

vertical_text = ts.image_to_data(img, lang='jpn_vert', output_type=Output.DICT, config=vertical_config)
horizontal_text = ts.image_to_data(img, lang='jpn', output_type=Output.DICT, config=horizontal_config)

vertical_confidence = sum(vertical_text['conf'])/len(vertical_text['conf'])
horizontal_confidence = sum(horizontal_text['conf'])/len(horizontal_text['conf'])

if vertical_confidence > horizontal_confidence:
    d = vertical_text
else:
    d = horizontal_text

print(d)

result = ''

for char in d['text']: 
    result += char

print(result)

def show_text():

    draw = ImageDraw.Draw(img)

    for i in range(4, len(d['level'])):
        x = d['left'][i]
        y = d['top'][i]
        w = d['width'][i]
        h = d['height'][i]
        
        # Draw rectangle
        draw.rectangle([x, y, x + w, y + h], outline="green", width=3)

    img.show()

