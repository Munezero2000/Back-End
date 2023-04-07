from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def db_connection():
    """
    a method that when called creates a connection to the database
    Returns:
        conn: an object for database connectivity
    """
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM BOOK")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        else:
            return "Something Went Wrong", 404

    if request.method == "POST":
        author = request.form["author"]
        title = request.form['title']
        language = request.form['language']
        sql = """INSERT INTO book (author, language, title) VALUES(?, ?, ?)"""
        cursor = cursor.execute(sql, (author, language, title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created Successful"


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM BOOK WHERE id =?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something went wrong", 404

    if request.method == 'PUT':
        author = request.form["author"]
        title = request.form['title']
        language = request.form['language']
        cursor.execute("""
        UPDATE BOOK SET 
        author=?,
        language=?,
        title=?
        WHERE
        id=?
        """, (author, language, title, id))
        conn.commit()
        updated_book = {
            'id': id,
            'author': author,
            'language': language,
            'title': title}
        return jsonify(updated_book)

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM BOOK WHERE id=?", (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200


if __name__ == '__main__':
    app.run(debug=True)
