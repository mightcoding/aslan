import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog

def create_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS wishes (
            user TEXT NOT NULL,
            wish TEXT NOT NULL,
            FOREIGN KEY (user) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    db_password = c.fetchone()
    conn.close()
    return db_password and db_password[0] == password

def add_wish(user, wish_text):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('INSERT INTO wishes (user, wish) VALUES (?, ?)', (user, wish_text))
    conn.commit()
    conn.close()

def get_wishes(user):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT wish FROM wishes WHERE user = ?', (user,))
    wishes = c.fetchall()
    conn.close()
    return wishes

def init_gui():
    app = Tk()
    app.title('Приложение пожеланий')

    def login_or_register():
        login_window = Toplevel(app)
        login_window.title("Вход / Регистрация")
        username_var = StringVar()
        password_var = StringVar()
        Label(login_window, text="Имя пользователя:").pack()
        Entry(login_window, textvariable=username_var).pack()
        Label(login_window, text="Пароль:").pack()
        Entry(login_window, textvariable=password_var, show='*').pack()
        Button(login_window, text="Войти", command=lambda: perform_login(username_var.get(), password_var.get(), login_window)).pack(side=LEFT)
        Button(login_window, text="Регистрация", command=lambda: perform_register(username_var.get(), password_var.get(), login_window)).pack(side=RIGHT)

    def main_menu(user):
        menu_window = Toplevel(app)
        menu_window.title("Главное меню")
        Label(menu_window, text="Список друзей: Пусто").pack()
        Button(menu_window, text="Создать новое пожелание", command=lambda: create_wish(user)).pack()
        Button(menu_window, text="Посмотреть желания", command=lambda: view_wishes(user)).pack()
        Button(menu_window, text="Выйти", command=menu_window.destroy).pack()

    def create_wish(user):
        wish_window = Toplevel(app)
        wish_window.title("Новое пожелание")
        wish_text = Text(wish_window, height=5, width=50)
        wish_text.pack()
        Button(wish_window, text="Сохранить", command=lambda: save_wish(user, wish_text.get("1.0", END), wish_window)).pack()
        Button(wish_window, text="Назад", command=wish_window.destroy).pack()

    def view_wishes(user):
        wishes_window = Toplevel(app)
        wishes_window.title("Ваши пожелания")
        wishes = get_wishes(user)
        for wish in wishes:
            Label(wishes_window, text=wish[0]).pack()
        Button(wishes_window, text="Назад", command=wishes_window.destroy).pack()

    def perform_login(username, password, window):
        if check_user(username, password):
            messagebox.showinfo("Успех", "Вы успешно вошли в систему!")
            window.destroy()
            main_menu(username)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def perform_register(username, password, window):
        if register_user(username, password):
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            window.destroy()
            main_menu(username)
        else:
            messagebox.showerror("Ошибка", "Такой пользователь уже существует.")

    def save_wish(user, wish_text, window):
        if wish_text.strip():
            add_wish(user, wish_text.strip())
            messagebox.showinfo("Успех", "Пожелание сохранено!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожелание не может быть пустым.")

    login_or_register()
    app.mainloop()

create_db()
init_gui()
