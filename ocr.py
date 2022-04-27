import cv2 
import pytesseract

img = cv2.imread("/home/sebastian/2f05e196-c6b2-4694-953c-daa69846cb1d.jpg")
print(type(img))
# Adding custom options
custom_config = r'--oem 1 --psm 6'
text = pytesseract.image_to_string(img, lang='spa')
print(text)