import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database_connection import add_book_to_db, get_recommendations_from_db, update_book_in_db, delete_book_from_db

# Функція для додавання книги
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()

    if title and author and genre and year and rating:
        try:
            # Перевірка на числові значення року та рейтингу
            year = int(year)
            rating = float(rating)

            # Додаємо книгу до бази даних
            add_book_to_db(title, author, genre, year, rating)
            messagebox.showinfo("Успіх", "Книга додана до бази даних.")
            clear_add_book_fields()  # Очистити поля після успішного додавання
        except ValueError:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть коректні числа для року та рейтингу.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка: {e}")
    else:
        messagebox.showwarning("Увага", "Будь ласка, заповніть всі поля.")

# Функція для редагування книги
def edit_book():
    book_id = entry_book_id.get()
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()

    if book_id and title and author and genre and year and rating:
        try:
            # Перевірка на числові значення року та рейтингу
            year = int(year)
            rating = float(rating)

            # Оновлюємо книгу в базі даних
            update_book_in_db(book_id, title, author, genre, year, rating)
            messagebox.showinfo("Успіх", "Дані книги оновлено.")
            clear_add_book_fields()  # Очистити поля після успішного редагування
        except ValueError:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть коректні числа для року та рейтингу.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка: {e}")
    else:
        messagebox.showwarning("Увага", "Будь ласка, заповніть всі поля.")

# Функція для видалення книги
def delete_book():
    book_id = entry_book_id.get()

    if book_id:
        try:
            # Видаляємо книгу з бази даних
            delete_book_from_db(book_id)
            messagebox.showinfo("Успіх", f"Книга з ID {book_id} видалена з бази даних.")
            clear_add_book_fields()  # Очистити поля після видалення
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка: {e}")
    else:
        messagebox.showwarning("Увага", "Будь ласка, введіть ID книги для видалення.")

# Функція для очищення полів після додавання книги
def clear_add_book_fields():
    entry_book_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

# Функція для отримання рекомендацій
def recommend_books():
    genre = combo_genre.get()
    min_rating = entry_recommend_rating.get()

    try:
        if min_rating:
            min_rating = float(min_rating)
        else:
            min_rating = None

        # Отримуємо рекомендації з бази даних
        books = get_recommendations_from_db(genre, min_rating)
        result_text.delete(1.0, tk.END)  # Очистити текстову область перед виведенням нових рекомендацій

        if books:
            for book in books:
                result_text.insert(tk.END, f"{book.Title} by {book.Author} ({book.Year}) - Rating: {book.Rating}\n")
        else:
            result_text.insert(tk.END, "Немає рекомендацій за вашим запитом.\n")

    except ValueError:
        messagebox.showwarning("Помилка вводу", "Будь ласка, введіть коректний рейтинг.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

# Створення головного вікна
root = tk.Tk()
root.title("Програмний додаток для рекомендацій книг")
root.geometry("650x750")
root.config(bg="#e0f7fa")  # Задаємо колір фону головного вікна

# Стиль для віджетів
style = ttk.Style()
style.configure("TButton",
                font=("Arial", 12),
                padding=10,
                relief="flat",
                background="#4CAF50",  # Зелений колір кнопки
                foreground="red")  # Червоний текст на кнопці
style.map("TButton",
          background=[('active', '#388E3C')])  # Міняється колір при наведенні (темно-зелений)

# Введення даних для додавання книги
frame_add_book = tk.LabelFrame(root, text="Додати/Редагувати/Видалити книгу", padx=10, pady=10, bg="#e0f7fa", font=("Arial", 14))
frame_add_book.pack(padx=10, pady=10, fill="both")

tk.Label(frame_add_book, text="ID книги (для редагування/видалення):", bg="#e0f7fa", font=("Arial", 12)).grid(row=0, column=0)
entry_book_id = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_book_id.grid(row=0, column=1)

tk.Label(frame_add_book, text="Назва книги:", bg="#e0f7fa", font=("Arial", 12)).grid(row=1, column=0)
entry_title = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_title.grid(row=1, column=1)

tk.Label(frame_add_book, text="Автор:", bg="#e0f7fa", font=("Arial", 12)).grid(row=2, column=0)
entry_author = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_author.grid(row=2, column=1)

tk.Label(frame_add_book, text="Жанр:", bg="#e0f7fa", font=("Arial", 12)).grid(row=3, column=0)
entry_genre = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_genre.grid(row=3, column=1)

tk.Label(frame_add_book, text="Рік видання:", bg="#e0f7fa", font=("Arial", 12)).grid(row=4, column=0)
entry_year = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_year.grid(row=4, column=1)

tk.Label(frame_add_book, text="Рейтинг:", bg="#e0f7fa", font=("Arial", 12)).grid(row=5, column=0)
entry_rating = tk.Entry(frame_add_book, font=("Arial", 12), bg="#ffffff")
entry_rating.grid(row=5, column=1)

# Використовуємо ttk.Button для додавання, редагування та видалення
ttk.Button(frame_add_book, text="Додати книгу", command=add_book, style="TButton").grid(row=6, column=0, pady=10)
ttk.Button(frame_add_book, text="Редагувати книгу", command=edit_book, style="TButton").grid(row=6, column=1, pady=10)
ttk.Button(frame_add_book, text="Видалити книгу", command=delete_book, style="TButton").grid(row=7, columnspan=2, pady=10)

# Введення даних для отримання рекомендацій
frame_recommend = tk.LabelFrame(root, text="Рекомендації", padx=10, pady=10, bg="#e0f7fa", font=("Arial", 14))
frame_recommend.pack(padx=10, pady=10, fill="both")

tk.Label(frame_recommend, text="Жанр для рекомендацій:", bg="#e0f7fa", font=("Arial", 12)).grid(row=0, column=0)

# Додаємо ComboBox для вибору жанру
combo_genre = ttk.Combobox(frame_recommend, font=("Arial", 12), values=["Фантастика", "Історичний роман", "Роман", "Есеїстика", "Поезія", "Трилер", "Мемуари", "Комедія", "Драма", "Готичний роман", "Листи", "Історична повість"])  # Додайте список жанрів
combo_genre.grid(padx=10, pady=10, row=0, column=1)

tk.Label(frame_recommend, text="Мінімальний рейтинг:", bg="#e0f7fa", font=("Arial", 12)).grid(row=1, column=0)
entry_recommend_rating = tk.Entry(frame_recommend, font=("Arial", 12), bg="#ffffff")
entry_recommend_rating.grid(row=1, column=1)

# Додавання кнопки для отримання рекомендацій
ttk.Button(frame_recommend, text="Отримати рекомендації", command=recommend_books, style="TButton").grid(row=2, columnspan=2, pady=10)

# Місце для виведення результатів рекомендацій
result_text = tk.Text(root, height=10, width=50, font=("Arial", 12), bg="#ffffff", wrap=tk.WORD)
result_text.pack(padx=10, pady=10)

# Запуск основного циклу
root.mainloop()
