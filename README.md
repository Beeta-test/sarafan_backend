# Product API
## Описание
Product API — это REST API для управления категориями, подкатегориями, товарами и списками покупок. Проект включает функционал для создания, обновления, удаления и получения данных о продуктах и связанных моделях.

## Функциональность
Управление категориями и подкатегориями.
CRUD-операции для продуктов.
Возможность добавления продуктов в список покупок.
Очистка списка покупок.
Аутентификация пользователей и управление учетными записями.
## Технологии
Python 3.11
Django 5.1
Django REST Framework
pytest для тестирования
## Установка

Клонируйте репозиторий:
git clone https://github.com/your_username/product_api.git
cd product_api

Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows

Установите зависимости:
pip install -r requirements.txt

Примените миграции базы данных:
python manage.py migrate

Создайте суперпользователя:
python manage.py createsuperuser

Запустите сервер разработки:
python manage.py runserver

## Тестирование
Для запуска тестов используйте команду из директории product_api:
pytest

# Использование API
Основные маршруты
/api/category/	Управление категориями	GET, POST

/api/subcategory/	Управление подкатегориями	GET, POST

/api/product/	Управление товарами	GET, POST

/api/shopping_list/	Список покупок	GET, POST

/api/shopping_list/clear/	Очистка списка покупок	POST

/swagger/ Добументация к API

Примеры API-запросов
Создание продукта
POST /api/product/
Тело запроса:
{
    "name": "New Product",
    "slug": "new-product",
    "image": "path/to/image.jpg",
    "price": "20.00",
    "subcategory": 1,
    "category": 1
}
