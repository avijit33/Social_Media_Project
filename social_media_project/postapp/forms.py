from django import forms
from postapp.models import Posts

class Postform(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['image','caption',]