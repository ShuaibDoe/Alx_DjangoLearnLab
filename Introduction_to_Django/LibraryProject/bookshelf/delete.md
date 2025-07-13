from bookshelf.models import Book instance = Book.objects.create(id=1,title='1984',author='George Orwell',publication_year= '1949') book = Book.objects.get(id=1) book.delete()
