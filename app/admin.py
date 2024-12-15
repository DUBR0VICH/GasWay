from django.contrib import admin
from .models import Category, Product, Order  # Импортируем модели

# Регистрируем модели для админки
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
