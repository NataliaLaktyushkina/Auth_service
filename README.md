
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

[Схемы взаимодействия (Avro)](flask_app/src/static)

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


# Проектная работа 7 спринта

Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps){target="_blank"} — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить Twitter, Facebook, VK, Google, Yandex или Mail будет хорошей идеей.

Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

Информация по OAuth у разных поставщиков данных: 

- [Twitter](https://developer.twitter.com/en/docs/authentication/overview){target="_blank"},
- [Facebook](https://developers.facebook.com/docs/facebook-login/){target="_blank"},
- [VK](https://vk.com/dev/access_token){target="_blank"},
- [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
- [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
- [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.

## Дополнительное задание

Реализуйте возможность открепить аккаунт в соцсети от личного кабинета. 

Решение залейте в репозиторий текущего спринта и отправьте на ревью.
