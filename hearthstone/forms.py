from django import forms
from .models import Comment

class SearchForm(forms.Form):
    query = forms.CharField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)