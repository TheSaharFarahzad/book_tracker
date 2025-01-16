from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("Reading", "Reading"),
        ("Completed", "Completed"),
    ]
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    users = models.ManyToManyField(User, related_name="books", blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="Not Started"
    )
    notes = models.TextField(blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
