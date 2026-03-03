from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'mood', 'date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトルを入力'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '今日の出来事を書いてみましょう',
                'rows': 8
            }),
            'mood': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }