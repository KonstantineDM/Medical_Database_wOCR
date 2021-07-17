from tkinter import *
from PIL import ImageTk, Image

class ShowImage(Toplevel):
    # global bg2, bg_resized, new_bg

    def __init__(self, parent=None, filepath=None):
        Toplevel.__init__(self)
        parent.withdraw()
        self.filepath = filepath
        self.title('Просмотр изображения')
        self.geometry('504x896+50+50')
        self.bind('<Configure>', self.resizer)
        self.bind('<Escape>', lambda x: self.destroy())

        # Define image
        self.bg = ImageTk.PhotoImage(file=self.filepath)
        #self.bg = Image.open(self.filepath)

        # Create canvas
        self.my_canvas = Canvas(self)
        self.my_canvas.pack(fill=BOTH, expand=YES)

        # Set image in canvas
        self.my_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        # Add text to canvas
        self.my_canvas.create_text(250, 20, text='Esc - закрыть изображение')

    def resizer(self, event):
        # Open image
        self.bg2 = Image.open(self.filepath)
        # Resize image
        self.bg_resized = self.bg2.resize((event.width, event.height),
                                         Image.ANTIALIAS)
        # Define resized image
        self.new_bg = ImageTk.PhotoImage(self.bg_resized)
        # Readd image to the canvas
        self.my_canvas.create_image(0, 0, image=self.new_bg, anchor='nw')
        # Readd text to canvas
        self.my_canvas.create_text(event.width//2, 20, text='Esc - закрыть изображение')
        self.my_canvas.create_text(event.width // 2, 40, text=self.filepath)

def show_img(parent, filepath):
    show = ShowImage(parent, filepath=filepath)
    show.grab_set()
    show.focus_set()


if __name__ == '__main__':
    filepath = '.\samples\line_removed.png'
    # root = Tk()
    # show = ShowImage(root, filepath=filepath)
    # show.mainloop()
    #show_img(filepath)
