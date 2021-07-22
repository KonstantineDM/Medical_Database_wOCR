from tkinter import Menu


class MenuBar():
    """Create a menu bar in the GUI"""
    def __init__(self, parent=None, **configs):
        self.parent = parent
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

        # TODO: consider implementing switch between bright and dark themes
        # # Add Theme menu
        # theme = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label='Выбор темы', menu=theme)
        # theme.add_command(label='Светлая', command=self.bright_theme)
        # theme.add_command(label='Темная', command=self.dark_theme)

        # Display menu
        parent.config(menu=menu_bar)

    # def bright_theme(self):
    #     self.parent.configure(bg='white')
    #
    # def dark_theme(self):
    #     self.parent.configure(bg='gray')
