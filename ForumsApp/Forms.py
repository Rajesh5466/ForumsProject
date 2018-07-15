from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter name'})
    )
    last_name = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Surname'})
    )
    email=forms.EmailField(
        max_length=32,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    username = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )


class QuestionForm(forms.ModelForm):
    class Meta:
        model=Questions
        exclude=['username']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Question title'}),
            'description': forms.Textarea(attrs={'cols': 27, 'rows': 7,'placeholder':'Enter description'}),
            'tags' : forms.TextInput(attrs={'placeholder': 'Enter Hashtags'})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answers
        exclude=['question','username','likes','dislikes']
        widgets={
            'description':forms.Textarea(attrs={'cols': 27, 'rows': 7,'placeholder': 'Enter your Answer'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model=AnswersComments
        exclude=['answer','username']
        widgets={
            'description':forms.Textarea(attrs={'cols': 27, 'rows': 7,'placeholder': 'Enter your Comment'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Questions
        exclude = ['username','title','description']
        widgets={
            'tags':forms.TextInput(),
        }