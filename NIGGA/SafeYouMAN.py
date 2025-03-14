import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import ipaddress

class IPEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифрование IP-адресов")
        
        # Создаем ключ шифрования (в реальном приложении его нужно хранить безопасно)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # Создаем элементы интерфейса
        self.ip_entry = ttk.Entry(root, width=20)
        self.ip_entry.pack(pady=10)
        
        self.encrypt_button = ttk.Button(root, text="Зашифровать IP", command=self.encrypt_ip)
        self.encrypt_button.pack(pady=5)
        
        self.result_label = ttk.Label(root, text="Результат будет здесь")
        self.result_label.pack(pady=10)
        
    def encrypt_ip(self):
        try:
            # Получаем IP-адрес из поля ввода
            ip = self.ip_entry.get()
            ipaddress.ip_address(ip)  # Проверяем валидность IP
            
            # Шифруем IP
            encrypted_ip = self.cipher_suite.encrypt(ip.encode())
            
            # Показываем результат
            self.result_label.config(text=f"Зашифрованный IP: {encrypted_ip}")
            
        except ValueError:
            self.result_label.config(text="Ошибка: введите корректный IP-адрес")
        except Exception as e:
            self.result_label.config(text=f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x350")
    app = IPEncryptionApp(root)
    root.mainloop()