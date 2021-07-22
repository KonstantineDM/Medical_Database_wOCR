# Creator   : Konstantin Davydov
# # Start date: 2021-07-03 (Y-M-D)
# # End date  : None

"""
Program for managing database with records on educational medical info;
Can show, add, update, delete records in database (implemented as SQLite db);

The second option in the main window opens an OCR tool GUI (based on pytesseract):
 - choose image
 - process the image (ROI, morphology, clean marks)
 - recognize text in the image and save it to a file for further use
"""

# TODO: when showing image, make image window the active one

import os
from distutils import command
from tkinter import *
import database
import fonts_db
from img_process import image_process
from menubar import MenuBar
# from openpyxl.workbook import Workbook
# from openpyxl import load_workbook

# filepath = ''  # ./samples/line_removed.png

##### EXCEL STUFF !EXPERIMENTAL  ##### #TODO: ADD OUTPUT TO EXCEL FILE -  IS IT NEEDED?

# Load existing workbook
# wb = load_workbook('database.xlsx')

# Create an active worksheet
# ws = wb.active

# Print something from workbook
# print(ws['A2'].value)
# print()
# print(ws['B2'].value)
# print()
# print(ws['C2'].value)
# print()
# print(ws['D2'].value)

# Create directory for pictures if it doesn't exist
if os.path.isdir('.\samples'):
    pass
else:
    os.mkdir('.\samples')

# Creating tkinter main window
root = Tk()
root.title('ЭЛЕКТРОННЫЙ СПРАВОЧНИК')    # Название окна программы
root.geometry('800x550')
if os.path.isfile('squirrel.ico'): root.iconbitmap('squirrel.ico')

##### MENU BAR #####
menu_bar = MenuBar(root)

##### MAIN FRAME #####
# Create Main Frame
frame = LabelFrame(root,
                   text='Справочник учебной мед.информации',
                   font=fonts_db.font_medium(root),
                   padx=120,
                   pady=100,)
frame.pack(expand=YES, fill=BOTH, padx=10, pady=10)

##### BUTTONS (MAIN FUNCTIONALITY) #####
# Create buttons
database_open = Button(frame,
                       text='Открыть базу данных',
                       font=fonts_db.font_large(root),
                       command=database.database)
database_open.pack(fill=X, expand=YES, pady=20, ipadx=100)
image_recognition = Button(frame,
                       text='Распознавание изображения',
                       font=fonts_db.font_large(root),
                       command=image_process)
image_recognition.pack(fill=X, expand=YES, pady=20, ipadx=100)


root.mainloop()
