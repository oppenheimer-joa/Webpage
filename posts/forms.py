# forms.py

from django import forms

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('title', '영화 제목'),
        ('people', '영화 인물'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    search_term = forms.CharField(max_length=100)
