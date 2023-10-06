# Foodgram.
## Блог рецептов.
#### Базовый сервис. Для всех пользователей.
1. **На главной странице** вы найдете рецепты наших пользователей. Они представлены карточками с изображением рецепта и его названием. Вы можете посматривать весь список рецептов с помощью навигации по цифрам внизу страницы.
2. **При нажатии на конкретный рецепт** откроется его страница, с полной информацией: описание рецепта, кол-во ингредиентов и прочее.
3. **С помощью тегов** можно отфильтровать рецепты по времени приема пищи (завтрак, обед или ужин). **Теги** отображаются на странице рецепта.
#### Регистрация.
4. Если вы захотите у нас остаться первым делом стоит зарегистрироваться. Это откроет доступ к дополнительным полезным функциям сайта.
#### Расширенный сервис. Для авторизованных пользователей.
5. **Создавать свои** собственные **рецепты**, они буду сохраняться в вашей кулинарной книге (в вашем профиле). Ингредиенты при этом выбираются из нашей обширной базы, в которой найдется все ! 
   П.с. если все же там не хватает нужного вам ингредиента обратитесь в службу обратной связи - напишите мне на почту;). 
6. **Взаимодействовать с** кулинарными **книгами других** пользователей: просматривать, добавлять в избранное, оставлять комментарии под рецептами.
7. **Добавлять** рецепты **в** нашу специальную **корзину**, которая просуммирует все ингредиенты и выдаст вам итоговый список покупок в PDF-файле.
---
### Эндпоинты не вошедшие в стандартный UI.
1. `admin/` - админ-панель Django.
2. `api/docs/` - документация Redoc по API проекта.
---
### Инструкции для запуска приложения на вашем сервере.

1. Клонируйте этот репозиторий на сервер.

2. Переименуйте файл `infra/.env.dist` в `.env`. В этом файле находятся конфиги проекта. При необходимости здесь вы можете установить собственные значения.

3. Запустите контейнеры Docker. | Необходим [Docker](https://www.docker.com/get-started/) и [Docker Compose](https://docs.docker.com/compose/install/standalone/)
```bash
# Из директории infra/
docker-compose up -d
```

* Сайт будет доступен по адресам указанным в ALLOWED_HOSTS (см. `.env` файл).

Рекомендуется также:

4. Создать суперпользователя для админ-панели.
```bash
docker-compose exec backend python manage.py createsuperuser 
```

5. Загрузить в БД подготовленные данные.
```bash
docker-compose exec backend python manage.py loaddata fixtures.json
```
