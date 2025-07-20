from relationship_app.models import Author, Book, Library, Librarian

library_name = "Central Library"  # example name
library = Library.objects.get(name=library_name)

# Example: list books in that library
books = library.books.all()
for book in books:
    print(book.title)
  
# Query all books by a specific author (e.g., "George Orwell")
orwell = Author.objects.get(name="George Orwell")
books_by_orwell = Book.objects.filter(author=orwell)
print("Books by George Orwell:", list(books_by_orwell))

# List all books in a specific library (e.g., "Central Library")
central_library = Library.objects.get(name="Central Library")
books_in_library = central_library.books.all()
print("Books in Central Library:", list(books_in_library))

# Retrieve the librarian for a specific library (e.g., "Central Library")
librarian = Librarian.objects.get(library=central_library)
print("Librarian of Central Library:", librarian.name)
