from django.core.management.base import BaseCommand
from tracker.models import Author, Book, Genre
from django.contrib.auth.models import User
from faker import Faker
from random import randint, uniform, choice
from datetime import timedelta, datetime
from typing import List


class DatabaseCleaner:
    @staticmethod
    def clear() -> None:
        Book.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()


class UserFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def create_users(self, count: int) -> List[User]:
        users = []
        usernames = set()
        while len(users) < count:
            username = f"{self.faker.user_name()}{randint(1000, 9999)}"
            if username not in usernames:
                usernames.add(username)
                users.append(
                    User(
                        username=username,
                        email=self.faker.email(),
                        password="123.qaz",
                    )
                )
        return users


class AuthorFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def create_authors(self, count: int) -> List[Author]:
        return [Author(name=self.faker.name()) for _ in range(count)]


class GenreFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def create_genres(self, count: int) -> List[Genre]:
        return [Genre(name=self.faker.word()) for _ in range(count)]


class BookFactory:
    def __init__(self, faker: Faker, start_date: datetime) -> None:
        self.faker = faker
        self.start_date = start_date

    def _generate_dates(self, status: str) -> tuple[datetime, datetime | None]:
        start_date = self.start_date + timedelta(days=randint(0, 45000))
        end_date = (
            start_date + timedelta(days=randint(1, 365))
            if status == "Completed"
            else None
        )
        return start_date, end_date

    def create_books(
        self, authors: List[Author], genres: List[Genre], count: int
    ) -> List[Book]:
        books = []
        for _ in range(count):
            status = choice(["Not Started", "Reading", "Completed"])
            start_date, end_date = self._generate_dates(status)
            book = Book(
                title=self.faker.sentence(nb_words=4),
                author=choice(authors),
                start_date=start_date,
                end_date=end_date,
                status=status,
                notes=self.faker.text(max_nb_chars=200),
                rating=round(uniform(1, 5), 1),
            )
            books.append(book)
        return books

    @staticmethod
    def assign_genres_to_books(books: List[Book], genres: List[Genre]) -> None:
        for book in books:
            book.genres.set([choice(genres) for _ in range(randint(1, 3))])


class DatabasePopulator:
    def __init__(self, chunk_size: int = 1000) -> None:
        self.chunk_size = chunk_size

    def populate(self, model_objects: List, model_class) -> None:
        for i in range(0, len(model_objects), self.chunk_size):
            model_class.objects.bulk_create(model_objects[i : i + self.chunk_size])


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs) -> None:
        DatabaseCleaner.clear()
        self.stdout.write(self.style.WARNING("Previous data deleted."))

        faker = Faker()
        populator = DatabasePopulator()

        # Populate Users
        user_factory = UserFactory(faker)
        users = user_factory.create_users(count=1000)
        populator.populate(users, User)
        self.stdout.write(self.style.SUCCESS(f"{len(users)} users created."))

        # Populate Authors
        author_factory = AuthorFactory(faker)
        authors = author_factory.create_authors(count=500)
        populator.populate(authors, Author)
        self.stdout.write(self.style.SUCCESS(f"{len(authors)} authors created."))

        # Populate Genres
        genre_factory = GenreFactory(faker)
        genres = genre_factory.create_genres(count=50)
        populator.populate(genres, Genre)
        self.stdout.write(self.style.SUCCESS(f"{len(genres)} genres created."))

        # Populate Books
        book_factory = BookFactory(faker, start_date=datetime(1900, 1, 1))
        books = book_factory.create_books(authors=authors, genres=genres, count=10_000)
        populator.populate(books, Book)

        # Assign genres to books
        books = Book.objects.all()
        book_factory.assign_genres_to_books(books, genres)

        # Assign books to users
        for user in users:
            user_books = [books[randint(0, len(books) - 1)] for _ in range(10)]
            user.books.set(user_books)

        self.stdout.write(
            self.style.SUCCESS(f"Database populated with {len(books)} books.")
        )
