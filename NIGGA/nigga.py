import os
import platform
import socket
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2 # для работы с камерой
import soundcard as sc # для работы со звуком
import psutil # для получения информации об устройствах



def check_devices():
    # Проверка веб-камеры
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            webcam_status = "Подключено"
        else:
            webcam_status = "Отключено"
    except:
        webcam_status = "Недоступно"
    
    # Проверка микрофона
    try:
        microphone_status = "Подключено" if sc.default_microphone() else "Отключено"
    except:
        microphone_status = "Недоступно"
    
    # Проверка динамиков
    try:
        speakers_status = "Подключено" if sc.default_speaker() else "Отключено"
    except:
        speakers_status = "Недоступно"
    
    # Проверка экрана
    try:
        screen_status = "Доступно" if psutil.cpu_count() > 0 else "Отключено"
    except:
        screen_status = "Недоступно"
    
    return {
        "Веб-камера": webcam_status,
        "Микрофон": microphone_status,
        "Динамики": speakers_status,
        "Экран": screen_status
    }

def demonstration_screen():
    devices = check_devices()
    
    # Создаем новое окно для списка устройств
    devices_window = tk.Toplevel(window)
    devices_window.title("Список устройств")
    devices_window.geometry("300x200")
    
    # Создаем список устройств
    devices_label = ttk.Label(devices_window, text="NIGGA HACK")
    devices_list = ttk.Treeview(devices_window, height=5)
    devices_list["columns"] = ("name", "status")
    devices_list.column("#0", width=10)
    devices_list.column("name", width=150)
    devices_list.column("status", width=100)
    devices_list.heading("name", text="Устройство")
    devices_list.heading("status", text="Статус")
    
    # Заполняем список реальными устройствами
    for i, (device, status) in enumerate(devices.items()):
        devices_list.insert("", "end", text=str(i+1), values=(device, status))
    
    # Размещаем элементы
    devices_label.pack(pady=10)
    devices_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

def add_device():
    class DeviceMonitorApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Мониторинг устройств")
        
            # Создаем элементы интерфейса
            self.ip_entry = ttk.Entry(root, width=20)
            self.ip_entry.pack(pady=10)
        
            self.add_button = ttk.Button(root, text="Добавить устройство", command=self.add_device)
            self.add_button.pack(pady=5)
        
            self.devices_tree = ttk.Treeview(root, columns=("IP", "Статус", "Загрузка CPU", "Загрузка RAM"), show="headings")
            self.devices_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
            self.devices_tree.heading("IP", text="IP адрес")
            self.devices_tree.heading("Статус", text="Статус")
            self.devices_tree.heading("Загрузка CPU", text="Загрузка CPU")
            self.devices_tree.heading("Загрузка RAM", text="Загрузка RAM")
        
            self.devices = {}  # Словарь для хранения информации об устройствах
        
            # Запускаем поток для обновления статистики
            self.update_thread = threading.Thread(target=self.update_stats)
            self.update_thread.daemon = True
            self.update_thread.start()

        def add_device(self):
            ip = self.ip_entry.get()
            try:
                socket.inet_aton(ip)  # Проверяем валидность IP
                if ip not in self.devices:
                    self.devices[ip] = {"status": "Проверка...", "cpu": 0, "ram": 0}
                    self.devices_tree.insert("", "end", values=(ip, "Проверка...", "0%", "0%"))
                    self.ip_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Предупреждение", "Устройство уже добавлено")
            except socket.error:
                messagebox.showerror("Ошибка", "Неверный формат IP-адреса")

        def update_stats(self):
            while True:
                for ip in list(self.devices.keys()):
                    try:
                    # Проверяем доступность устройства
                        response = subprocess.call(f"ping -n 1 {ip}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        status = "Онлайн" if response == 0 else "Оффлайн"
                
                # Получаем статистику (для локального хоста)
                        if ip == "127.0.0.1":
                            cpu = psutil.cpu_percent()
                            ram = psutil.virtual_memory().percent
                        else:
                            cpu = 0
                            ram = 0
                
                        self.devices["status"] = status
                        self.devices["cpu"] = cpu
                        self.devices["ram"] = ram
                
                # Получаем идентификатор строки по IP
                        item_id = self.devices_tree.item(ip)
                        if item_id:
                            self.devices_tree.item(item_id, values=(ip, status, f"{cpu}%", f"{ram}%"))
                
                    except Exception as e:
                        self.devices["status"] = "Ошибка"
                        # Получаем идентификатор строки по IP
                        item_id = self.devices_tree.item(ip)
                        if item_id:
                            self.devices_tree.item(item_id, values=(ip, "Ошибка", "0%", "0%"))
                
                    time.sleep(5) # Обновляем статистику каждые 5 секунд

    if __name__ == "__main__":
        root = tk.Tk()
        app = DeviceMonitorApp(root)
        root.mainloop()

# Создаем главное окно
window = tk.Tk()
window.title("Управление системой")
window.geometry("400x500")  # Увеличили высоту окна
window.resizable(False, False)
BGMENU = tk.Label(window, background="black")
BGMENU.pack(fill=tk.BOTH, expand=True)
# Добавляем текст
text_label = tk.Label(
    BGMENU, 
    text="NIGGA HACK", 
    foreground="white",  # Цвет текста
    background="black",  # Цвет фона
    font=("Arial", 24, "bold")  # Шрифт, размер и стиль
)

# Размещаем текст по центру
text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Создаем рамку для кнопок
frame = ttk.Frame(window, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# Создаем кнопки
btn_demonstration = ttk.Button(frame, text="Состояние вашего устройства", command=demonstration_screen)


# Размещаем кнопки вертикально с отступами
btn_demonstration.pack(pady=10)
# Функция для настройки устройств
def configure_devices():
    settingswin = tk.Tk()
    settingswin.title("Settings")
    settingswin.geometry("1200x1150")

# Кнопка настройки устройств
btn_configure = ttk.Button(frame, text="Настроить устройства", command=configure_devices)
btn_configure.pack(pady=10)
btn_AddPC = ttk.Button(frame, text="Добавить устройство", command=add_device)
btn_AddPC.pack(pady=10)

# Запускаем основной цикл
window.mainloop()