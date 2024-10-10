# Проект Django с Docker

Этот проект представляет собой API на основе Django, работающий с PostgreSQL и Docker. В нем реализованы основные CRUD-операции для управления пользователями и продуктами, а также аутентификация на основе JWT.

## Требования

- Docker
- Docker Compose

## Запуск проекта

### Шаг 1: Создайте базу данных

Перед запуском убедитесь, что у вас настроена база данных PostgreSQL. Вам нужно создать базу данных, а также настроить переменные среды в файле `.env`.

### Шаг 2: Настройте файл .env

Создайте файл `.env` в корне проекта и добавьте следующие параметры:

### Шаг 3: Соберите и запустите контейнеры

Для сборки и запуска проекта используйте следующую команду:

```
docker-compose -f docker-compose.yml up --build
```

Свагер находиться по адресу 
http://localhost:8000/api/swagger


### для создание супер пользователя 
docker-compose exec web python manage.py createsuperuser

# product_test
