import sqlite3

conn = sqlite3.connect('books.db')

conn.execute("DROP TABLE IF EXISTS books")

conn.execute("""
             CREATE TABLE books
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             author TEXT NOT NULL,
             title TEXT NOT NULL,
             UNIQUE(author, title))
             """)

conn.execute("INSERT INTO books (author, title)"
             "VALUES ('Jane Austen', 'Pride and Prejudice')")
conn.execute("INSERT INTO books (author, title)"
             "VALUES ('Arthur Conan Doyle', 'The Adventures of Sherlock Holmes')")
conn.execute("INSERT INTO books (author, title)"
             "VALUES ('James Joyce', 'Ulysses')")
conn.execute("INSERT INTO books (author, title)"
             "VALUES ('Miguel de Cervantes', 'Don Quixote')")
conn.commit()
conn.close()
