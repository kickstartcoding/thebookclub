from django import forms

class AddBookForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

GENRES = [
    ('fiction', 'Adult Fiction'),
    ('nonfiction', 'Adult Non-Fiction'),
    ('children', "Children's Books"),
]

class AddReadingListForm(forms.Form):
    name = forms.CharField()
    topic = forms.ChoiceField(choices=GENRES)

