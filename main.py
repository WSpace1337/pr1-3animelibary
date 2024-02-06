import sqlite3 as sq
import tkinter as tk 
from tkinter import ttk, messagebox
import webbrowser

#create database for anime libary  
class DB:
    def __init__(self):
        self.conn = sq.connect('anime.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS anime(
            id integer primary key AUTOINCREMENT,
            name TEXT,
            studio TEXT,
            genre TEXT,
            year INT,
            rating FLOAT
            );''')
        self.conn.commit()
    
    def insert_data(self, name, studio,genre, year,rating):
        self.c.execute('''INSERT INTO anime(name, studio,genre,year,rating) values(?,?,?,?,?)''', (name,genre,studio,year,rating))
        self.conn.commit()

 
#GUI

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        print('Привет, пупсик <3')
    
    def init_main(self):
        toolbar  = tk.Frame(bg = '#edffff', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)

        #кнопошки
        btn_open_dialog = tk.Button(toolbar, text = 'Добавить аниме',command = self.open_dialog,bg = '#f2ffff', bd = 0, compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)
        
        btn_edit_dialog = tk.Button(toolbar, text = 'Редактировать',bg = '#f2ffff', bd = 0, compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side = tk.LEFT)

        btn_delete = tk.Button(toolbar, text = 'Удалить',bg = '#f2ffff', bd = 0, compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side = tk.LEFT)
        
        btn_search = tk.Button(toolbar, text = 'Поиск',bg = '#f2ffff', bd = 0, compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side = tk.LEFT)

        btn_rat = tk.Button(toolbar, text='Смена рейтинга', bg ='#f2ffff', bd = 0, compound=tk.TOP, command=self.open_update_rating)
        btn_rat.pack(side = tk.LEFT)

        btn_refrash = tk.Button(toolbar, text = 'Обновить',  bg = '#f2ffff', bd = 0, compound= tk.TOP, command=self.view_records)
        btn_refrash.pack(side = tk.RIGHT)

        #САМАЯ КРУТАЯ КНОПКА ИЗ ВСЕХ 
        btn_dont_press = tk.Button(text='НЕ НАЖИМАЙ НА НЕЕ!!!!!!', bg = '#f2ffff', bd = 0.5, command=self.dont_press)
        btn_dont_press.place(x = 20,y = 355)

        # так же крутая кнопка
        btn_donate = tk.Button(text = 'DONATE ON COFE', bg = '#f2ffff', bd = 0.5, command=self.donate)
        btn_donate.place(x = 525, y = 355)


        #Делаем отображение из базы данных 
        self.tree = ttk.Treeview(self, columns=('ID', 'name','studio', 'genre', 'year', 'rating'), height=15, show='headings')

        self.tree.column('ID', width = 15, anchor = tk.CENTER)
        self.tree.column('name', width = 300, anchor = tk.CENTER)
        self.tree.column('studio', width = 75, anchor = tk.CENTER)
        self.tree.column('genre', width = 80, anchor = tk.CENTER)
        self.tree.column('year', width = 75, anchor = tk.CENTER) 
        self.tree.column('rating', width = 75, anchor = tk.CENTER)

        self.tree.heading('ID', text = 'ID') 
        self.tree.heading('name', text = 'Название') 
        self.tree.heading('studio', text = 'Студия') 
        self.tree.heading('genre', text = 'Жанр') 
        self.tree.heading('year', text = 'Год выпуска') 
        self.tree.heading('rating', text = 'Рейтинг') 

        self.tree.pack(side= tk.LEFT)

        #scrollbar
        
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.tree.configure(yscrollcommand = scroll.set)
        
    def records(self, name, studio,genre, year,rating):
        self.db.insert_data(name,studio,genre,year,rating)
        self.view_records()
    
    def update_record(self, name, studio, genre, year, rating):
        self.db.c.execute('''UPDATE anime SET name=?, studio=?, genre=?, year=?, rating=? WHERE ID=?''', (name, genre,studio,year,rating, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()
    
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM anime WHERE ID=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()
    
    def search_record(self,name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM anime  WHERE name  LIKE ?''', name)
        [self.tree.delete(i)for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
        
        #Если записей после поиска нету, то мы выводим сообщение об отсутсвие записи, и показываем всю базу данных. Костыль зато работает!
        if len(self.tree.get_children()) < 1:
            messagebox.showinfo(title='Ну и ну!', message='Похоже то чего вы ищите еще нету в базе данных.')
            self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM anime''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values = row) for row in self.db.c.fetchall()]
    
    def update_rating(self, rating):
        #Делаем проверку на то что рейтинг не больше 5(так как 5 это максимальное значение)
        if rating == '1337':
            messagebox.showinfo(title='Настрадамус предсказал это!', message='''Never gonna give you up 
                                \nNever gonna let you down 
                                \nNever gonna run around and desert you 
                                \nNever gonna make you cry 
                                \nNever gonna say goodbye 
                                \nNever gonna tell a lie and hurt you 
                                \n<3 <3 <3 <3 <3 <3 <3 ''')
            rating = '5'
            self.db.c.execute('''UPDATE anime set rating=? WHERE ID=?''', (rating,self.tree.set(self.tree.selection()[0], '#1'),))
            self.db.conn.commit()
        elif rating > '5':
            messagebox.showerror(title='Ошибка!', message='Вы ввели значения рейтинга больше 5.0. Повторите ввод правильно')
        else:
            self.db.c.execute('''UPDATE anime set rating=? WHERE ID=?''', (rating,self.tree.set(self.tree.selection()[0], '#1'),))
            self.db.conn.commit()
        self.view_records()
    
    def donate(self):
        webbrowser.open_new_tab('https://send.monobank.ua/jar/WAi2sfkdT')

    def dont_press(self):
        webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


    def open_search_dialog(self):
        Search()

    def open_dialog(self):
        Child()
    
    def open_update_dialog(self):
        Update()
    
    def open_update_rating(self):
        UpdateRating()

# вызывает дочернее окно для поиска информации в базе данных 

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск аниме по названию')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        self.label_search =  tk.Label(self, text='Поиск')
        self.label_search.place(x = 50, y = 20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 105, y = 20, width=150)

        #buttons dlya etogo
        btn_cancel = ttk.Button(self, text='Закрыть', command= self.destroy)
        btn_cancel.place(x = 185, y = 50)

        self.btn_search = ttk.Button(self, text='Поиск')
        self.btn_search.place(x = 105, y = 50)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_record(self.entry_search.get()))
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.grab_set()
        self.focus_set()

#Редактирует еще одно дочернее окно  по поиску информации в базе данных, на смену рейтинга
        
class UpdateRating(Search):
    def __init__(self):
        super().__init__()
        self.init_rating()
        self.view = app
    
    def init_rating(self):
        self.title('Сменить рейтинг')
        
        label_rating = tk.Label(self, text='Рейтинг:')
        label_rating.place(x = 50, y = 20)
        self.label_search.destroy()

        btn_edit_rat = ttk.Button(self, text='Сменить рейтинг')
        btn_edit_rat.place(x = 75, y =50)

        btn_edit_rat.bind('<Button-1>', lambda event: self.view.update_rating(self.entry_search.get()))
        btn_edit_rat.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.btn_search.destroy()

#открывает дочеренее окно для добавления записей
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добаить аниме')
        self.geometry('400x250+400+300')
        self.resizable(False, False)

        #названия полей
        label_name = tk.Label(self, text='Название')
        label_name.place(x = 125, y = 50)

        label_name = tk.Label(self, text='Жанр')
        label_name.place(x = 125, y = 75)
        
        label_name = tk.Label(self, text='Студия')
        label_name.place(x = 125, y = 100)

        label_name = tk.Label(self, text='Год')
        label_name.place(x = 125, y = 125)

        label_name = tk.Label(self, text='Рейтинг')
        label_name.place(x = 125, y = 150)
        
        #Поля ввода
        
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)

        self.entry_studio = ttk.Entry(self)
        self.entry_studio.place(x = 200, y = 75)

        self.entry_genre = ttk.Entry(self)
        self.entry_genre.place(x =  200, y = 100)

        self.combobox_year = ttk.Combobox(self, values = [ 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 
                                                          1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 
                                                          2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,2024])
        self.combobox_year.current(0)
        self.combobox_year.place(x = 200, y = 125)

        self.entry_rating = ttk.Entry(self)
        self.entry_rating.place(x = 200, y =150)
        
        #Кнопошки
        
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x = 300, y = 180)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x= 220, y = 180)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                   self.entry_studio.get(),
                                                                   self.entry_genre.get(), 
                                                                   self.combobox_year.get(), 
                                                                   self.entry_rating.get()))
        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.grab_set()
        self.focus_set()

#Обновляет дочернее окно для редактирования поля пры выделении
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_date()
    
    def init_edit(self):
        try:
            self.title('Редактировать позицию')

            btn_edit = ttk.Button(self, text = 'Редактировать')
            btn_edit.place(x = 200, y = 180)

            btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                            self.entry_studio.get(),
                                                                            self.entry_genre.get(),
                                                                            self.combobox_year.get(),
                                                                            self.entry_rating.get()))
            btn_edit.bind('<Button-1>', lambda event: self.destroy(), add="+")
            self.btn_add.destroy()
        except IndexError:
            messagebox.showerror(title='Произошла ошибка!', message='Выделите запись перед редактирование!')
            self.destroy()

    #поставляем те значения которые были, чтобы изменять точечно
    def default_date(self):
        try:
            self.db.c.execute('''SELECT * FROM  anime WHERE ID = ?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
            row = self.db.c.fetchone() #кортеж где (name,studio,genre,year,rating) нумерация с 1, так как row[0] это будет номер id
            self.entry_name.insert(0, row[1])
            self.entry_studio.insert(0, row[2])
            self.entry_genre.insert(0, row[3])
            year_value = [ 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 
                        1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 
                        2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,2024]
            self.combobox_year.current(year_value.index(row[4]))
            self.entry_rating.insert(0, row[5])
        except IndexError:
            messagebox.showerror(title='Произошла ошибка!', message='Выделите запись перед редактирование!')
            self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Anime")
    root.geometry("660x390+300+200")
    root.resizable(False, False)
    root.mainloop()
