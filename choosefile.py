import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from utils import fonts_db

class ChooseIMG(tk.Frame):
    filepath = ''

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        # self.title('Распознавание изображения')
        self.choose = tk.Button(parent, text='Выберите изображение',
                                command=self.choose_file,
                                font=fonts_db.font_medium(parent))
        self.choose.grid(row=0, column=0, padx=20, pady=20)
        self.chosen = tk.Entry(parent, width=65,
                              font=fonts_db.font_small(parent))
        #self.chosen.insert(0, self.filepath)
        self.chosen.grid(row=0, column=1, columnspan=2, padx=20)

    # Create 'Choose File' button
    def choose_file(self):
        ChooseIMG.filepath = tk.filedialog.askopenfilename(initialdir='./samples',
                                                      filetypes=(('All Files', '*.*'),
                                                                 ('JPEG Files', '*.jpg'),
                                                                 ('PNG Files', '*.png')))
        try:
            self.my_image = ImageTk.PhotoImage(Image.open(ChooseIMG.filepath))
        except AttributeError: pass
        #image_label = tk.Label(image=self.my_image)
        #image_label.pack()
        # Set chosen file to entry widget
        self.set_chosen(ChooseIMG.filepath)

    # Set value of "Chosen File" to entry box
    def set_chosen(self, filename):
        self.chosen.delete(0, tk.END)
        self.chosen.insert(0, '/'.join(ChooseIMG.filepath.split('/')))


if __name__ == '__main__':
    root = tk.Tk()
    ChooseIMG(root)
    root.mainloop()
    print('Chosen File:', ChooseIMG.filepath)

##### BACKUP CODE AS FUNCTIONS

# # Create main window
# root = tk.Tk()
# root.title('Распознавание изображения')
# root.geometry('650x700')
# filepath = ''
#
# # Create 'Choose File' button
# def choose_file():
#     global filepath
#     filepath = tk.filedialog.askopenfilename(initialdir='./samples',
#                                               filetypes=(('All Files', '*.*'),
#                                                          ('JPEG Files', '*.jpg'),
#                                                          ('PNG Files', '*.png')))
#     my_image = ImageTk.PhotoImage(Image.open(filepath))
#     image_label = tk.Label(image=my_image)
#     image_label.pack()
#     # Set chosen file to entry widget
#     set_chosen(filepath)
#
# # Set value of "Chosen File" to entry box
# def set_chosen(filepath):
#     chosen.delete(0, tk.END)
#     chosen.insert(0, '/'.join(filepath.split('/')[-3:]))
#
# choose_file = tk.Button(root, text='Выберите изображение',
#                         command=choose_file)
# choose_file.pack(padx=20, side=tk.LEFT)
# chosen = tk.Entry(root, width=50)
# chosen.insert(0, filepath)
# chosen.pack(side=tk.LEFT)
#
# root.mainloop()
