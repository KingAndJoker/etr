# etr

## Run

commant prompt:

```shell
flask --app etr run
```

### Docker run

```shell
docker build -t etr:latest .
docker run --name etr -d -p 8000:5000 --rm etr:latest
```

## Database

Database is SQLite.

Url to database:

```apacheconf
sqlite:///users.db
```
