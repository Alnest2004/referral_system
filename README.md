# Проект "Referral System"

Этот проект представляет собой систему управления реферальными кодами пользователей.

## Описание

Система позволяет пользователям создавать реферальные коды, которые могут быть использованы другими пользователями при регистрации. Каждый реферальный код имеет срок действия, после которого он становится неактивным.

## Установка

1. Клонируйте репозиторий на свой компьютер:

```shell
git clone https://github.com/Alnest2004/referral_system.git
```

2. Копировать файл `.env` 
```shell
cp .env
```

3. Создать и запустить контейнер (при запуске контейнера будут созданы и применены миграции):
```shell
docker-compose up -d --build
```

4. Создать суперпользователя:
```shell
docker exec -it referral_system python manage.py createsuperuser --username USER
```

5Остановить контейнер
```shell
docker-compose down
```

## Запуск
```shell
docker-compose up
``` 

## Реализованные интерфейсы

### Реализованные API

- [X] `POST /api/users/`
  - создание нового Пользователя

- [x] `POST /api/token/`
  - получение токена JWT авторизации (в Body нужно указать usernmame и password пользователя)

- [x] `GET /api/users/`
  - получение списка Пользователей
  - доступно только авторизованным пользователям

- [x] `GET /api/users/<id: int>/`
  - получение информации по конкретному пользователю
  - доступно только авторизованным пользователям

- [x] `PATCH /api/users/<id: int>/`
  - частичное обновление Пользователя
  - только для Администраторов или самого себя

- [x] `DELETE /api/users/<id: int>/`
  - удаление Пользователя
  - доступно только Администраторам

- [X] `POST /api/referral-code/`
  - используется для регистрации пользователей с помощью реферального кода

- [X] `GET /api/referral-code/`
  - используется для получения реферального кода по электронной почте реферера

- [X] `GET /api/referrals/<int:referrer_id>/`
  - используется для получения информации о пользователях, которые использовали реферальный код, связанный с определенным реферером (пользователем, который отправил приглашение). 

### Реализованные URL

- [x] <http://0.0.0.0:8000/admin/>
  - интерфейс администрирования

### Swagger specifications

- [x] <http://0.0.0.0:8000/swagger/> 
  - A swagger-ui view of your API specification 
- [x] <http://0.0.0.0:8000/swagger.json> 
  - A JSON view of your API specification 
- [x] <http://0.0.0.0:8000/swagger.yaml> 
  - A YAML view of your API specification
- [x] <http://0.0.0.0:8000/redoc/> 
  - A ReDoc view of your API specification 

#### Авторизация с помощью *BasicAuthentication* 
```shell
curl \
  -X GET \
  -H "Content-Type: application/json" \
  -u USER:PASSWORD \
  http://0.0.0.0:8000/api/post/
```

#### Авторизация с помощью *JWT*

- создаём токен авторизации
```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "USER", "password": "PASSWORD"}' \
  http://0.0.0.0:8000/api/token/
```

- получаем ответ вида
> {"refresh":"ey...I0","access":"ey...lQ"}

- авторизуемся с помощью токена:
```shell
curl \
  -X GET \
  -H "Authorization: Bearer ey...lQ" \
  http://0.0.0.0:8000/api/post/
```

## Линтеры

Исходный код проверен линтерами `black` и `flake8`


### Время на реализацию

1 рабочий день


## Использованные библиотеки

- [Django](https://www.djangoproject.com/) v. 5.0.2
- [Django REST framework](https://www.django-rest-framework.org/) v. 3.14.0
- [django-filter](https://django-filter.readthedocs.io/en/stable/) v. 23.5 - allows users to filter down a queryset based on a model’s fields, displaying the form to let them do this
- [Psycopg](https://www.psycopg.org/docs/) v. 2.9.9 - PostgreSQL database adapter for Python
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) v. 1.21.7 - Yet another Swagger generator. Generate real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) v. 5.3.1 - Simple JWT provides a JSON Web Token authentication backend for the Django REST Framework
- [python-dotenv](https://pypi.org/project/python-dotenv/) v. 1.0.1 - Reads key-value pairs from a `.env` file and can set them as environment variables
- [black](https://black.readthedocs.io/en/stable/) v. 24.1.1 - The uncompromising code formatter
- [flake8](https://flake8.pycqa.org/en/latest/index.html) v. 7.0.0- Your Tool For Style Guide Enforcement


Сервер будет доступен по адресу http://127.0.0.1:8000/.

## Тестирование

Для запуска тестов используйте команду:
```shell
python manage.py test
```


