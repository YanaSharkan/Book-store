from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Avg, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from .forms import ReminderForm
from .models import Author, Book, Publisher, Store
from .tasks import send_reminder


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IndexView(generic.TemplateView):
    template_name = 'store/index.html'


class AuthorsView(generic.ListView):
    template_name = 'store/authors.html'
    context_object_name = 'entries_list'
    paginate_by = 5
    model = Author

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'store/author.html'


class PublishersView(generic.ListView):
    template_name = 'store/publishers.html'
    context_object_name = 'entries_list'

    def get_queryset(self):
        return Publisher.objects.all()


class PublisherDetailView(generic.DetailView):
    model = Publisher
    template_name = 'store/publisher.html'


class BooksView(generic.ListView):
    context_object_name = 'entries_list'
    template_name = 'store/books.html'
    paginate_by = 10
    model = Book

    def get_queryset(self):
        return Book.objects.prefetch_related('authors', 'publisher').annotate(Count('authors')).all()


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'store/book.html'


class StoresView(generic.ListView):
    context_object_name = 'entries_list'
    template_name = 'store/stores.html'

    def get_queryset(self):
        return Store.objects.prefetch_related('books').annotate(Count('books')).all()


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'store/store.html'

    def get_object(self):
        store = super(StoreDetailView, self).get_object()
        store.avg_book_price = store.books.all().aggregate(Avg('price'))['price__avg']
        return store


class AuthorCreateView(AdminRequiredMixin, CreateView):
    model = Author
    fields = ['name', 'age']


class AuthorUpdateView(AdminRequiredMixin, UpdateView):
    model = Author
    fields = ['name', 'age']
    template_name_suffix = '_update_form'


class AuthorDeleteView(AdminRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('store:authors')


def create_reminder(request):
    params = dict()
    params["form"] = ReminderForm()

    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            send_reminder.apply_async((form.cleaned_data['email'], form.cleaned_data['text']),
                                      eta=form.cleaned_data['date_time'])
            params["result"] = "Reminder scheduled"
        else:
            params["error"] = "Date not valid"

    return render(request, "store/reminder.html", params)
