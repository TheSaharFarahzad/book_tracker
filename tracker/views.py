from django.views.generic import ListView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Genre, Author
from .forms import BookUpdateForm


class BaseBookListView(ListView):
    model = Book
    context_object_name = "books"

    def get_ordering(self):
        sort = self.request.GET.get("sort", "title")
        sort_order = self.request.GET.get("sort_order", "asc")
        return f"{'-' if sort_order == 'desc' else ''}{sort}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "authors": Author.objects.all(),
                "genres": Genre.objects.all(),
                "statuses": Book.STATUS_CHOICES,
            }
        )
        return context


class HomeView(BaseBookListView):
    template_name = "tracker/home.html"

    def get_queryset(self):
        return Book.objects.all().order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_count = Book.objects.all().count()
        context["total_books_count"] = books_count
        context["user_books"] = (
            self.request.user.books.all() if self.request.user.is_authenticated else []
        )
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("You must be logged in to perform this action.")

        book = get_object_or_404(Book, id=request.POST.get("book_id"))
        action = request.POST.get("action")

        if action == "add":
            book.users.add(request.user)
        elif action == "remove":
            book.users.remove(request.user)
        else:
            raise Http404("Invalid action.")

        return self.get(request, *args, **kwargs)


class BookListView(LoginRequiredMixin, BaseBookListView):
    template_name = "tracker/book_list.html"

    def get_queryset(self):
        return (
            Book.objects.filter(users=self.request.user)
            .distinct()
            .order_by(self.get_ordering())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_books_count = Book.objects.filter(users=self.request.user).count()
        context["total_books_count"] = user_books_count
        return context


class UpdateStatusView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = "tracker/book_update.html"

    def get_success_url(self):
        return reverse_lazy("tracker:book_list")

    def get_object(self, queryset=None):
        return get_object_or_404(Book, pk=self.kwargs["pk"])


class RemoveFromListView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.users.remove(request.user)
        return redirect("tracker:book_list")
