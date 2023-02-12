from django.core.management.base import BaseCommand

from faker import Faker

from ...models import Author, Book, Publisher, Store


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('book_count', type=int, choices=range(1, 101))

    def handle(self, *args, **options):
        fake = Faker()
        book_count = options['book_count']
        publisher_record = Publisher.objects.create(name=fake.name())
        author_record_1 = Author.objects.create(name=fake.name(), age=fake.random.randint(18, 100))
        author_record_2 = Author.objects.create(name=fake.name(), age=fake.random.randint(18, 100))

        books_params = [{'name': fake.company(),
                         'pages': fake.random.randint(100, 1000),
                         'price': fake.random.randint(10, 100),
                         'rating': fake.random.randint(2, 5),
                         'publisher': publisher_record,
                         'pubdate': fake.date_time()} for _ in range(book_count)]
        books_records = []
        for book_param in books_params:
            book_record = Book.objects.create(**book_param)
            book_record.authors.set([author_record_1, author_record_2])
            books_records.append(book_record)
            # 'authors': [author_record_1, author_record_2],

        # books_records = Book.objects.bulk_create([Book(**values) for values in books_params])
        store_record = Store.objects.create(name=fake.company())
        store_record.books.set(books_records)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created books {} for store {}'.format(len(books_records), store_record.name)
        ))
