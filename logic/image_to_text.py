from PIL import Image, ImageDraw
import pytesseract as ts
from pytesseract import Output

#Can't directly handle batch 
class Tesseract():
    def __init__(self) -> None:
        ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.__vertical_config = r'--oem 3 -l jpn_vert tessedit_char_whitelist=0123456789'
        self.__horizontal_config = r'--oem 3 -l jpn tessedit_char_whitelist=0123456789'
        self.__image = None

    def text_from_image(self, src) -> str:
        self.__load_image(src)

        return self.__analyze_image()

    def __load_image(self, src):
        image = Image.open(src)

        scale = 1             
        image = image.resize((image.size[0]*scale, image.size[1]*scale), 3)

        self.__image = image
                
    def __analyze_image(self):
        vertical_text = ts.image_to_data(self.__image, lang='jpn_vert', output_type=Output.DICT, config=self.__vertical_config)
        horizontal_text = ts.image_to_data(self.__image, lang='jpn', output_type=Output.DICT, config=self.__horizontal_config)

        vertical_confidence = sum(vertical_text['conf'])/len(vertical_text['conf'])
        horizontal_confidence = sum(horizontal_text['conf'])/len(horizontal_text['conf'])

        if vertical_confidence > horizontal_confidence:
            d = vertical_text
        else:
            d = horizontal_text

        result = ''

        for char in d['text']: 
            result += char

        return [result]

#Debugging only
'''
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
'''


