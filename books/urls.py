from django.urls import path, include
from books import views

app_name = "Books"

urlpatterns = [
    path('books', views.BookApiView.as_view(), name='books'),
    path('books_csv_upload', views.UploadCSV.as_view(), name='books_csv_upload'),
    path('orders', views.OrdersApiView.as_view(), name='orders'),
    path('line-items', views.LineItemApiView.as_view(), name='line-items'),
    path('create-order', views.CreateOrder.as_view(), name='create-order'),
]
