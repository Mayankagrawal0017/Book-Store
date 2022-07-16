from django.db import models


class Book (models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.CharField(max_length=255, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.book)


class Order (models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField(null=False, blank=False)
    item_list = models.JSONField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        ordering = ('-created_at',)


class OrderLineItem (models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    amount = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_line_item'
        unique_together = ('order_id', 'book_id',)
        ordering = ('-created_at',)

