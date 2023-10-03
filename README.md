# etr

Project handler Codeforces API and returns list of submissions some users.

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

Database is MySQL.

```shell
docker run --name etr_db -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password --restart unless-stopped mysql:8.1.0
```

Url to database:

```apacheconf
mysql+mysqlconnector://root:1@localhost:3306
```

## Example ```.env```

```apacheconf
URL_PREFIX=/etr
URL_DATABASE=mysql+mysqlconnector://root:password@localhost:3306
```
