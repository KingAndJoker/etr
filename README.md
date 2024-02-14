# etr

Project handler Codeforces API and returns list of submissions some users.

## Run

commant prompt:

```shell
uvicorn etr:app
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
DATABASE_ECHO=true
CODEFORCES_API_KEY=0123456789abcdef0123456789abcdef01234567
CODEFORCES_API_SECRET=0123456789abcdef0123456789abcdef01234567
SQL_PASSWORD=12345
```

## Example ```alembic.ini```

```apacheconf
...
sqlalchemy.url = driver://user:pass@localhost/dbname
...
```

Alembic.ini file generate automatically. But you don`t forget to set sqlalchemy.url - the url for the database.

## Run migrations

Before performing the migration you must run the command:

```shell
alembic init "folder"
```

In `alembic/env.py` you have to write the code:

```python
...
from etr.models.base import Base
from etr.models.problem import Problem, problems_tags, Tag
from etr.models.user import User
from etr.models.team import Team, teams_users
from etr.models.submission import Submission
from etr.models.contest import Contest
target_metadata = Base.metadata
...
```

This code sets the metadata for alembic.

After you do something in the database models you have to perform the migration.

```shell
alembic revision --autogenerate -m "some message..."
alembic upgrade head
```
