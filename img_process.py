import pytesseract
import cv2
import numpy as np

# Directory with Images (default)
img_dir = './samples'

###### REMOVE HORIZONTAL UNDERSCORE LINES (thick marker or smth) ######
# Read
img = cv2.imread('./samples/Image.png')

# Convert to gray colours
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create kernel for long horizontal lines
# and apply morph-close operation
kernel = np.ones((5, 15), np.uint8)
morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.imwrite('./samples/line_detected.png', morphed)

# Invert the morphed image, and add to the source image:
dst = cv2.add(gray, (255-morphed))
cv2.imwrite('./samples/line_removed.png', dst)

#------------------------------------------------------------------------------
# img = cv2.imread('./samples/undies_1.jpg', 0)
# img = cv2.bitwise_not(img)
#
# # (1) clean up noises
# kernel_clean = np.ones((2,2),np.uint8)
# cleaned = cv2.erode(img, kernel_clean, iterations=1)
#
# # (2) Extract lines
# kernel_line = np.ones((1, 5), np.uint8)
# clean_lines = cv2.erode(cleaned, kernel_line, iterations=6)
# clean_lines = cv2.dilate(clean_lines, kernel_line, iterations=6)
#
# # (3) Subtract lines
# cleaned_img_without_lines = cleaned - clean_lines
# cleaned_img_without_lines = cv2.bitwise_not(cleaned_img_without_lines)
#
# plt.imshow(cleaned_img_without_lines)
# plt.show()
# cv2.imwrite('./samples/img_wanted.jpg', cleaned_img_without_lines)

#------------------------------------------------------------------------------
# im = cv2.imread('./samples/undies_1.jpg')
# gray = 255 - cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
#
# # prepare a mask using Otsu threshold, then copy from original.
# this removes some noise
# __, bw = cv2.threshold(cv2.dilate(gray, None), 128, 255, cv2.THRESH_BINARY or cv2.THRESH_OTSU)
# gray = cv2.bitwise_and(gray, bw)
# # make copy of the low-noise underlined image
# grayu = gray.copy()
# imcpy = im.copy()
# # scan each row and remove lines
# for row in range(gray.shape[0]):
#     avg = np.average(gray[row, :] > 16)
#     if avg > 0.9:
#         cv2.line(im, (0, row), (gray.shape[1]-1, row), (0, 0, 255))
#         cv2.line(gray, (0, row), (gray.shape[1]-1, row), (0, 0, 0), 1)
#
# cont = gray.copy()
# graycpy = gray.copy()
# # after contour processing, the residual will contain small contours
# residual = gray.copy()
# # find contours
# contours, hierarchy = cv2.findContours(cont, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# for i in range(len(contours)):
#     # find the boundingbox of the contour
#     x, y, w, h = cv2.boundingRect(contours[i])
#     if 10 < h:
#         cv2.drawContours(im, contours, i, (0, 255, 0), -1)
#         # if boundingbox height is higher than threshold, remove the contour from residual image
#         cv2.drawContours(residual, contours, i, (0, 0, 0), -1)
#     else:
#         cv2.drawContours(im, contours, i, (255, 0, 0), -1)
#         # if boundingbox height is less than or equal to threshold, remove the contour gray image
#         cv2.drawContours(gray, contours, i, (0, 0, 0), -1)
#
# # now the residual only contains small contours. open it to remove thin lines
# st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# residual = cv2.morphologyEx(residual, cv2.MORPH_OPEN, st, iterations=1)
# # prepare a mask for residual components
# __, residual = cv2.threshold(residual, 0, 255, cv2.THRESH_BINARY)
#
# cv2.imshow("gray", gray)
# cv2.imshow("residual", residual)
#
# # combine the residuals. we still need to link the residuals
# combined = cv2.bitwise_or(cv2.bitwise_and(graycpy, residual), gray)
# # link the residuals
# st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 7))
# linked = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, st, iterations=1)
# cv2.imshow("linked", linked)
# # prepare a msak from linked image
# __, mask = cv2.threshold(linked, 0, 255, cv2.THRESH_BINARY)
# # copy region from low-noise underlined image
# clean = 255 - cv2.bitwise_and(grayu, mask)
# cv2.imshow("clean", clean)
# cv2.imshow("im", im)

#------------------------------------------------------------------------------

###### RECOGNIZE TEXT FROM GIVEN IMAGE AND SAVE IT TO A FILE ######
samples_path = r'.\samples\line_removed.png'

pytesseract.pytesseract.tesseract_cmd = r'D:\code\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(samples_path, lang='rus+eng')
print(text)

#------------------------------------------------------------------------------
###### REMOVE NEW LINE SYMBOLS FROM RECOGNIZED TEXT ######
# text = '''Учитывая, что нарушение функции
# митохондрий явно связано с ожирением и
# диабетом 2 типа, неудивительно, что
# существует большой интерес к
# '''

text = text.split(' ')
res = ''
for word in text:
    word = word.replace('\n', ' ')
    res += ' '+ word

print(res)

#------------------------------------------------------------------------------
###### CROP IMAGE TO DELETE "Author" and  "Send message" bars in Instagram ######
# image = cv2.imread('./samples/undies_1.png')
# x1 = 0
# y1 = 100
# x2 = 720
# y2 = 1200
# crop = image[y1:y2, x1:x2]
# cv2.imwrite('./samples/Image.png', crop)
# cv2.waitKey(0)


if __name__ == '__main__':
    from tkinter import *

    def choose(): pass
    def process(): pass

    root = Tk()
    Button(root, text='Выбрать картинку', command=choose).pack()
    Button(root, text='Распознать текст', command=process).pack()
