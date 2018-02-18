# Инструкция по развёртке
## Установка Docker
Работать по инструкции:
* [Mac](http://docs.docker.com/mac/)
* [Windows](http://docs.docker.com/windows/)
* [Linux](https://docs.docker.com/linux/)
* установка [docker-compose](https://docs.docker.com/compose/install/)

## Сборка проекта

* Выполнить `cp .env.sample .env` . В `.env` указать значения переменных.
* Выполнить `docker-compose build`

## Запуск
* Выполнить `docker-compose up -d`
