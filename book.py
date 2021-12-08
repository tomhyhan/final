from sqlalchemy import Column, Integer, Float, String, DateTime
from base import Base

import datetime

class Book(Base):
    """ Book Class """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    title = Column(String(250))
    author = Column(String(250))
    rating = Column(Integer())
    price = Column(Float())

    def __init__(self, title, author, rating, price):
        """ Creates a new Package record """

        self.title = title
        self.author = author
        self.rating = rating
        self.price = price

    def to_dict(self):
        """ Converts the Package record to a Python dictionary """

        new_dict = { "id" : self.id,
                     "timestamp": self.timestamp.strftime("%Y-%m-%d"),
                     "title" : self.title,
                     "author" : self.author,
                     "rating" : self.rating,
                     "price" : self.price }

        return new_dict
