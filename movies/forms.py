from django import forms
from .models import Comment


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rating']

    comment = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 3,
        "cols": 120,
    }), label='', required=True)
    rating = forms.IntegerField()
