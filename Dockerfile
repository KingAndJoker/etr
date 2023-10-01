FROM python:3.11.5-slim-bookworm

VOLUME /volume
LABEL maintainer="a12345678.87654321@yandex.ru"
WORKDIR /etr
COPY . .
RUN pip3 install --upgrade pip -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["sh", "./boot.sh"]