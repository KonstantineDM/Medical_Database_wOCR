from tkinter import Menu


class MenuBar():
    # Create a menu bar for the main.py GUI
    def __init__(self, parent=None, **configs):
        self.parent = parent
        menu_bar = Menu(parent)

        # Adding File menu
        file = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Файл', menu=file)
        file.add_separator()
        file.add_command(label='Выход', command=parent.destroy)

        # Display menu in parent
        parent.config(menu=menu_bar)
