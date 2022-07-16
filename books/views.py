import datetime
from pytz import timezone
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from books.models import Book, Order, OrderLineItem
from .serializers import BookSerializer, OrderSerializer, OrderLineItemSerializer, UploadCsvSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from book_store import settings
import pandas as pd


class BookApiView(APIView, LimitOffsetPagination):

    def get(self, request, *args, **kwargs):
        '''
        List all the books
        '''
        books = Book.objects.filter().all()
        results = self.paginate_queryset(books, request, view=self)
        serializer = BookSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class OrdersApiView(APIView, IsAuthenticated, LimitOffsetPagination):

    def get(self, request, *args, **kwargs):
        """
        List all the order of last 90  day's
        """
        date = datetime.datetime.now(timezone(settings.TIME_ZONE)) - datetime.timedelta(days=settings.DELTA_PERIOD)
        order = Order.objects.filter(created_at__gte=date).all()
        results = self.paginate_queryset(order, request, view=self)
        serializer = OrderSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class LineItemApiView(APIView, IsAuthenticated, LimitOffsetPagination):

    def get(self, request, *args, **kwargs):
        """
        List all the order items of last 90 day's
        """
        date = datetime.datetime.now(timezone(settings.TIME_ZONE)) - datetime.timedelta(days=settings.DELTA_PERIOD)
        order_line_item = OrderLineItem.objects.filter(created_at__gte=date).all()
        results = self.paginate_queryset(order_line_item, request, view=self)
        serializer = OrderLineItemSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class CreateOrder(APIView):

    def post(self, request, *args, **kwargs):
        """
        create an order and line item
        """
        item_list = request.data.get('item_list')
        if not item_list:
            return Response({"Error-1": "No Book is added in cart"}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(id__in=[i["book_id"] for i in item_list]).all()
        order_amount = 0
        line_item_list = []
        for item in item_list:
            try:
                if not item:
                    raise Exception(f"Empty  Item")

                book_id = int(item.get("book_id"))
                if not book_id:
                    raise Exception(f"No Book  ID Item")

                quantity = int(item.get("quantity"))
                if not quantity:
                    raise Exception(f"No quantity for  Item")

                if quantity > settings.LIMIT:
                    raise Exception(f"book quantity exceed {settings.LIMIT}")

                book = books.get(id=109)
                if not book.is_active or book.stock < quantity:
                    raise Exception(f"{book.book} is out of stock")

                amount = book.price*quantity
                new_item = {
                    "order_id": 0,
                    "book_id": book_id,
                    "quantity": quantity,
                    "amount": amount
                }
                order_amount += amount
                line_item_list.append(new_item)

            except Exception as e:
                return Response({"Error-2": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        order_detail = {
            "item_list": item_list,
            "amount": order_amount,
        }
        serializer = OrderSerializer(data=order_detail)
        if serializer.is_valid():
            serializer.save()

            for item in line_item_list:
                item["order_id"] = serializer.data["id"]
                book = books.get(id=item["book_id"])
                book.stock -= item["quantity"]
                book.updated_at = datetime.datetime.now(timezone(settings.TIME_ZONE))
                book.save()

            item_serializer = OrderLineItemSerializer(data=line_item_list, many=True)
            if item_serializer.is_valid():
                item_serializer.save()
                return Response({"OrderDetails": serializer.data, "ItemDetails": item_serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadCsvSerializer

    def post(self, request, *args, **kwargs):
        serializer = UploadCsvSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():

            book = Book.objects.filter(id=row['id'])[0]
            if book:
                book.price = row['price']
                book.stock += row['stock']
                book.is_active = row['is_active']
                book.updated_at = datetime.datetime.now(timezone(settings.TIME_ZONE))
                book.save()
            else:
                new_file = Book(
                    id=row['id'],
                    book=row["book"],
                    price=row['price'],
                    stock=row["stock"],
                    is_active=row["is_active"],
                    created_at=datetime.datetime.now(timezone(settings.TIME_ZONE)),
                    updated_at=datetime.datetime.now(timezone(settings.TIME_ZONE)),
                )
                new_file.save()
        return Response({"status": "success"}, status.HTTP_201_CREATED)
