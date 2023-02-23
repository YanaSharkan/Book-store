from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def get_absolute_url(self):
        return '/store/author/%i/' % self.id

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def display_authors(self):
        """
        Creates a string for the Authors.
        """
        return ', '.join([author.name for author in self.authors.all()[:]])

    display_authors.short_description = 'Author'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def display_books(self):
        """
        Creates a string for the Books.
        """
        return ', '.join([book.name for book in self.books.all()[:7]])

    display_books.short_description = 'Book'
