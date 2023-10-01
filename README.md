# etr

## Run

commant prompt:

```shell
flask --app etr run
```

### Docker run

```shell
docker build -t 2biwy:latest .
docker run --name 2biwy -d -p 8000:5000 --rm 2biwy:latest
```

## Database

Database is SQLite.

Url to database:

```apacheconf
sqlite:///users.db
```
