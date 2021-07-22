"""
Create a database, connect it to program
"""

import sqlite3
from tkinter import *

# TODO: rewrite as class?
# TODO: поле описания сделать расширяемым (кнопку для открытия "Описание" в отдельном окне?)
# TODO: добавить запрос подтверждения на удаление (askyesno и if?)
# TODO: запрет на добавление пустой записи в базу (предупреждение или что-то типа)
# TODO: показывать список тем в отдельном окне, а не в виде Лэйбла в окне программы
# TODO: сделать редактиврование по ИД темы? а  не по ее названию

def database():
    # Creating tkinter main window
    root = Tk()
    root.title('ЭЛЕКТРОННЫЙ СПРАВОЧНИК')    # Название окна программы
    root.geometry('720x460')
    root.iconbitmap('squirrel.ico')
    root.grab_set()
    root.focus_force()

    ##### DATABASE #####
    # Create a database or connect to one
    conn = sqlite3.connect('database_med.db')

    # Create cursor
    c = conn.cursor()

    # Create table (executed only once)
    '''
    c.execute("""CREATE TABLE database 
                (
                    topic text,
                    description text,
                    symptoms text,
                    treatment text,
                    picts_videos blob,
                    notes text
                )"""
    )
    '''

    # Create a function to delete entry
    def delete():
        # Create a database or connect to one
        conn = sqlite3.connect('database_med.db')
        # Create cursor
        c = conn.cursor()

        # Delete a record
        c.execute("DELETE FROM database WHERE topic=" + "'" + choose_box.get() + "'")
        choose_box.delete(0, END)

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        # Insert into Table

    # Create a submit function for database
    def submit():
        # Create a database or connect to one
        conn = sqlite3.connect('database_med.db')
        # Create cursor
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

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

        # Clear the textboxes
        topic.delete(0, END)
        description.delete("1.0", END)
        symptoms.delete(0, END)
        treatment.delete(0, END)
        picts_videos.delete(0, END)
        notes.delete(0, END)

    # Create query function
    def query():
        # Create a database or connect to one
        conn = sqlite3.connect('database_med.db')
        # Create cursor
        c = conn.cursor()

        # Query the database
        c.execute('SELECT *, oid FROM database')
        records = c.fetchall()
        print(records)

        # Loop through results
        print_records = ''
        for record in records:
            print_records += str(record[-1]) + '\t' + str(record[0]) + '\n'

        query_label = Label(root, text=print_records)
        query_label.grid(row=13, column=0, columnspan=2)


        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

    # Create Edit function to update record
    def save_changes():
        # Create a database or connect to one
        conn = sqlite3.connect('database_med.db')
        # Create cursor
        c = conn.cursor()

        c.execute("""
            UPDATE database SET
            topic = :topic,
            description = :description,
            symptoms = :symptoms,
            treatment = :treatment,
            picts_videos = :picts_videos,
            notes = :notes
            
            WHERE oid = :oid""",
            {
                "topic": topic_editor.get(),
                "description": description_editor.get(),
                "symptoms": symptoms_editor.get(),
                "treatment": treatment_editor.get(),
                "picts_videos": picts_videos_editor.get(),
                "notes": notes_editor.get()
            }
        )

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

    def edit():
        # Creating tkinter main window
        editor = Tk()
        editor.title('РЕДАКТИРОВАНИЕ ЗАПИСИ')
        editor.geometry('620x400')
        editor.iconbitmap('squirrel.ico')

        # Create a database or connect to one
        conn = sqlite3.connect('database_med.db')
        # Create cursor
        c = conn.cursor()

        # Query the database
        record_topic = choose_box.get()
        c.execute('SELECT * FROM database WHERE topic=' + '"' + record_topic + '"')
        records = c.fetchall()

        # Create global variables for text box names
        global topic_editor
        global description_editor
        global symptoms_editor
        global treatment_editor
        global picts_videos_editor
        global notes_editor

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

        # Loop through results
        for record in records:
            topic_editor.insert(0, record[0])
            description_editor.insert("1.0", record[1])
            symptoms_editor.insert(0, record[2])
            treatment_editor.insert(0, record[3])
            picts_videos_editor.insert(0, record[4])
            notes_editor.insert(0, record[5])

        # Create a Clear All Fields function for Edit window
        def clear_all_editor():
            topic_editor.delete(0, END)
            description_editor.delete("1.0", END)
            symptoms_editor.delete(0, END)
            treatment_editor.delete(0, END)
            picts_videos_editor.delete(0, END)
            notes_editor.delete(0, END)

        # Create a Save Changes button
        save_chng_btn = Button(editor, text='Сохранить изменения', command=save_changes)
        save_chng_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Create a Clear All Fields button
        clear_all = Button(editor, text='Очистить все поля', command=clear_all_editor)
        clear_all.grid(row=7, column=0, columnspan=2, pady=5, padx=10, ipadx=110)

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()



    # Create entry boxes
    topic = Entry(root, width=80)
    topic.grid(row=0, column=1, padx=10, pady=(10,3), sticky=E+W)
    description = Text(root, width=0, height=10, wrap=WORD)
    description.grid(row=1, column=1, padx = 10, pady=(5,3), sticky=E+W)
    symptoms = Entry(root, width=50)
    symptoms.grid(row=2, column=1, padx=10, pady=(5,3), sticky=E+W)
    treatment = Entry(root, width=50)
    treatment.grid(row=3, column=1, padx=10, pady=(5,3), sticky=E+W)
    picts_videos = Entry(root, width=50)
    picts_videos.grid(row=4, column=1, padx=10, pady=(5,3), sticky=E+W)
    notes = Entry(root, width=50)
    notes.grid(row=5, column=1, padx=10, pady=(5,3), sticky=E+W)
    choose_box = Entry(root, width=30)
    choose_box.grid(row=10, column=1, padx=10, pady=(10,3), sticky=W)

    # Create entry box labels
    topic_label = Label(root, text='Тема', width=15, anchor=E)
    topic_label.grid(row=0, column=0)
    # description_label = Label(root, text='Описание', width=15, anchor=E)
    # description_label.grid(row=1, column=0)
    description_label = Button(root, text='Описание\n(раскрыть)',
                               command=None)
    description_label.grid(row=1, column=0, sticky=E, padx=10)
    symptoms_label = Label(root, text='Симптомы', width=15, anchor=E)
    symptoms_label.grid(row=2, column=0)
    treatment_label = Label(root, text='Лечение', width=15, anchor=E)
    treatment_label.grid(row=3, column=0)
    picts_videos_label = Label(root, text='Картинки и Видео', width=15, anchor=E)
    picts_videos_label.grid(row=4, column=0)
    notes_label = Label(root, text='Примечание', width=15, anchor=E)
    notes_label.grid(row=5, column=0)
    choose_label= Label(root, text='Выберите тему', width=15, anchor=E)
    choose_label.grid(row=10, column=0)

    # Create submit button
    submit_btn = Button(root, text='Добавить запись в справочник', command=submit)
    submit_btn.grid(row=6, column=1, columnspan=1, pady=(10,5), padx=60, sticky=W+E)

    # Create s Query button
    query_btn = Button(root, text='Показать список тем', command=query)
    query_btn.grid(row=7, column=1, columnspan=1, pady=(5,10), padx=60, sticky=W+E)

    # Create a Delete button
    delete_btn = Button(root, text='Удалить запись\n(по названию темы)', command=delete)
    delete_btn.grid(row=10, column=1, pady=10, padx=10, sticky=E)

    # Create an Update button
    edit_btn = Button(root, text='Редактировать запись\n(по названию темы)', command=edit)
    edit_btn.grid(row=10, column=1, pady=10, padx=(80,10))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


    root.mainloop()


if __name__ == '__main__':
    database()