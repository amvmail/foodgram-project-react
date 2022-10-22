                                            **Сайт «Продуктовый помощник»**                                                
  
                                                                             Тут должна быть ссылка на статус git



«Продуктовый помощник» — дипломный проект курса «Python-разработчик» от Яндекс.Практикум.

Это онлайн-сервис, на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

**Логины для тестов**
***
адрес сервера - http://ipbuild.ru 
ip сервера    - 158.160.9.100

superuser (admin) - login     su           email
                    passwd    123456Aa   admin@foodgram.ru
food1 (user)  - login     food1
                passwd    12345678Aa
                reg_email food1@foodgram.ru
food2 (user)  - login     food2
                passwd    12345678Aa
                reg_email food2@foodgram.ru
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

**Запуск сервера по адресу http://ipbuild.ru**
***
python manage.py runserver
***

**Загрузка тестовых данных:**
***
docker-compose exec web python manage.py loaddata fixtures.json
***