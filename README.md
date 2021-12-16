# ClickSign Storage Service v1

ClickSign Storage Service is api to store files and folders

## Installation

Use the package manager [poetry](https://python-poetry.org/docs/) to install packages.

```bash
poetry install
```

Set the env var ```SQLALCHEMY_DATABASE_URL``` with PostgreSQL connection string

```bash
postgresql://[user]:[pass]@[host]:5432/[database_name]
```

Apply migrations

```bash
alembic upgrade head
```

Set initial data

```bash
poetry run python pre_init.py
```

## Run

```bash
poetry run uvicorn app.main:app
```

Access api documentation in ```http://127.0.0.1:8000/docs``` or ```http://127.0.0.1:8000/redoc```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
