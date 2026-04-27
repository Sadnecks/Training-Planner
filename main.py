import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'trainings.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title('Training Planner')
        self.trainings = []
        self.load_data()

        # Поля ввода
        ttk.Label(root, text='Дата (ГГГГ-ММ-ДД):').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text='Тип тренировки:').grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text='Длительность (мин):').grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(root, text='Добавить тренировку', command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры
        ttk.Label(root, text='Фильтр по типу:').grid(row=4, column=0, padx=5, pady=5)
        self.filter_type = ttk.Entry(root)
        self.filter_type.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(root, text='Фильтр по дате:').grid(row=5, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(root)
        self.filter_date.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(root, text='Применить фильтр', command=self.apply_filter).grid(row=6, column=0, columnspan=2, pady=5)

        # Таблица тренировок
        self.tree = ttk.Treeview(root, columns=('date', 'type', 'duration'), show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип')
        self.tree.heading('duration', text='Длительность')
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.update_table()

    def add_training(self):
        date = self.date_entry.get()
        type_ = self.type_entry.get()
        duration = self.duration_entry.get()

        if not date or not type_ or not duration:
            messagebox.showerror('Ошибка', 'Все поля обязательны!')
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
            duration = float(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Ошибка', 'Неверный формат даты или длительности!')
            return

        self.trainings.append({'date': date, 'type': type_, 'duration': duration})
        self.save_data()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for tr in self.trainings:
            self.tree.insert('', tk.END, values=(tr['date'], tr['type'], tr['duration']))

    def apply_filter(self):
        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        filtered = self.trainings
        if f_type:
            filtered = [tr for tr in filtered if f_type in tr['type'].lower()]
        if f_date:
            filtered = [tr for tr in filtered if tr['date'] == f_date]

        for i in self.tree.get_children():
            self.tree.delete(i)
        for tr in filtered:
            self.tree.insert('', tk.END, values=(tr['date'], tr['type'], tr['duration']))

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)

if __name__ == '__main__':
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
