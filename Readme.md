# Название проекта
## TronProject

### Весь проект обернут в docker
Чтобы развернуть сервис в контейнере, необходимо в терминале прописать:
</br>`docker compose -f docker-compose-devlocal-full.yml up -d`

### Сваггер доступен по адресу `http://localhost:8000/`
Можно тестировать прямо там, можно через Postman
#### GET-запрос: http://localhost:8000/api/v1/requests?page=...&size=...
Page и Size можно указывать произвольно(по умолчанию 1 и 10)

#### POST-запрос: http://localhost:8000/api/v1/tron_info/{address}
Вместо {address} - любой адрес, я использовал: `TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR`

Ну и имеются тесты, рекомендую запускать через IDE и указывать Working directory: TronProject
