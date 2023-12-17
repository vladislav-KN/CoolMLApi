# Запуск программы
### Установка
1. Загрузить: [Docker](https://docs.docker.com/get-docker)
2. Создать сфайл ___docker-compose.yml___:
~~~
name: cool-forecast

services:
  cool.forecast.api:
    image: exqzmepls/cool-forecast-api:0.2.0-beta
    container_name: cool-forecast-api
    depends_on:
      cool.forecast.db:
        condition: service_healthy
      cool.forecast.seq:
        condition: service_started
    ports:
      - 38080:8080

  cool.forecast.db:
    image: timescale/timescaledb-ha:pg14-latest
    container_name: cool-forecast-db
    environment:
      - POSTGRES_DB=cool-forecast
      - POSTGRES_USER=cool
      - POSTGRES_PASSWORD=cool!pwd
    ports:
      - 35432:5432
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 5s
      retries: 5

  cool.forecast.seq:
    image: datalust/seq:latest
    container_name: cool-forecast-seq
    environment:
      - ACCEPT_EULA=Y
    ports:
      - 30080:80

  cool.forecast.ml:
    image: nightmarecat/coolmlapi:latest
    container_name: cool-forecast-ml
    ports:
      - 38000:80
~~~
3. Командная строка для докера
~~~
docker-compose up
~~~
### Командная строка для докера

# Работа с данным API
### Требования
~~~
numpy>=1.26.2
pandas>=2.1.4
fastapi>=0.105.0
uvicorn>=0.24
scikit-learn==1.3.0
pydantic>=2.5.2
requests>=2.31.0
~~~
### Установка
- [Docker](https://docs.docker.com/get-docker)
- [Anaconda](https://www.anaconda.com/download) - для запуска Jupyter NoteBook
- [Образ в DockerHub](https://hub.docker.com/repository/docker/nightmarecat/coolmlapi/general)
### Командная строка для докера
~~~
docker-compose up
~~~
## Шаблоны запросов описаны в http://127.0.0.1:8000/docs

#### Красивая картинка .jpg
![Красивая картинка .jpg](https://images.wallpaperscraft.ru/image/single/kotiata_koty_pushistye_99165_1920x1080.jpg)
