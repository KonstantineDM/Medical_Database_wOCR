# Creator   : Konstantin Davydov
# # Start date: 2021-07-03 (Y-M-D)
# # End date  : None

"""
Program for managing database with records on medical educational info;
Can show, add, update, delete records in database;
Database is an SQLite database
"""

# TODO: when showing image, make image window the active one
# TODO: get the hold of Git

from distutils import command
from tkinter import *
# from openpyxl.workbook import Workbook
# from openpyxl import load_workbook
from showimage import show_img
from showimage import ShowImage
from choosefile import ChooseIMG

# filepath = ''  # ./samples/line_removed.png

##### EXCEL SHIT (MAYBE REWRITE) #####

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

# Creating tkinter main window
root = Tk()
root.title('ЭЛЕКТРОННЫЙ СПРАВОЧНИК')    # Название окна программы
root.iconbitmap('squirrel.ico')

##### MENU BAR #####
# Creating menu bar
menubar = Menu(root)

# Adding File menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=None)
file.add_command(label='Open', command=None)
file.add_command(label='Save', command=None)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

# Adding Edit menu and commands
edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Placeholder', command=None)

# Display menu
root.config(menu=menubar)

##### MAIN FRAME #####
# Create Main Frame
frame = LabelFrame(root, text='Справочник учебной мед.информации',
                   padx=100, pady=100)
frame.pack(expand=YES, fill=BOTH, padx=10, pady=10)

# Create buttons
choose_img = ChooseIMG(frame)
choose_img.pack()
showimage = Button(frame, text='Show IMG',
                   command=lambda: show_img(root, ChooseIMG.filepath))
showimage.pack()

root.mainloop()
