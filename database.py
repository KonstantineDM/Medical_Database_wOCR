import sqlite3
from tkinter import *
from tkinter import messagebox
import os
from utils.tk_table_dke import MDB_Table


# TODO: поле описания сделать расширяемым (кнопку для открытия поля "Описание" в отдельном окне?)

def database():
    """
    Main function for creating the database (db);

    Contains functions:
        delete - delete a record from db by the data in choose_box;
        submit - confirm adding new record to the db;
        query - make a query to the db to show the list of records;
        save_changes - commit changes to the chosen db record;
        edit - opens a GUI for editing db record (chosen in the choose_box);
    """
    # Create main window for db, separately from main.py GUI
    root = Tk()
    root.title('БАЗА ДАННЫХ')    # Название окна программы
    root.geometry('720x460')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    if os.path.isfile('squirrel.ico'): root.iconbitmap('squirrel.ico')
    root.grab_set()
    root.focus_force()

    # Create a database or connect to one
    conn = sqlite3.connect('database_med.db')
    # Create cursor
    c = conn.cursor()

    # Create table if none exists
    c.execute("""CREATE TABLE IF NOT EXISTS database 
                (
                    topic text,
                    description text,
                    symptoms text,
                    treatment text,
                    picts_videos blob,
                    notes text
                )"""
    )


    def delete():
        # Delete a chosen record from db (type in choose_box)
        ask_yesno = messagebox.askquestion('Удалить запись',
                                           'Вы уверены, что хотите удалить запись?',
                                           icon = 'warning')
        if ask_yesno == 'yes':
            conn = sqlite3.connect('database_med.db')
            c = conn.cursor()

            # Delete a record (by record's ID)
            c.execute("DELETE FROM database"
                      " WHERE oid=" + "'" + choose_box.get() + "'")
            # Clear the choose_box
            choose_box.delete(0, END)

            # Commit changes and close connection
            conn.commit()
            conn.close()
        else: pass


    def submit():
        # Confirm adding new record to the db

        # Prevent adding empty record to the DB
        for entry in (topic.get(),
                      description.get("1.0", "end-1c")):
            if len(entry) == 0:
                messagebox.showerror(title="Пустая запись не допустима",
                                     message="Поля 'Тема' и 'Описание' "
                                             "должны быть заполнены")
                break
            else:
                conn = sqlite3.connect('database_med.db')
                c = conn.cursor()

                c.execute("INSERT INTO database VALUES (:topic, :description, :symptoms, :treatment, :picts_videos, :notes)",
                          {
                              'topic': topic.get(),
                              'description': description.get("1.0", "end-1c"),
                              'symptoms': symptoms.get(),
                              'treatment': treatment.get(),
                              'picts_videos': picts_videos.get(),
                              'notes': notes.get()
                          }
                          )

                # Commit changes and close connection
                conn.commit()
                conn.close()

                # Clear the textboxes
                topic.delete(0, END)
                description.delete("1.0", END)
                symptoms.delete(0, END)
                treatment.delete(0, END)
                picts_videos.delete(0, END)
                notes.delete(0, END)
                break


    def query():
        """
        Make a query to the db to show the preview list of records;
        Represent query's results in the form of a table in a new window;
        """

        conn = sqlite3.connect('database_med.db')
        c = conn.cursor()

        # Query the database (by record's ID)
        c.execute('SELECT oid, * FROM database')
        records = c.fetchall()

        # Display records in the form of a table
        record_window = Toplevel()
        MDB_Table(record_window, records)

        # Commit changes and close connection
        conn.commit()
        conn.close()


    def save_changes(parent):
        # Commit changes to the chosen db record

        # Prevent adding empty record to the DB
        for entry in (topic_editor.get(),
                      description_editor.get("1.0", "end-1c")):
            if len(entry) == 0:
                messagebox.showerror(title="Пустая запись не допустима",
                                     message="Поля 'Тема' и 'Описание' "
                                             "должны быть заполнены")
                break
            else:
                conn = sqlite3.connect('database_med.db')
                c = conn.cursor()

                # Update record, chosen by its ID (oid)
                c.execute("""UPDATE database SET
                    topic = :topic,
                    description = :description,
                    symptoms = :symptoms,
                    treatment = :treatment,
                    picts_videos = :picts_videos,
                    notes = :notes
                    
                    WHERE oid = :oid""",
                    {
                        "oid": choose_box.get(),
                        "topic": topic_editor.get(),
                        "description": description_editor.get("1.0", END),
                        "symptoms": symptoms_editor.get(),
                        "treatment": treatment_editor.get(),
                        "picts_videos": picts_videos_editor.get(),
                        "notes": notes_editor.get()
                    }
                )

                # Commit changes and close connection
                conn.commit()
                conn.close()


    def edit():
        # Opens a GUI for editing db record, chosen in the choose_box

        # Make edit boxes names global
        global topic_editor
        global description_editor
        global symptoms_editor
        global treatment_editor
        global picts_videos_editor
        global notes_editor

        # Creating a new window
        editor = Tk()
        editor.title('РЕДАКТИРОВАНИЕ ЗАПИСИ')
        editor.geometry('620x400')
        editor.iconbitmap('squirrel.ico')

        conn = sqlite3.connect('database_med.db')
        c = conn.cursor()

        # Query the database (by record's ID)
        record_id = choose_box.get()
        c.execute('SELECT * FROM database WHERE oid=' + '"' + record_id + '"')
        records = c.fetchall()

        # Check if chosen record exists; Warning if it doesn't;
        # Hide and then close Editor window
        if len([record[0] for record in records]) == 0:
            editor.withdraw()
            messagebox.showerror("Ошибка", "Такой записи в базе нет")
            editor.destroy()
            return

        # Create edit boxes
        topic_editor = Entry(editor, width=80)
        topic_editor.grid(row=0, column=1, padx=10, pady=(10,3), sticky=E+W)
        description_editor = Text(editor, width=0, height=10, wrap=WORD)
        description_editor.grid(row=1, column=1, padx = 10, pady=(5,3), sticky=E+W)
        symptoms_editor = Entry(editor, width=50)
        symptoms_editor.grid(row=2, column=1, padx=10, pady=(5,3), sticky=E+W)
        treatment_editor = Entry(editor, width=50)
        treatment_editor.grid(row=3, column=1, padx=10, pady=(5,3), sticky=E+W)
        picts_videos_editor = Entry(editor, width=50)
        picts_videos_editor.grid(row=4, column=1, padx=10, pady=(5,3), sticky=E+W)
        notes_editor = Entry(editor, width=50)
        notes_editor.grid(row=5, column=1, padx=10, pady=(5,3), sticky=E+W)

        # Create edit box labels
        topic_label_editor = Label(editor, text='Тема', width=15, anchor=E)
        topic_label_editor.grid(row=0, column=0)
        description_label_editor = Label(editor, text='Описание', width=15, anchor=E)
        description_label_editor.grid(row=1, column=0)
        symptoms_label_editor = Label(editor, text='Симптомы', width=15, anchor=E)
        symptoms_label_editor.grid(row=2, column=0)
        treatment_label_editor = Label(editor, text='Лечение', width=15, anchor=E)
        treatment_label_editor.grid(row=3, column=0)
        picts_videos_label_editor = Label(editor, text='Картинки и Видео', width=15, anchor=E)
        picts_videos_label_editor.grid(row=4, column=0)
        notes_label_editor = Label(editor, text='Примечание', width=15, anchor=E)
        notes_label_editor.grid(row=5, column=0)

        # Insert record's info into entry boxes of the Edit window
        for record in records:
            topic_editor.insert(0, record[0])
            description_editor.insert("1.0", record[1])
            symptoms_editor.insert(0, record[2])
            treatment_editor.insert(0, record[3])
            picts_videos_editor.insert(0, record[4])
            notes_editor.insert(0, record[5])


        def clear_all_editor():
            # Clear all fields in the Edit window
            topic_editor.delete(0, END)
            description_editor.delete("1.0", END)
            symptoms_editor.delete(0, END)
            treatment_editor.delete(0, END)
            picts_videos_editor.delete(0, END)
            notes_editor.delete(0, END)

        # Create a Save Changes button
        save_chng_btn = Button(editor, text='Сохранить изменения', command=lambda: save_changes(editor))
        save_chng_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Create a Clear All Fields button
        clear_all = Button(editor, text='Очистить все поля', command=clear_all_editor)
        clear_all.grid(row=7, column=0, columnspan=2, pady=5, padx=10, ipadx=110)

        # Commit changes and close connection
        conn.commit()
        conn.close()


    def expand_text():
        # Expand the "Description"" field of a record to allow reading
        # the whole text in it (for when it contains a lot of text)
        root = Toplevel()
        root.geometry("1200x700")
        text_exp = Text(root)
        text_exp.pack(fill=BOTH, expand=YES)
        text_exp.insert("1.0", description.get("1.0", "end-1c"))


    def display():
        # Display the chosen record in a new window

        display = Tk()
        display.title('ПРОСМОТР ЗАПИСИ')
        display.geometry('650x750')
        display.iconbitmap('squirrel.ico')

        conn = sqlite3.connect('database_med.db')
        c = conn.cursor()

        # Query the database (by record's ID)
        record_id = choose_box.get()
        c.execute('SELECT * FROM database WHERE oid=' + '"' + record_id + '"')
        records = c.fetchall()

        if len([record[0] for record in records]) == 0:
            display.withdraw()
            messagebox.showerror("Ошибка", "Такой записи в базе нет")
            display.destroy()
            return

        # Create display boxes
        topic_display = Entry(display, width=80)
        topic_display.grid(row=0, column=1, padx=10, pady=(10,3), sticky=E+W)
        description_display = Text(display, width=0, height=10, wrap=WORD)
        description_display.grid(row=1, column=1, padx = 10, pady=(5,3), sticky=E+W)
        symptoms_display = Text(display, width=0, height=10, wrap=WORD)
        symptoms_display.grid(row=2, column=1, padx=10, pady=(5,3), sticky=E+W)
        treatment_display = Text(display, width=0, height=10, wrap=WORD)
        treatment_display.grid(row=3, column=1, padx=10, pady=(5,3), sticky=E+W)
        picts_videos_display = Entry(display, width=50)
        picts_videos_display.grid(row=4, column=1, padx=10, pady=(5,3), sticky=E+W)
        notes_display = Text(display, width=0, height=10, wrap=WORD)
        notes_display.grid(row=5, column=1, padx=10, pady=(5,3), sticky=E+W)

        # Create display box labels
        topic_label_display = Label(display, text='Тема', width=15, anchor=E)
        topic_label_display.grid(row=0, column=0)
        description_label_display = Label(display, text='Описание', width=15, anchor=E)
        description_label_display.grid(row=1, column=0)
        symptoms_label_display = Label(display, text='Симптомы', width=15, anchor=E)
        symptoms_label_display.grid(row=2, column=0)
        treatment_label_display = Label(display, text='Лечение', width=15, anchor=E)
        treatment_label_display.grid(row=3, column=0)
        picts_videos_label_display = Label(display, text='Картинки и Видео', width=15, anchor=E)
        picts_videos_label_display.grid(row=4, column=0)
        notes_label_display = Label(display, text='Примечание', width=15, anchor=E)
        notes_label_display.grid(row=5, column=0)

        # Insert record's info into entry boxes of the Edit window
        for record in records:
            topic_display.insert(0, record[0])
            description_display.insert("1.0", record[1])
            symptoms_display.insert("1.0", record[2])
            treatment_display.insert("1.0", record[3])
            picts_videos_display.insert(0, record[4])
            notes_display.insert("1.0", record[5])


    # Create entry boxes
    topic = Entry(root, width=80)
    topic.grid(row=0, column=1, columnspan=4, padx=10, pady=(10,3), sticky=E+W)
    description = Text(root, width=0, height=10, wrap=WORD)
    description.grid(row=1, column=1, columnspan=4, padx = 10, pady=(5,3), sticky=E+W)
    symptoms = Entry(root, width=50)
    symptoms.grid(row=2, column=1, columnspan=4, padx=10, pady=(5,3), sticky=E+W)
    treatment = Entry(root, width=50)
    treatment.grid(row=3, column=1, columnspan=4, padx=10, pady=(5,3), sticky=E+W)
    picts_videos = Entry(root, width=50)
    picts_videos.grid(row=4, column=1, columnspan=4, padx=10, pady=(5,3), sticky=E+W)
    notes = Entry(root, width=50)
    notes.grid(row=5, column=1, columnspan=4, padx=10, pady=(5,3), sticky=E+W)
    choose_box = Entry(root, width=20)
    choose_box.grid(row=10, column=1, padx=10, pady=(10,3), sticky=W)

    # Create entry box labels
    topic_label = Label(root, text='Тема', width=15, anchor=E)
    topic_label.grid(row=0, column=0)
    # description_label = Label(root, text='Описание', width=15, anchor=E)
    # description_label.grid(row=1, column=0)
    description_label = Button(root, text='Описание (раскрыть)',
                               command=expand_text, justify='center')
    description_label.grid(row=1, column=0, sticky=E, padx=10)
    symptoms_label = Label(root, text='Симптомы', width=15, anchor=E)
    symptoms_label.grid(row=2, column=0)
    treatment_label = Label(root, text='Лечение', width=15, anchor=E)
    treatment_label.grid(row=3, column=0)
    picts_videos_label = Label(root, text='Картинки и Видео', width=15, anchor=E)
    picts_videos_label.grid(row=4, column=0)
    notes_label = Label(root, text='Примечание', width=15, anchor=E)
    notes_label.grid(row=5, column=0)
    choose_label= Label(root, text='Выберите запись\n(ИД)', width=15, anchor=E)
    choose_label.grid(row=10, column=0)

    # Create submit button
    submit_btn = Button(root, text='Добавить запись в справочник', command=submit)
    submit_btn.grid(row=6, column=1, columnspan=4, pady=(10,5), padx=10, sticky=W+E)

    # Create s Query button
    query_btn = Button(root, text='Показать список тем', command=query)
    query_btn.grid(row=7, column=1, columnspan=4, pady=(5,10), padx=10, sticky=W+E)

    # Create a display button
    display_btn = Button(root, text='Показать запись', command=display)
    display_btn.grid(row=10, column=2, pady=10, padx=5)

    # Create an Update button
    edit_btn = Button(root, text='Редактировать запись', command=edit)
    edit_btn.grid(row=10, column=3, pady=10, padx=5)

    # Create a Delete button
    delete_btn = Button(root, text='Удалить запись', command=delete)
    delete_btn.grid(row=10, column=4, pady=10, padx=10)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    root.mainloop()


if __name__ == '__main__':
    database()