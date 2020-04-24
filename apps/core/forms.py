from django import forms
from apps.core.models import Book, ReadingList

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']

class AddReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['title', 'category', 'description', 'tags']

