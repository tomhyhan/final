import tkinter as tk
import requests
from tkinter import messagebox
import datetime
from add_book_popup import AddBookPopup


API_DELETE_ENDPOINT = "http://127.0.0.1:5000/books/"
API_ALL_ENDPOINT = "http://127.0.0.1:5000/books/all"


class BookstoreGui(tk.Frame):

    def __init__(self, master=None):
        """ Initializes the main frame """
        super().__init__(master)
        self.grid()
        self._create_widgets()

    def _create_widgets(self):
        """ Creates the main package management widgets """

        tk.Label(self, text="Books List").grid(row=1, column=1)
        self._books_listbox = tk.Listbox(self, width=100)
        self._books_listbox.grid(row=2, column=0, columnspan=3)
        self._books = []

        self._add = tk.Button(self, text="Add Book", command=self._add_book)
        self._add.grid(column=0, row=3)
        self._delete = tk.Button(self, text="Delete Book", command=self._delete_book)
        self._delete.grid(column=1, row=3)
        self._quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self._quit.grid(column=2, row=3)

        self._get_books()

    def _get_books(self):
        """ Gets all book records from the backend """
        resp = requests.get(API_ALL_ENDPOINT)

        if resp.status_code != 200:
            messagebox.showwarning("Warning", "Could not retrieve the books.")
            return

        self._books.clear()
        self._books_listbox.delete(0, tk.END)

        data = resp.json()
        for book in data:
            self._books.append(book)
            self._books_listbox.insert(tk.END, "Book %s, Author %s, Rating %d, Price %.2f (Added: %s)" % \
            (book["title"], book["author"], book["rating"], book["price"], book["timestamp"]))

    def _add_book(self):
        """ Add a book record to the backend """
		
        self._popup_win = tk.Toplevel()
        self._popup = AddBookPopup(self._popup_win, self._close_book_cb)

    def _close_book_cb(self):
        self._popup_win.destroy()
        self._get_books()

    def _delete_book(self):
        """ Deletes a book record from the backend """
        selection = self._books_listbox.curselection()

        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No book selected to delete.")
            return

        book = self._books[selection[0]]

        result = messagebox.askyesno("Delete", "Are you sure you want to delete the book?")
		
        if result:
            resp = requests.delete(API_DELETE_ENDPOINT + str(book["id"]))
            self._get_books()

root = tk.Tk()
app = BookstoreGui(master=root)
app.mainloop()
