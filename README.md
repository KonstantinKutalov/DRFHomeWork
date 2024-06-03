Запуск проекта с помощью Docker

Необходимые инструменты:

Docker

Docker Compose

Установка:

Клонируйте репозиторий:

git clone https://github.com/KonstantinKutalov/DRFHomeWork.git

Перейдите в директорию проекта:

cd DRFHomeWork

Создайте файл .env с следующими переменными:

POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=

Запуск:

Запустите Docker Compose:

docker-compose up -d

Доступ к проекту:

Django: http://localhost:8000/

PostgreSQL:

Redis:

Дополнительные команды:

Остановка всех сервисов:

docker-compose down

Перезапуск всех сервисов:

docker-compose restart

Просмотр журналов:

docker-compose logs

Просмотр состояния сервисов:

docker-compose ps

Размещение на удаленном сервере:

Установите Docker и Docker Compose на удаленном сервере.

Скопируйте все файлы проекта на сервер.

Запустите docker-compose up -d.
