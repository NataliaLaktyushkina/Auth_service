
#### Адрес репозитория:
https://github.com/NataliaLaktyushkina/Auth_sprint_2.git

[Получить client_id и secret_key](https://console.cloud.google.com/apis/credentials/oauthclient)

#### Запуск приложения:

`docker-compose up --build`

Необходимо запустить в папке с файлом *"alembic.ini":*
`alembic revision -m "initial"`
`alembic upgrade head`    
`alembic revision --autogenerate`
`alembic upgrade head` 

Создание пользователя с админскими правами:
Переменные окружения:
- SUPERUSER_NAME
- SUPERUSER_EMAIL
- SUPERUSER_PASS

Команды:
- `export FLASK_APP=auth_app`
- `flask create-superuser`

#### OAuth 2.0:
[Login](http://127.0.0.1:5001/v1/oauth_login)

[Схемы взаимодействия](flask_app/src/static/swagger_config.yml)

[Репозиторий Movie API](https://github.com/NataliaLaktyushkina/Sprint_4_Async_API)

Полученный токен можно передать в заголовке Authorization, теле запроса или GET-параметрах. 
Рекомендуется всегда использовать именно заголовки авторизации, 
как наиболее естественный для HTTP способ.

####  Jaeger:
[Реализация](flask_app/src/utils/tracer.py)
[Использование №1](flask_app/src/api/v1/oauth.py)
[Использование №2](flask_app/src/api/v1/personal_account.py)

#### Limiter:
[Реализация](flask_app/src/utils/token_bucket.py)
[Использование](flask_app/src/api/v1/personal_account.py)

#### Партицирование
[Партицирование](flask_app/src/database/dm_models.py) по дате рождения (=возрасту) - для фильтрации контента
 Alembic не подтянул партицирование - [миграции прописаны вручную](flask_app/src/alembic/versions/custom1_partition.py)

При созданнии партицированной таблицы - ключ партицирования необходимо указать как primary key, по-другому primary key для таблицы postgres создать не дает.
При этом в других таблицах есть foreign keys, которые ссылаются на id в таблицы users. 
Я хотела перенести данные из таблицы users в новую партицированную таблицу. 
Для этого нужно пересоздать foreign keys в таблицах (login history, social_acc), чтобы ключ ссылался на новую таблицу,
Но postgres не дает создать новый ключ -  (psycopg2.errors.InvalidForeignKey) there is no unique constraint matching given keys for referenced table "users_partitioned".
Unigue constraint без указания колонки партицирования postgres также не дает создать -  unique constraint on partitioned table must include all partitioning columns

**И получается, что непонятно, как будут другие таблицы работать с партицированной.**

----

[Список переменных окружения](flask_app/src/utils/.env.example)

[Документация по AuthAPI](http://127.0.0.1:80/apidocs )

----
P.S. Если после обновления swagger_config.yml не обновляется отображение
endpoint'ов, то можно:
- почистить кэш в браузере
- удалить images
- удалить volumes
и собрать контейнреы заново
