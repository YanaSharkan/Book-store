from django.contrib import admin

from .models import Author, Book, Publisher, Store


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ('name',)


class BookInline(admin.TabularInline):
    model = Book
    fields = ('name', 'pages', 'price', 'rating', 'pubdate')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pages', 'price', 'rating', 'display_authors', 'publisher', 'pubdate')
    date_hierarchy = 'pubdate'
    list_filter = ('publisher__name', 'rating')
    filter_vertical = ('authors',)
    search_fields = ('name',)

    fieldsets = (
        ('Book', {
            'fields': ('name', 'price', 'pages', 'rating')
        }),
        ('Publish Info', {
            'fields': ('authors', 'publisher', 'pubdate')
        }),
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_books')
    filter_vertical = ['books']
    search_fields = ('name',)
