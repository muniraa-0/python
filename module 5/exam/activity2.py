class book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.is_borrowed = False
    
    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            print(f"'{self.title}' has been borrowed")
        else:
            print(f"sorry,'{self.title}' is already borrowed.")
    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            print(f"'{self.title}' has been returned.")
        else:
            print(f"'{self.title}' was not borrowed.")

book1 = book("The great Gatsby","F. Scott Fitzgelard.")
book2 = book("1984", "George Orwell")
book3 = book("To kill a mockingbird", "Harper Lee")

print("--- Library System Demo ---")
book1.borrow()
book2.borrow()
book3.borrow()

print("\nReturning a book:")
book1.return_book()

print("\nTrying to borrow an already borrowed book:")
book2.borrow()

print("\nReturning all books:")
book2.return_book()
book3.return_book()

print("\nTrying to return a book That's not borrowed:")
book1.return_book()
