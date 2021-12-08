from book import Book

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BookManager:
    """ Manager of books in a bookstore """

    def __init__(self, db_name):

        if db_name is None or db_name == "":
            raise ValueError("DB Name cannot be undefined")

        engine = create_engine("sqlite:///" + db_name)
        self._db_session = sessionmaker(bind=engine)

    def add_book(self, title, author, rating, price):
        """ Adds a single book """

        # TODO - need validation
        if title is None or title == "":
            raise ValueError("Title must be defined and valid")

        if author is None or author == "":
            raise ValueError("Author must be defined and valid")

        if rating is None or type(rating) != int:
            raise ValueError("Rating must be defined and valid")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if price is None or type(price) != float:
            raise ValueError("Price must be defined and valid")

        if price < 0.0:
            raise ValueError("Price must be a positive value")

        session = self._db_session()

        book = Book(title, author, rating, price)

        session.add(book)
        session.commit()

        session.close()

    def delete_book(self, id):
        """ Deletes a single book based on the id """

        # TODO - need validation
        if id is None or type(id) != int or id < 0:
            raise ValueError("ID must be a positive integer")

        session = self._db_session()

        book = session.query(Book).filter(Book.id == id).first()

        if book is None:
            session.close()
            raise ValueError("Book does not exist")

        session.delete(book)
        session.commit()

        session.close()


    def get_all_books(self):
        """ Returns a list of all books """

        session = self._db_session()

        books = session.query(Book).all()

        session.close()

        return books
