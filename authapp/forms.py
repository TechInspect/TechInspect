from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

import hashlib
import random

from authapp.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # Добавить placeholder
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес элeктронной почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, *args, **kwargs):
        user = super(UserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class UserProfileForm(UserChangeForm):
    # изменить встроенные поля - widget=forms.FileInput() (убрать кнопки изменить, очистить)
    # required - не обязательно загружать изображение
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # readonly - поле доступно только для чтения
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            if field_name != 'avatar':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'custom-file-input'
        # вместо else можно:
        # self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        # profile.html add in form enctype="multipart/form-data" - чтобы отправлять файлы