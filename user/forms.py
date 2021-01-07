from django import forms
from .models import Profile


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'social_media_url']

    profile_pic = forms.ImageField()
    social_media_url = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 1,
        "cols": 80,
    }), label='')
