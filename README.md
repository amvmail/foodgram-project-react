                                            **Сайт «Продуктовый помощник»**                                                
  
                                                                             Тут должна быть ссылка на статус git



«Продуктовый помощник» — дипломный проект курса «Python-разработчик» от Яндекс.Практикум.

Это онлайн-сервис, на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

**Логины для тестов**
***
superuser (admin) - login     super
                    passwd    123456Aa
                    reg_email admin@foodgram.ru
testuser1 (user)  - login     food1
                    passwd    Foodfood1
                    reg_email food1@foodgram.ru
testuser2 (user)  - login     food2
                    passwd    Foodfood2
                    reg_email food2@foodgram.ru
testuser3 (user)  - login     food3
                    passwd    Foodfood3
                    reg_email food3@foodgram.ru
testuser4 (user)  - login     food4
                    passwd    123456Qw#
                    reg_email food4@foodgram.ru
***

**Работа по подготовке сервера для установки сервиса.**

Необходимо установить Docker с официального сайта.
Информация по работе с проектом (в режиме работы с контейнерами)


**Клонирование проекта:**

git clone https://github.com/amvmail/foodgram-project-react.git


**Работа с контейнерами:**

Вход в командную оболочку внутри контейнера:
***
docker exec -it <container_id> bash
***

**Создание миграций (в cli контейнера):**
***
python manage.py migrate
***

**Создание суперпользователя (в командной оболочке):**
***
python manage.py createsuperuser
***

**Сбор статики:**
***
python manage.py collectstatic --no-input
***

**Запуск сервера по адресу http://127.0.0.1/:8000**
***
python manage.py runserver
***

**Загрузка тестовых данных:**
***
docker-compose exec web python manage.py loaddata fixtures.json
***