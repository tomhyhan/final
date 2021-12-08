from flask import Flask
from flask import request
from flask import Response

from book_manager import BookManager

import json

app = Flask(__name__)

DB_NAME = "bookstore.sqlite"


@app.route('/books/all', methods=['GET'])
def get_all_books():
    """ Gets all book records """

    book_mgr = BookManager(DB_NAME)
    books = book_mgr.get_all_books()

    book_list = []
    for book in books:
        book_list.append(book.to_dict())

    result = json.dumps(book_list)

    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json')

    return response

@app.route('/books', methods=['POST'])
def add_book():
    """ Adds a new book record """

    book_json = request.get_json()

    book_mgr = BookManager(DB_NAME)

    book_mgr.add_book(book_json['title'], book_json['author'], book_json['rating'], book_json['price'])

    response = app.response_class(status=200)

    return response



@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """ Deletes a book record """

    book_mgr = BookManager(DB_NAME)

    book_mgr.delete_book(id)

    response = app.response_class(status=200)

    return response


if __name__ == "__main__":
    app.run()
