import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []
        self.load_data()

        # Создаём виджеты
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = ttk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(self.root, variable=self.precip_var).grid(row=3, column=1, sticky='w', padx=5)

        # Кнопка добавления
        ttk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=('Date', 'Temp', 'Desc', 'Precip'), show='headings')
        self.tree.heading('Date', text='Дата')
        self.tree.heading('Temp', text='Температура')
        self.tree.heading('Desc', text='Описание')
        self.tree.heading('Precip', text='Осадки')
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Фильтры
        ttk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_entry = ttk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Фильтр по температуре (>):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp_entry = ttk.Entry(self.root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        ttk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=10, column=0, pady=10)
        ttk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=10, column=1, pady=10)

    def validate_input(self):
        try:
            date = datetime.strptime(self.date_entry.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        try:
            temp = float(self.temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return False

        if not self.desc_entry.get():
            messagebox.showerror("Ошибка", "Описание не может быть пустым.")
            return False

        return True

    def add_record(self):
        if not self.validate_input():
            return

        record = {
            'date': self.date_entry.get(),
            'temperature': float(self.temp_entry.get()),
            'description': self.desc_entry.get(),
            'precipitation': self.precip_var.get()
        }
        self.records.append(record)
        self.update_table()
        self.clear_entries()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in self.records:
            self.tree.insert('', 'end', values=(
                record['date'],
                f"{record['temperature']}°C",
                record['description'],
                "Да" if record['precipitation'] else "Нет"
            ))

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def save_data(self):
        with open('weather_records.json', 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в weather_records.json")

    def load_data(self):
        try:
            with open('weather_records.json', 'r', encoding='utf-8') as f:
                self.records = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Данные загружены из weather_records.json")
        except FileNotFoundError:
            self.records = []

    def apply_filters(self):
        filtered = self.records
        date_filter = self.filter_date_entry.get()
        temp_filter = self.filter_temp_entry.get()

        if date_filter:
            filtered = [r for r in filtered if r['date'] == date_filter]
        if temp_filter:
            try:
                temp_val = float(temp_filter)
                filtered = [r for r in filtered if r['temperature'] > temp_val]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура для фильтра должна быть числом.")
                return

        self.update_filtered_table(filtered)

    def reset_filters(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()

    def update_filtered_table(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in records:
            self.tree.insert('', 'end', values=(
                record['date'],
                f"{record['temperature']}°C",
                record['description'],
                "Да" if record['precipitation'] else "Нет"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
