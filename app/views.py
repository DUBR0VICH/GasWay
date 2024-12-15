"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import Blog

from .models import Comment
from .forms import CommentForm

from .forms import BlogForm

#new
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import Product, Order
from .forms import OrderForm, ProductForm
from django.contrib.auth.models import User
from .forms import RoleAssignmentForm



def home(request):
    """Renders the home page."""
    posts = Blog.objects.all()[:3]  # Получаем последние 3 новости
    return render(
        request,
        'app/index.html',
        {
            'title': 'Официальный сайт Gas Way',
            'year': datetime.now().year,
            'posts': posts,  # Передаём новости в шаблон
        }
    )

def cart(request):
    """Renders the cart page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Корзина',
            'message':'Корзина с вашими товарами',
            'year':datetime.now().year,
        }
    )

def catalog(request):
    """Renders the catalog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title':'Каталог',
            'message':'Каталог',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Контакты',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    internet = {'1': 'Баги', '2': 'Предложения', '3': 'Отзыв'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['internet'] = internet[ form.cleaned_data['internet'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data,
            'title':'Форма обратной связи',
            'year':datetime.now().year
        }
    )

def registration(request):
    """Renders the registration page."""
    
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            regform.save() # сохраняем изменения после добавления данных

            # Назначение роли "Клиент" пользователю
            client_group = Group.objects.get(name='Клиент')  # Получаем группу "Клиент"
            reg_f.groups.add(client_group)  # Добавляем пользователя в группу

            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Новости',
            'posts': posts, #список статей в шаблон страницы
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the posted blog page."""
    post_1 = get_object_or_404(Blog, id=parametr)  # Получаем пост
    comments = Comment.objects.filter(post=parametr)  # Комментарии к посту

    # Проверка прав пользователя
    can_manage_post = request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name="Менеджер").exists()
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'can_manage_post': can_manage_post,  # Передача результата проверки
            'year': datetime.now().year,
        }
    )


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью',
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Описание',
            'message':'Страница с описанием',
            'year':datetime.now().year,
        }
    )


#new


# Проверки для ролей
def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

def is_client(user):
    return user.groups.filter(name='Клиент').exists()

# Каталог товаров
def catalog(request):
    products = Product.objects.all()

    # Проверка, может ли пользователь управлять каталогом
    can_manage_catalog = request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name="Менеджер").exists()
    )

    return render(
        request,
        'app/catalog.html',
        {
            'products': products,
            'can_manage_catalog': can_manage_catalog,  # Передаём в шаблон
        }
    )


# Корзина клиента
@login_required
@user_passes_test(is_client, is_manager)
def cart(request):
    orders = Order.objects.filter(client=request.user, status='pending')
    return render(request, 'app/cart.html', {'orders': orders})

# История заказов клиента
@login_required
@user_passes_test(is_client, is_manager)
def my_orders(request):
    orders = Order.objects.filter(client=request.user)
    return render(request, 'app/my_orders.html', {'orders': orders})

# Управление заказами менеджером
@login_required
@user_passes_test(is_manager)
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'app/manage_orders.html', {'orders': orders})

# Добавление товара в корзину
@login_required
@user_passes_test(is_client, is_manager)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.status = 'pending'
            order.save()
            return redirect('cart')
    else:
        form = OrderForm(initial={'product': product})
    return render(request, 'app/add_to_cart.html', {'form': form, 'product': product})

# Изменение ролей пользователей
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    users = User.objects.all()

    # Создаём группы, если они ещё не существуют
    client_group, _ = Group.objects.get_or_create(name='Клиент')
    manager_group, _ = Group.objects.get_or_create(name='Менеджер')

    message = None  # Сообщение об изменении роли

    if request.method == "POST":
        user_id = request.POST.get('user_id')  # Получаем ID пользователя
        new_role = request.POST.get('role')  # Получаем выбранную роль

        if user_id and new_role:  # Если оба поля заполнены
            user = User.objects.get(id=user_id)

            # Удаляем все текущие роли
            user.groups.clear()

            # Назначаем новую роль
            if new_role == 'Клиент':
                user.groups.add(client_group)
            elif new_role == 'Менеджер':
                user.groups.add(manager_group)

            # Формируем сообщение об успешной смене роли
            message = f"Роль пользователя '{user.username}' была изменена на '{new_role}'."

            return render(request, 'app/manage_users.html', {'users': users, 'message': message})

    return render(request, 'app/manage_users.html', {'users': users, 'message': message})






# Редактирование и удаление постов
@login_required
@user_passes_test(lambda u: u.is_superuser or is_manager(u))
def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog')  # Возвращаемся на страницу новостей
    else:
        form = BlogForm(instance=post)

    return render(request, 'app/edit_post.html', {'form': form, 'post': post})

@login_required
@user_passes_test(lambda u: u.is_superuser or is_manager(u))
def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('blog')  # Возвращаемся на страницу новостей
    return render(request, 'app/delete_post.html', {'post': post})


# Добавление, редактирование, удаление товаров
@login_required
@user_passes_test(lambda u: u.is_superuser or is_manager(u))
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новый товар в модель Product
            return redirect('catalog')  # Возвращаемся в каталог
    else:
        form = ProductForm()

    return render(request, 'app/add_product.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser or is_manager(u))
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)  # Используем ProductForm
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm(instance=product)

    return render(request, 'app/edit_product.html', {'form': form, 'product': product})


@login_required
@user_passes_test(lambda u: u.is_superuser or is_manager(u))
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('catalog')
    return render(request, 'app/delete_product.html', {'product': product})
