import pyodbc

# Налаштування підключення до бази даних
server = 'DESKTOP-QQAOEK4'
database = 'BooksDB'

def get_connection():
    """Функція для отримання підключення до бази даних."""
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
        f'Encrypt=yes;'
        f'TrustServerCertificate=yes;'
    )

def add_book_to_db(title, author, genre, year, rating):
    if not title or not author or not genre or not year or not rating:
        print("Помилка: всі поля повинні бути заповнені!")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                print(f"Виконання запиту: INSERT INTO Books (Title, Author, Genre, Year, Rating) VALUES ('{title}', '{author}', '{genre}', {year}, {rating})")
                cursor.execute("""
                    INSERT INTO Books (Title, Author, Genre, Year, Rating)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, author, genre, year, rating))
                conn.commit()
                print(f"Книга '{title}' додана до бази даних.")
    except pyodbc.Error as e:
        print(f"Помилка при додаванні книги: {e}")
    except Exception as e:
        print(f"Невідома помилка: {e}")

# Функція для отримання рекомендацій з бази даних
def get_recommendations_from_db(genre, min_rating=None):
    try:
        with get_connection() as conn:  # Використовуємо контекстний менеджер для підключення
            with conn.cursor() as cursor:
                query = "SELECT Title, Author, Genre, Year, Rating FROM Books WHERE Genre = ?"
                params = [genre]

                if min_rating is not None:
                    query += " AND Rating >= ?"
                    params.append(min_rating)

                cursor.execute(query, params)
                books = cursor.fetchall()

                return books
    except pyodbc.Error as e:
        print(f"Помилка при отриманні рекомендацій: {e}")
        return []
    except Exception as e:
        print(f"Невідома помилка: {e}")
        return []

# Функція для отримання всіх книг з бази даних
def get_all_books_from_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT Title, Author, Genre, Year, Rating FROM Books")
                books = cursor.fetchall()
                return books
    except pyodbc.Error as e:
        print(f"Помилка при отриманні всіх книг: {e}")
        return []
    except Exception as e:
        print(f"Невідома помилка: {e}")
        return []

# Функція для оновлення інформації про книгу
def update_book_in_db(book_id, title=None, author=None, genre=None, year=None, rating=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE Books SET "
                params = []
                if title:
                    query += "Title = ?, "
                    params.append(title)
                if author:
                    query += "Author = ?, "
                    params.append(author)
                if genre:
                    query += "Genre = ?, "
                    params.append(genre)
                if year:
                    query += "Year = ?, "
                    params.append(year)
                if rating:
                    query += "Rating = ?, "
                    params.append(rating)

                query = query.rstrip(', ')  # Видаляємо зайву кому в кінці
                query += " WHERE BookID = ?"
                params.append(book_id)

                cursor.execute(query, params)
                conn.commit()
                print(f"Книга з ID {book_id} оновлена.")
    except pyodbc.Error as e:
        print(f"Помилка при оновленні книги: {e}")
    except Exception as e:
        print(f"Невідома помилка: {e}")

def delete_book_from_db(book_id):
    try:
        # Создаем соединение с базой данных
        conn = get_connection()  # Функция для подключения к базе данных
        cursor = conn.cursor()
        
        # Выполняем запрос на удаление книги по ID
        cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))
        conn.commit()  # Подтверждаем изменения
        
        # Проверка, что книга была удалена
        if cursor.rowcount == 0:
            raise ValueError("Книга с таким ID не найдена.")
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Ошибка при удалении книги: {e}")
    