from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("book_list/", views.BookListView.as_view(), name="book_list"),
    path(
        "update_status/<int:pk>/",
        views.UpdateStatusView.as_view(),
        name="update_status",
    ),
    path(
        "remove_from_list/<int:pk>/",
        views.RemoveFromListView.as_view(),
        name="remove_from_list",
    ),
]
