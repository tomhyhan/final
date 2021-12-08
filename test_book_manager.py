from unittest import TestCase
import unittest

from book_manager import BookManager

import sqlite3
import os
import inspect

import xmlrunner


class TestBookManager(TestCase):
    """ Tests the BookManager class """

    TEST_DB = 'test_bookstore.sqlite'

    def setUp(self):
        """ Set up test environment """
        self.logPoint()

        conn = sqlite3.connect(TestBookManager.TEST_DB)

        c = conn.cursor()
        c.execute('''
                  CREATE TABLE books
                  (id INTEGER PRIMARY KEY ASC,
                   timestamp DATETIME NOT NULL,
                   title VARCHAR(250),
                   author VARCHAR(250),
                   rating INTEGER,
                   price REAL
                  )
                  ''')

        conn.commit()
        conn.close()

        self.book_mgr = BookManager(TestBookManager.TEST_DB)


    def tearDown(self):
        """ call log message for test"""
        self.logPoint()
        os.remove(TestBookManager.TEST_DB)

    def logPoint(self):
        """ Log out testing information """
        current_test = self.id().split('.')[-1]
        calling_function = inspect.stack()[1][3]
        print('in %s - %s()' % (current_test, calling_function))

    def test_add_book_success(self):
        """ TP-01 - Success test on add_book """

        books_before = self.book_mgr.get_all_books()
        self.assertEqual(len(books_before), 0)

        self.book_mgr.add_book("Title1", "Author1", 1, 9.99)
        self.book_mgr.add_book("Title2", "Author2", 5, 21.50)

        books_after = self.book_mgr.get_all_books()
        self.assertEqual(len(books_after), 2)

    def test_add_book_invalid(self):
        """ TP-02 - Validation test on add_book """

        with self.assertRaisesRegex(ValueError, "Title must be defined and valid"):
            self.book_mgr.add_book("", "Author1", 1, 9.99)

        with self.assertRaisesRegex(ValueError, "Author must be defined and valid"):
            self.book_mgr.add_book("Title1", "", 1, 9.99)

        with self.assertRaisesRegex(ValueError, "Rating must be defined and valid"):
            self.book_mgr.add_book("Title1", "Author1", "1", 9.99)

        with self.assertRaisesRegex(ValueError, "Price must be defined and valid"):
            self.book_mgr.add_book("Title1", "Author1", 1, "9.99")

        with self.assertRaisesRegex(ValueError, "Title must be defined and valid"):
            self.book_mgr.add_book(None, "Author1", 1, 9.99)

        with self.assertRaisesRegex(ValueError, "Author must be defined and valid"):
            self.book_mgr.add_book("Title1", None, 1, 9.99)

        with self.assertRaisesRegex(ValueError, "Rating must be defined and valid"):
            self.book_mgr.add_book("Title1", "Author1", None, 9.99)

        with self.assertRaisesRegex(ValueError, "Price must be defined and valid"):
            self.book_mgr.add_book("Title1", "Author1", 1, None)

        with self.assertRaisesRegex(ValueError, "Rating must be between 1 and 5"):
            self.book_mgr.add_book("Title1", "Author1", 0, 9.99)

        with self.assertRaisesRegex(ValueError, "Rating must be between 1 and 5"):
            self.book_mgr.add_book("Title1", "Author1", 6, 9.99)

        with self.assertRaisesRegex(ValueError, "Price must be a positive value"):
            self.book_mgr.add_book("Title1", "Author1", 3, -9.99)


    def test_delete_book_success(self):
        """ TP-04 - Success test on delete_book """

        books_before = self.book_mgr.get_all_books()
        self.assertEqual(len(books_before), 0)

        self.book_mgr.add_book("Title1", "Author1", 1, 9.99)
        self.book_mgr.add_book("Title1", "Author1", 3, 21.50)

        books_between = self.book_mgr.get_all_books()
        self.assertEqual(len(books_between), 2)

        for book in books_between:
            self.book_mgr.delete_book(book.id)

        books_after = self.book_mgr.get_all_books()
        self.assertEqual(len(books_after), 0)

    def test_delete_non_existent_book(self):
        """ TP-05 - Validation for non-existent book on delete_book """

        with self.assertRaisesRegex(ValueError, "Book does not exist"):
            self.book_mgr.delete_book(1000000)

    def test_delete_book_invalid(self):
        """ TP-06 - Validation test on delete_book """

        with self.assertRaisesRegex(ValueError, "ID must be a positive integer"):
            self.book_mgr.delete_book(None)

        with self.assertRaisesRegex(ValueError, "ID must be a positive integer"):
            self.book_mgr.delete_book("")

        with self.assertRaisesRegex(ValueError, "ID must be a positive integer"):
            self.book_mgr.delete_book(-100)

    def test_get_all_books_success(self):
        """ TP-07 - Success test on get_all_books """

        books_before = self.book_mgr.get_all_books()
        self.assertEqual(len(books_before), 0)

        self.book_mgr.add_book("Title1", "Author1", 1, 9.99)

        books_between = self.book_mgr.get_all_books()
        self.assertEqual(len(books_between), 1)

        self.book_mgr.add_book("Title2", "Author2", 3, 21.50)

        books_after = self.book_mgr.get_all_books()
        self.assertEqual(len(books_after), 2)
        
if __name__ == "__main__":
    runner = xmlrunner.XMLTestRunner(output='test-reports') 
    unittest.main(testRunner=runner) 
    unittest.main()


