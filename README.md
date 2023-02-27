# Медицинский справочник

## Запуск

### Скачать

```
git clone https://github.com/Arcane97/medical_reference_books.git
```

### Установить зависимости

Зависимости можно установить с помощью poetry либо virtualenv.

```
cd medical_reference_books

pip install -r requirements.txt
либо
poetry init
poetry install
```

### Запуск Django dev сервера

```
cd src
python manage.py runserver
```

## Описание

Админ-панель находится на:
http://127.0.0.1:8000/admin/

Логин пароль администратора: admin admin

Swagger документация http://127.0.0.1:8000/docs/

