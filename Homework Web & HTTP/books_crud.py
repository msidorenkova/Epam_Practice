import sqlite3

from flask import Flask, jsonify, request, g
from werkzeug.exceptions import abort

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect("books.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return 'books'

@app.route('/api/books/', methods=['GET'])
def books():
    all_books = g.db.execute("SELECT * FROM books").fetchall()
    return jsonify(all_books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    one_book = g.db.execute(f"SELECT * FROM books WHERE id={book_id}").fetchone()
    return jsonify(one_book)

@app.route('/api/books/', methods=['POST'])
def add_book():
    if 'author' in request.json and 'title' in request.json:
        g.db.execute(f"INSERT INTO books (author, title) VALUES ({request.json['author']}, {request.json['title']})")
        g.db.commit()
        new_book = g.db.execute(f"SELECT * FROM books WHERE author={request.json['author']} and title={request.json['title']}").fetchone()
        return jsonify(new_book), 201

    abort(400)

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def edit_order(book_id):
    if 'author' in request.json and 'title' in request.json:
        g.db.execute(f"UPDATE books SET author={request.json['author']}, title={request.json['title']} WHERE id={book_id}")
        g.db.commit()
        upd_book = g.db.execute(f"SELECT * FROM books WHERE id={book_id}").fetchone()
        return jsonify(upd_book), 201

    abort(400)


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    g.db.execute(f"DELETE FROM books WHERE id={book_id}")
    g.db.commit()
    return 'None', 204

if __name__ == '__main__':
    app.run()
