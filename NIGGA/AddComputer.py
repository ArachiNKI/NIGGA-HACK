import tkinter as tk
from tkinter import ttk
import socket
import requests

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Чёрная табличка сверху
        self.banner = tk.Label(
            self, 
            text="NIGGA HACK",
            bg="black",
            fg="white",
            font=("Arial", 14, "bold"),
            pady=5
        )
        self.banner.pack(fill=tk.X)

        # Настройка окна
        self.title("Связка устройств")
        self.geometry("400x350")

        # Создание меню
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Справка по использованию", command=self.help)
        menubar.add_cascade(label="Помощь", menu=file_menu)

        # Добавляем меню в окно
        self.config(menu=menubar)

        # Основной фрейм
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Кнопка для получения публичного IP
        self.public_ip_button = ttk.Button(
            self.main_frame,
            text="Получить публичный IP",
            command=self.show_public_ip)
        


        # Кнопка для связывания устройства
        self.bind_button = ttk.Button(
            self.main_frame,
            text="Связать это устройство",
            command=self.show_local_ip
        )
        self.bind_button.pack(pady=20)

        # Кнопка для связывания сети устройств
        self.network_bind_button = ttk.Button(
            self.main_frame,
            text="Связать сеть устройств",
            command=self.show_public_ip
        )
        self.network_bind_button.pack(pady=20)

        # Метка для отображения IP
        self.ip_label = ttk.Label(self.main_frame, text="")
        self.ip_label.pack(pady=10)

    def help(self):
        helpwindow = tk.Tk()
        helpwindow.geometry("700x385")
        helpwindow.title("Help")
        HelpText = tk.Label(helpwindow, text="""Здраствуй нигер, эта инструкция поможет тебе управлять чужим пк,
                             заражать роутеры и если мой прогресс поднимется то может отключать электричество в зданиях.
                             для связки устройства нужно запустить программу AddComputer.py когда запустится нажимай 
                            связать это устройство и запоминай IP адрес,
                             дальше запускай nigga.py -> добавить устройство -> вводи IP адрес. 
                            Для заражения роутеров надо нажимать 'Связать сеть устройств' и тоже запоминай IP
                            дальше переходи в nigga.py добавить сеть устройств и вставляй IP. Только слишком не вмешивайся в эту тему!
                            а то за такое можно и попасть на зону...""")
        HelpText.pack()

        


    def show_local_ip(self):
        # Получаем локальный IP адрес
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()

        self.ip_label.config(text=f"Локальный IP адрес: {ip}")

    def show_public_ip(self):
        try:
            # Получаем публичный IP адрес
            public_ip = requests.get('https://api.ipify.org').text

            # Создаем новое окно
            popup = tk.Toplevel(self)
            popup.title("Внешний IP адрес")
            popup.geometry("300x150")

            # Добавляем метку с IP
            label = ttk.Label(
                popup,
                text=f"Внешний IP адрес сети: {public_ip}",
                font=("Arial", 12)
            )
            label.pack(pady=30, padx=20)

            # Кнопка закрытия
            close_button = ttk.Button(
                popup,
                text="Закрыть",
                command=popup.destroy
            )
            close_button.pack(pady=10)

        except:
            self.ip_label.config(text="Не удалось получить внешний IP адрес")

if __name__ == "__main__":
    app = Application()
    app.mainloop()