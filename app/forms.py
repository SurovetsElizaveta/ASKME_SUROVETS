from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password', 'password_confirmation')

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords do not match')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        user.save()
        profile = Profile(user=user)
        profile.save()

        return user

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(min_length=2, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    email = forms.CharField()
    # avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password')

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #
    #     # user.username = self.username
    #     # user.set_password(self.cleaned_data['password'])
    #     # user.email = self.email
    #     # profile = Profile
    #     # profile.save()
    #     return user

class AskForm(forms.ModelForm):
    tag = forms.CharField()
    class Meta:
        model = Question
        fields = ['title', 'text', 'tag']

    def clean(self):
        data = super().clean()
        if len(data['tag'].split(' ')) > 3:
            raise ValidationError('You can add only 3 tags.')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']