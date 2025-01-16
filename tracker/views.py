from django.views.generic import ListView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Genre, Author
from .forms import BookUpdateForm


class BaseBookListView(ListView):
    model = Book
    context_object_name = "books"
    paginate_by = 20

    def build_filters(self):
        filters = Q()
        if search_query := self.request.GET.get("search"):
            filters &= Q(title__icontains=search_query)
        if author_name := self.request.GET.get("author"):
            filters &= Q(author__name__icontains=author_name)
        if genre_name := self.request.GET.get("genre"):
            filters &= Q(genres__name__icontains=genre_name)
        if status_filter := self.request.GET.get("status"):
            filters &= Q(status=status_filter)
        return filters

    def get_ordering(self):
        sort = self.request.GET.get("sort", "title")
        sort_order = self.request.GET.get("sort_order", "asc")
        return f"{'-' if sort_order == 'desc' else ''}{sort}"

    def get_current_filters(self):
        return {
            "search": self.request.GET.get("search", ""),
            "author": self.request.GET.get("author", ""),
            "genre": self.request.GET.get("genre", ""),
            "status": self.request.GET.get("status", ""),
            "sort": self.request.GET.get("sort", "title"),
            "sort_order": self.request.GET.get("sort_order", "asc"),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "authors": Author.objects.all(),
                "genres": Genre.objects.all(),
                "statuses": Book.STATUS_CHOICES,
                "current_filters": self.get_current_filters(),
            }
        )
        return context


class HomeView(BaseBookListView):
    template_name = "tracker/home.html"

    def get_queryset(self):
        return (
            Book.objects.filter(self.build_filters())
            .select_related("author")
            .prefetch_related("genres")
            .defer("start_date", "end_date", "notes", "rating")
            .order_by(self.get_ordering())
        )

    def get_total_books_count(self):
        return Book.objects.filter(self.build_filters()).count()

    def get_user_books(self):
        if self.request.user.is_authenticated:
            return self.request.user.books.all()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books_count"] = self.get_total_books_count()
        context["user_books"] = self.get_user_books()
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
            .filter(self.build_filters())
            .distinct()
            .select_related("author")
            .prefetch_related("genres")
            .defer("start_date", "end_date", "notes", "rating")
            .order_by(self.get_ordering())
        )

    def get_total_books_count(self):
        filters = Q(users=self.request.user) & self.build_filters()
        return Book.objects.filter(filters).count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books_count"] = self.get_total_books_count()
        return context


class UpdateStatusView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = "tracker/book_update.html"

    def get_success_url(self):
        return reverse_lazy("tracker:book_list")

    def get_object(self, queryset=None):
        return get_object_or_404(
            Book.objects.select_related("author").prefetch_related("genres"),
            pk=self.kwargs["pk"],
        )


class RemoveFromListView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.users.remove(request.user)
        return redirect("tracker:book_list")
