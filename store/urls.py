from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('publishers/', views.PublishersView.as_view(), name='publishers'),
    path('publishers/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('stores/', views.StoresView.as_view(), name='stores'),
    path('stores/<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    path('reminder/', views.create_reminder, name='create_reminder'),

]
