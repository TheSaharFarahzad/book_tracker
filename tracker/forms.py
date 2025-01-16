from django import forms
from .models import Book


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["start_date", "end_date", "status", "notes", "rating"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=Book.STATUS_CHOICES),
            "notes": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "rating": forms.NumberInput(attrs={"min": 0, "max": 5}),
        }
