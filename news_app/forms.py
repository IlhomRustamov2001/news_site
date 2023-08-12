from django import forms
from django.forms import TextInput
from .models import Contact, Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=[ 'body']
        widgets={
            'body':TextInput(attrs={
                'class':'form-control',
                'style': 'max-width:500px',
                'placeholder': 'body'
            })
        }

        