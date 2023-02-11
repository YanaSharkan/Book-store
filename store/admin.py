from django.contrib import admin

from .models import Author, Publisher, Book, Store


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name', 'pages', 'price', 'rating', 'display_authors', 'publisher', 'pubdate')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name', 'display_books')
