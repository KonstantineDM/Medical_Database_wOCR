from tkinter import *


class Table:
    """
    A simple class for representing data (tuples embedded in list)
    in the form of a table
    """
    def __init__(self, parent, data_list: list):
        self.parent = parent
        self.data_list = data_list
        self.total_rows = len(data_list)
        self.total_columns = len(data_list[0])
        self.create_table()
        self.create_header()

    def create_header(self):
        # Create a header for columns in the table (overload in subclass)
        pass

    def create_table(self):
        # Create rows from data in data_list
        for r in range(self.total_rows):
            for c in range(self.total_columns):
                self.entry = Entry(self.parent, font=('Times', 16),
                                   borderwidth=1, relief='solid')
                self.entry.grid(row=r, column=c)
                self.entry.insert(END, self.data_list[r][c])

class MDB_Table(Table):
    """
    A subclass specific for the medical database table
    """
    def create_header(self):
        # Create header for the table
        col_names = ('ИД', 'Тема', 'Описание')
        for name in col_names:
            if name == 'Описание':
                self.entry = Entry(self.parent, width=70, font=('Times', 16),
                                   borderwidth=1, relief='solid')
                self.entry.grid(row=0, column=col_names.index(name))
                self.entry.insert(END, name)
            else:
                self.entry = Entry(self.parent, font=('Times', 16),
                                   borderwidth=1, relief='solid')
                self.entry.grid(row=0, column=col_names.index(name))
                self.entry.insert(END, name)

    def create_table(self):
        # Create rows from data in data_list
        for r in range(1, self.total_rows):
            for c in range(0, self.total_columns-4):
                if c == 2:
                    self.entry = Entry(self.parent, width=70, font=('Times', 16),
                                       borderwidth=1, relief='solid')
                    self.entry.grid(row=r, column=c)
                    self.entry.insert(0, self.data_list[r][c])
                else:
                    self.entry = Entry(self.parent, font=('Times', 16),
                                       borderwidth=1, relief='solid')
                    self.entry.grid(row=r, column=c)
                    self.entry.insert(0, self.data_list[r][c])
