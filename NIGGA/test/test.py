import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import platform
import psutil
import threading
import time

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
                    response = os.system("ping -n 1 " + ip) if platform.system() == "Windows" else os.system("ping -c 1 " + ip)
                    status = "Онлайн" if response == 0 else "Оффлайн"
                    
                    # Получаем статистику (для локального хоста)
                    if ip == "127.0.0.1":
                        cpu = psutil.cpu_percent()
                        ram = psutil.virtual_memory().percent
                    else:
                        cpu = 0
                        ram = 0
                        
                    self.devices[ip]["status"] = status
                    self.devices[ip]["cpu"] = cpu
                    self.devices[ip]["ram"] = ram
                    
                    self.devices_tree.item(self.devices_tree.item(ip), values=(ip, status, f"{cpu}%", f"{ram}%"))
                except:
                    self.devices[ip]["status"] = "Ошибка"
                    self.devices_tree.item(self.devices_tree.item(ip), values=(ip, "Ошибка", "0%", "0%"))
                    
            time.sleep(5)  # Обновляем статистику каждые 5 секунд

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceMonitorApp(root)
    root.mainloop()