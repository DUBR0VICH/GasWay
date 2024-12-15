"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User



# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, verbose_name = "Автор")

    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    # Методы класса

    def get_absolute_url(self): # Метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self): # Метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title

    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # Имя таблицы для модели
        ordering = ["-posted"] # Порядорк сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # Имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # Тоже для вмех статей блога

admin.site.register(Blog)

class Comment(models.Model):
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name = "Статья комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "Автор комментария")
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)


# new
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[('pending', 'Ожидание'), ('completed', 'Завершено')])

    def __str__(self):
        return f"Order {self.id} by {self.client.username}"

# Модель связки корзины с клиентом
class CartItem(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} для {self.client.username}"
