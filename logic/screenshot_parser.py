from PIL import ImageGrab
import cv2 as cv
import numpy as np

img = ImageGrab.grabclipboard()

height, width = img.size[0]*2, img.size[1]*2

if img is None:
    print("Clipboard doesn't contain an image")
else:
    img = img.resize((height, width))
    print("1")

img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])

img_gray = cv.filter2D(img_gray, -1, kernel)

_, tresh = cv.threshold(img_gray, 127, 255, 0)

cv.imshow('Contours', img)
cv.waitKey(0)
cv.destroyAllWindows()

contours, hierarchy = cv.findContours(tresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

blank_image = np.ones((width+100, height+40, 3), np.uint8) * 0

cv.drawContours(blank_image, contours, -1, (255,255,255), thickness=cv.FILLED)

print(hierarchy[0])

blank_image = cv.filter2D(blank_image, -1, kernel)

blank_image = cv.bilateralFilter(blank_image, 9, 75, 75)

# Display the image
cv.imshow('Contours', blank_image)
cv.waitKey(0)
cv.destroyAllWindows()