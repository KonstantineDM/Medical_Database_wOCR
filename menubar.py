from tkinter import Menu


class MenuBar():
    """Create a menu bar in the GUI"""
    def __init__(self, parent=None, **configs):

        # Creating menu bar
        menu_bar = Menu(parent)

        # Adding File menu and commands
        file = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Файл', menu=file)
        file.add_command(label='Создать файл', command=None)
        file.add_command(label='Открыть файл', command=None)
        file.add_command(label='Сохранить', command=None)
        file.add_separator()
        file.add_command(label='Выход', command=parent.destroy)

        # Adding Edit menu and commands
        edit = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Редактировать', menu=edit)
        edit.add_command(label='Placeholder', command=None)

        # Display menu
        parent.config(menu=menu_bar)
