from rest_framework import serializers
from .models import Book, Order, OrderLineItem


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineItem
        fields = '__all__'


class UploadCsvSerializer(serializers.Serializer):

    file = serializers.FileField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

