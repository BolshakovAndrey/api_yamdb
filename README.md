REST API для сервиса **YaMDb** 
База отзывов о фильмах, книгах и музыке. 

Груповой итоговый проект студентов _Яндекс.Практикум_ по курсу **"Работа с внешними API"**

**Описание**
Проект **YaMDb** собирает отзывы пользователей на произведения. 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен (например, можно добавить категорию 
«Изобразительное искусство» или «Ювелирка» через интерфейс Django администратора).

**API для сервиса YaMDb.** позволяет работать со следующими сущностями:

**Пользователи** (Получить список всех пользователей, создание пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учетной записи, изменить данные своей учетной записи)

**Произведения**, к которым пишут отзывы (Получить список всех объектов, создать произведение для отзывов, информация об объекте, обновить информацию об объекте, удалить произведение)

**Категории** (типы) произведений (Получить список всех категорий, создать категорию, удалить категорию)

**Жанры** (Получить список всех жанров, создать жанр, удалить жанр)

**Отзывы** (Получить список всех отзывов, создать новый отзыв, получить отзыв по id, частично обновить отзыв по id, удалить отзыв по id)

**Коментарии к отзывам** (Получить список всех комментариев к отзыву по id, создать новый комментарий для отзыва, получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id)

**JWT-токен** (Отправление confirmation_code на переданный email, получение JWT-токена в обмен на email и confirmation_code)

[Полная документация API (redoc.yaml)](https://github.com/BolshakovAndrey/api_yamdb/blob/master/static/redoc.yaml)

При первом запуске для функционирования проекта обязательно выполнить миграции:

`./ manage.py makemigrations` 

`./ manage.py migrate`

При желании вы можете загрузить демо-данные в базу данных командой

`./manage.py loaddata data/fixtures.json
`

**Участники:**

[Гаврилов Павел.](https://github.com/Venatorr/api_yamdb)
Управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля.

[Большаков Анрей.](https://github.com/BolshakovAndrey/api_yamdb) 
Категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них.

[Дробышев Артем.](https://github.com/stpdmnk/api_yamdb-1)
Отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.
