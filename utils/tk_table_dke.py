from tkinter import *


class Table:
    """
    A simple class for representing data (tuples embedded in list)
    in the form of a table
    """
    def __init__(self, data_list: list, parent=None):

        self.total_rows = len(data_list)
        self.total_columns = len(data_list[0])

        for r in range(self.total_rows):
            for c in range(self.total_columns):
                self.entry = Entry(parent, font=('Times', 16), borderwidth=1, relief='solid')
                self.entry.grid(row=r, column=c)
                self.entry.insert(END, data_list[r][c])
