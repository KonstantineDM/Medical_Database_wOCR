import pytesseract
import cv2
import numpy as np
import os
from tkinter import Tk, Button, E, W
from choosefile import ChooseIMG
from utils import fonts_db

# TODO: how to pack pytesseract with pyinstaller (code has reference to tesseract's exe)? COMPILE BINARY?
# https://stackoverflow.com/questions/59829470/pyinstaller-and-tesseract-ocr
# TODO: add choise of the file type to save text to (txt or xls or any other...)
# TODO: portability of pytesseract (for now path to it's exe is hardcoded)

# Directory with Images (default)
# img_dir = './samples'

###### REMOVE HORIZONTAL UNDERSCORE LINES (thick marker or smth) ######
def process(filepath):
    filename, fileext = os.path.splitext(filepath)

    # Read and resize IMG
    img = cv2.imread(filepath)
    img = cv2.resize(img, (720, 1080)) # (504, 756)

    # Choose only ROI in IMG

    roi = cv2.selectROI(img)

    # Crop image
    imCrop = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    cv2.imwrite(filename + '_ROI' + fileext, imCrop)

    # Convert to gray colors
    gray = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray, (3, 3))

    _, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    cv2.imshow("thresh", thresh)

    # Create kernel for long horizontal lines
    # and apply morphology operations
    kernel = np.ones((1, 20), np.uint8)
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    # cleaned = cv2.erode(morphed, kernel, iterations=1)
    cv2.imwrite(filename + '_lines_detected' + fileext, morphed)

    # Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255-morphed))
    cv2.imwrite(filename + '_lines_removed' + fileext, dst)
    filepath = filename + '_lines_removed' + fileext
    cv2.imshow('result', dst)
    cv2.waitKey(0)

    return filepath

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


###### RECOGNIZE TEXT FROM GIVEN IMAGE AND SAVE IT TO A FILE ######
def recognize(filepath):
    global text_recognized
    sample_path = filepath
    pytesseract.pytesseract.tesseract_cmd = r'D:\code\Tesseract-OCR\tesseract.exe'
    text_recognized = pytesseract.image_to_string(sample_path, lang='rus+eng')
    # print(text)
    # return text

###### REMOVE NEW LINE SYMBOLS FROM RECOGNIZED TEXT ######
###### CONVERT RECOGNIZED TEXT TO A BIG ONE LINER   ######

def text_to_one_line(text):
    text = text.replace('\n', ' ')
    text = text.split(' ')
    text = ' '.join(text)
    res_number = 1
    with open(".\\samples\\" + str(res_number) + '.txt', 'w') as file:
        print(text, file=file)
        res_number += 1
    # print(text)
    # print(".\\samples\\" + str(res_number) + ".txt")
    return text

def image_process():
    # TODO: why root everywhere? rewrite with "parent" parameter?
    # TODO: no root=Tk(), no root.mainloop() --> all done in parent
    root = Tk()
    root.title('Распознавание изображения')
    #root.attributes("-topmost", True)
    #root.grab_set()
    #root.focus_force()
    global text_recognized

    ChooseIMG(root).grid(row=1, column=1)
    process_btn = Button(root, text='Обработка изображения',
                     command=lambda: process(ChooseIMG.filepath),
                     font=fonts_db.font_small(root))
    process_btn.grid(row=1, column=0, ipadx=40, padx=10, pady=10, sticky=E)
    recognize_btn = Button(root, text='Распознавание изображения',
                       command=lambda: recognize(ChooseIMG.filepath),
                       font=fonts_db.font_small(root))
    recognize_btn.grid(row=1, column=1, ipadx=40, padx=10, pady=10)
    to_text_btn = Button(root, text='Перевод в текст',
                     command=lambda: text_to_one_line(text_recognized),
                     font=fonts_db.font_small(root))
    to_text_btn.grid(row=1, column=2, ipadx=40, padx=10, pady=10, sticky=W)

    root.lift()
    root.mainloop()


if __name__ == '__main__':
    image_process()
