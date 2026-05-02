class Book:
    def __init__(self, title="Python Basics", author="Ahmed", is_available=True):
        self.title = title
        self.author = author
        self.is_available = is_available

    def borrow_book(self):
        if self.is_available:
            self.is_available = False
            print(f"You borrowed '{self.title}'")
        else:
            print("The book is already out")


book1 = Book()
book1.borrow_book()
book1.borrow_book()