# Project Setup Guide :
  git clone  https://github.com/Mayankagrawal0017/Book-Store.git
  
  create  venv
  
  # run following cammand 
  pip install -r requierment.txt 
  sqlite3 db.sqlite3 < dump.sql 
  python manage.py  runserver 8000
  
  

# Book-Store
Simpel  Django  REST-API  Based  Order-Product Design  

# Postman Collection
https://www.getpostman.com/collections/8b8f94219e28a9344bdd

# Postman documentation
https://documenter.getpostman.com/view/19133639/UzQvsQHN

# Sample CSV
 https://drive.google.com/file/d/1atod9u3KTUhXnU9-JLKl04zbK4GRroAD/view?usp=sharing
 
 
# API  Url's  Localhost: 8000
  POST http://127.0.0.1:8000/create-order
  POST http://127.0.0.1:8000/books
  POST http://127.0.0.1:8000/orders
  POST http://127.0.0.1:8000/line-items
  POST http://127.0.0.1:8000/books_csv_upload
