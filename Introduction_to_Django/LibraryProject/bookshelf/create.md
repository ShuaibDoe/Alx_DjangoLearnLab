instance = Book.objects.create(title='1984',author='George Orwell',publication_year='1949')

book = Book.objects.get()
