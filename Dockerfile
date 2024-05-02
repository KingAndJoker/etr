FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y nano && apt-get clean && rm -rf /var/lib/apt/lists/*

VOLUME /volume
VOLUME /etr/.alembic/
LABEL maintainer="a12345678.87654321@yandex.ru"
WORKDIR /etr
COPY . .
RUN pip3 install --upgrade pip -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["sh", "./boot.sh"]