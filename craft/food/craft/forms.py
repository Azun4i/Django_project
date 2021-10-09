from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from captcha.fields import CaptchaField

# from .models import Comment
#
#
# class CommentForm(forms.ModelForm):
#
#     class Meta:
#         model = Comment
#         fields = ['text']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пороль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Подтверждения пороля', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserloginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))


# CHOICE_TIME = [
#     '10:00',    '10:30',    '12:30',    '13:00',
#     '14:00',    '14:30',    '15:00',    '15:30',
#     '16:00',    '16:30',    '17:00',    '17:30',
#     '18:00',    '18:30',    '19:00',    '19:30',
#     '20:00',    '20:30',    '21:00',    '21:30',
#     '22:00',    '22:30',    '23:00',    '23:30',
#     '0:00',     '0:30',     '1:00',     '1:30',
#     '2:00',
# ]
#
# CHOICE_PERSON = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


class ReserveForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group'}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group ml-md-4'}), required=False)
    date = forms.CharField(label='Номер телефона', widget=forms.SelectDateWidget(attrs={'class': 'form-group'}),
                           required=False)
    time = forms.ChoiceField(widget=forms.Select())
    # person = forms.ChoiceField(label='Колличество персон', widget=forms.Select(CHOICE_PERSON))
    massages = forms.CharField(label='Примечание', max_length=150, widget=forms.Textarea(attrs={'class': 'form-group'}),
                               required=False)

