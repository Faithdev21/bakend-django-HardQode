# HardQode Test Project

Документация (доступна после запуска проекта):

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

Добавлены .csv файл вместе со специальной management-командой для заполнения БД.


### Технологии

Python 3.9, Django 4.2.2, DRF 3.14, SQLite

### Запуск проекта локально

Склонируйте репозиторий:

```git clone git@github.com:Faithdev21/bakend-django-HardQode.git```

либо

```git clone https://github.com/Faithdev21/bakend-django-HardQode.git```

**!!!Добавьте файл с названием .env в education/ (туда же, где .env.example) и заполните его:!!!**

```
SECRET_KEY=django-insecure-r7=j=j2^+d-vx(rm%0wpa7b!r5t#wb#yeffoq2#co*^2(pg2oy
DEBUG=True
```

Установите poetry и нужные библиотеки:  
1. ```pip install poetry```  
2. ```poetry install```

Выполните миграции:
```python manage.py migrate```

Запустите проект:
```python3 manage.py runserver```

### Тестирование API

Для удобства тестирования можно выполнить команду загрузки тестовых данных в БД:

```python manage.py import_csv```

### Основной функционал:

`http://127.0.0.1/api/products/`  

GET - Получение всех доступных для покупки продуктов.

---

`http://127.0.0.1/api/products/<products_pk>/lessons`

GET - Получение всех уроков продукта к которым пользователь имеет доступ.

---

`http://127.0.0.1/api/products/<product_pk>/grant_access/`

POST - Добавление пользователю прав на чтение уроков продукта.

Пример запроса:

`http://127.0.0.1:8000/api/products/2/grant_access/`

С телом запроса:
```
{
    "user_id": 6
}
```
Ответ:  

![image](https://github.com/Faithdev21/bakend-django-HardQode/assets/119350657/5baf3337-270f-4ac4-8ebf-5a93afb1e3ec)

---

Документация API:

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

### Автор проекта

Егор Лоскутов

https://github.com/Faithdev21
