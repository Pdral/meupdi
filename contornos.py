import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('sementes1.jpeg')
image.thumbnail((255,351))
plt.imshow("resize", image)
plt.show()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)
canny = cv2.Canny(gray, 130, 255)
#cv2.imshow("canny", canny)

cnts = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print(cnts)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    cv2.drawContours(image,[c], 0, (0,255,0), 3)

cv2.imshow("result", image)
cv2.waitKey(0)