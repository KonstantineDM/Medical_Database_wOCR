import os
from tkinter import *
import database
import fonts_db
from img_process import image_process
from menubar import MenuBar


"""
Main script to launch the program;

Opens main GUI window with two buttons:
    - Open database ("Открыть базу данных")
    - Image recognition ("Распознавание изображения")
"""

# Create directory for images if it doesn't exist
if os.path.isdir('.\samples'):
    pass
else:
    os.mkdir('.\samples')

# Creating main window
root = Tk()
root.title('ЭЛЕКТРОННЫЙ СПРАВОЧНИК')
root.geometry('800x550')
# Use custom icon if present in cwd
if os.path.isfile('squirrel.ico'): root.iconbitmap('squirrel.ico')

# Create Menu bar (imported)
menu_bar = MenuBar(root)

# Create Main Frame
frame = LabelFrame(root,
                   text='Справочник учебной мед.информации',
                   font=fonts_db.font_medium(root),
                   padx=120,
                   pady=100,)
frame.pack(expand=YES, fill=BOTH, padx=10, pady=10)

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
