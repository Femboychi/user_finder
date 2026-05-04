import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.favorites = []
        self.load_favorites()

        # Создаём виджеты
        self.create_widgets()

    def create_widgets(self):
        # Поле поиска
        ttk.Label(self.root, text="Имя пользователя GitHub:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.search_entry = ttk.Entry(self.root, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка поиска
        ttk.Button(self.root, text="Найти", command=self.search_user).grid(row=0, column=2, padx=5, pady=5)

        # Результаты поиска
        ttk.Label(self.root, text="Результаты поиска:").grid(row=1, column=0, padx=5, pady=(10, 5), sticky='w')
        self.results_list = tk.Listbox(self.root, height=10, width=60)
        self.results_list.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

        # Кнопки управления избранным
        ttk.Button(self.root, text="Добавить в избранное", command=self.add_to_favorites).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self.root, text="Показать избранное", command=self.show_favorites).grid(row=3, column=1, padx=5, pady=10)

        # Список избранного
        ttk.Label(self.root, text="Избранное:").grid(row=4, column=0, padx=5, pady=(10, 5), sticky='w')
        self.favorites_list = tk.Listbox(self.root, height=8, width=60)
        self.favorites_list.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

        # Кнопки сохранения/загрузки
        ttk.Button(self.root, text="Сохранить избранное", command=self.save_favorites).grid(row=6, column=0, pady=10)
        ttk.Button(self.root, text="Загрузить избранное", command=self.load_favorites).grid(row=6, column=1, pady=10)

    def validate_input(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым.")
            return False
        return True

    def search_user(self):
        if not self.validate_input():
            return

        username = self.search_entry.get().strip()

        try:
            response = requests.get(f"https://api.github.com/users/{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_search_result(user_data)
            elif response.status_code == 404:
                messagebox.showwarning("Предупреждение", f"Пользователь '{username}' не найден.")
            else:
                messagebox.showerror("Ошибка", f"Ошибка API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Проблема с подключением: {e}")

    def display_search_result(self, user_data):
        self.results_list.delete(0, tk.END)
        display_text = f"{user_data['login']} | {user_data.get('name', 'N/A')} | {user_data.get('company', 'N/A')}"
        self.results_list.insert(tk.END, display_text)

    def add_to_favorites(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из результатов поиска.")
            return

        user_info = self.results_list.get(selection[0])
        if user_info not in self.favorites:
            self.favorites.append(user_info)
            self.update_favorites_display()
            messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")
        else:
            messagebox.showinfo("Информация", "Пользователь уже в избранном.")

    def show_favorites(self):
        self.update_favorites_display()

    def update_favorites_display(self):
        self.favorites_list.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_list.insert(tk.END, user)

    def save_favorites(self):
        with open('favorites.json', 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Избранное сохранено в favorites.json")

    def load_favorites(self):
        try:
            with open('favorites.json', 'r', encoding='utf-8') as f:
                self.favorites = json.load(f)
            self.update_favorites_display()
            messagebox.showinfo("Успех", "Избранное загружено из favorites.json")
        except FileNotFoundError:
            messagebox.showinfo("Информация", "Файл избранного не найден. Будет создан новый.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
