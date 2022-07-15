from django.contrib import admin
from books.models import Book, Order, OrderLineItem

# Register your models here.
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderLineItem)
