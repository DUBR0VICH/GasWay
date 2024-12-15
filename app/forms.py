"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import User
from .models import Comment
from .models import Blog
from .models import Order
from .models import Product

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Введите пароль'}))


class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваш никнейм', min_length=2, max_length=100)
    internet = forms.ChoiceField(label='Тема обратной связи:',
                                 choices=(('1', 'Баги'),
                                          ('2','Предложения'),
                                          ('3','Отзыв')), initial=1)
    notice = forms.BooleanField(label='Получать новости о продуктах на email?',
                                required=False)
    email = forms.EmailField(label='Ваш email', min_length=7)
    message = forms.CharField(label='Поле для текста обратной связи:',
                              widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)


# new
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class RoleAssignmentForm(forms.Form):
    """Форма для назначения ролей пользователям."""
    ROLE_CHOICES = [
        ('Клиент', 'Клиент'),
        ('Менеджер', 'Менеджер'),
    ]
    role = forms.ChoiceField(label='Назначить роль', choices=ROLE_CHOICES)

#Класс продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description']  # Поля для редактирования и добавления