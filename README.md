# EdMachine
API for Ed Machine

## swagger
- /docs

## required environment variables
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASS
- DB_NAME

## run API

    uvicorn app.main:app --reload --port 8090


## run migrations 

    #generate
    alembic revision --autogenerate -m "initial migration"

    #New changes
    alembic revision -m "Add a column"

    #run
    alembic upgrade head

## install required packages 

    pip install -r requirements.txt


## REQUIREMENTS FOR GROUP WORK IN VSCODE

```json
    {
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.linting.flake8Args": ["--config=.flake8"]
    }
```

## DOCUMENTATION

    http://127.0.0.1:8090/docs
    http://127.0.0.1:8090/redoc