# Currencies converter REST service

### Main features

* supported currencies: USD, EUR, CZK, PLN
* currencies rates are updated _everyday at 3:30 am CET_
* source data is fetched via [http://openexchange.org](http://openexchange.org)
* any math calculations use decimal precision of 6

### Endpoints

|Method|URL|Path Params|Description|
|------|---|------|-----------|
|**GET**|`/api/currencies/convert`|`:base/:to/:amount` _(all required)_|Currencies convert controller|

See [Documentation](#Documentation) for more detailed information about the API.

## Getting Started

### Prerequisites

* [Docker](https://docker.com) _(if you want to make your life easier)_
* [Poetry](https://python-poetry.org) _(for development only)_

### Installation

1. Get a free API Key at [http://openexchangerates.org](http://openexchangerates.org)
2. Clone the repo
   ```shell script
   git clone https://github.com/bxsx/currencies-converter-rest-service-fastapi.git
   ```
3. Go to the project directory
   ```shell script
   cd currencies-converter-rest-service-fastapi/
   ```
4. Setup your `.env`, you can use `.env-dev` as example (**NOTE:** `.env-dev` is not [production-ready](#development-vs-production-version))
   ```shell script
   cp .env-dev .env
   ```
5. Enter your API key (`abcdef123456` here) in `.env`
   ```shell script
   sed -i -e 's/OXR_ID=.*/OXR_ID=abcdef123456/' .env
   ```
6. Run the service
   ```shell script
   docker-compose up --build
   ```

### Development vs production version

`.env-dev` contains `COMPOSE_FILE` environment variable that is being used by `docker-compose`.
It is set to run service in a `DEVELOPMENT MODE`.

To deploy on production, **don't use** `.env-dev` file.
Other alternatives are to edit `COMPOSE_FILE` variable or to run the compose file explicitly:
```shell script
docker-compose -f docker-compose.yml up --build
```

Development mode:
* Live-code (working directory is mounted, web server is reloaded on any changes)
* Concurrency is disabled (`gunicorn` is shutdown, `uvicorn --reload` is used)

## Usage
### General usage

```shell script
curl -X GET "$HOST/api/currencies/convert/{base}/{to}/{amount}" -H  "accept: application/json"
```

#### Example request _(assuming `.env-dev` settings are used)_

```shell script
curl -X GET "http://0.0.0.0/api/currencies/convert/USD/EUR/123" -H  "accept: application/json"
```

##### Response (Code 200)

```json
{
  "base": "USD",
  "to": "EUR",
  "amount": 123,
  "exchange_rate": {
    "quote": 0.836134,
    "timestamp": "2020-11-29T21:00:02+00:00"
  },
  "result": 102.844482
}
```

## Documentation
### OpenAPI schema

Go to `/openapi.json` to get the OpenAPI JSON schema.

### Interactive API documentation (provided by Swagger UI)

Go to `/docs` to see the automatic interactive API documentation.

![swagger]

### ReDoc

Go to `/redoc` to see the ReDoc documentation.

![redoc]

## Configuration

All application settings are stored in `.env` file.

See `start.sh` for deployment configuration and set corresponding variable via `.env` file if needed.
The most important variables (with default values):

```shell script
LOG_LEVEL=info
ACCESS_LOGFILE="-"
ERROR_LOGFILE="-"

HOST=0.0.0.0
PORT=80

KEEP_ALIVE=5
TIMEOUT=120
GRACEFUL_TIMEOUT=120

WORKERS_PER_CORE=1
MAX_WORKERS=
WEB_CONCURRENCY=
```

### Auto-tune web server

This service has an auto-tuning mechanism to achieve the best performance.
However it's possible to tune the server manually via `WEB_CONCURRENCY` and other environmental variables.
See `start.sh` for more details.

## Tests and development

1. Install [Poetry](https://python-poetry.org)
2. Install all dependencies
   ```shell script
   poetry install
   ```
3. Run test suite
   ```shell script
   poetry run pytest --cov=app
   ```
4. Verify all tests passed
   ```
   ============================ test session starts ============================
   platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
   rootdir: /Users/xsx/+dev/projects/currencies-converter-rest-service-fastapi,
   configfile: pyproject.toml
   plugins: mock-3.3.1, cov-2.10.1, asyncio-0.14.0
   collected 525 items

   tests/test_actions.py ...............................                 [  5%]
   tests/test_api.py ................................................... [ 15%]
   ..................................................................... [ 28%]
   ..................................................................... [ 41%]
   ..................................................................... [ 55%]
   ..................................................................... [ 68%]
   ..................................................................... [ 81%]
   ............................................................          [ 92%]
   tests/test_cache.py .....                                             [ 93%]
   tests/test_celerybeat.py .                                            [ 93%]
   tests/test_celerytasks.py .....                                       [ 94%]
   tests/test_schemas.py ....                                            [ 95%]
   tests/test_validation.py ....................                         [ 99%]
   tests/helpers/test/test_supported_currencies.py ...                   [100%]

   ---------- coverage: platform darwin, python 3.8.6-final-0 -----------
   Name                 Stmts   Miss  Cover
   ----------------------------------------
   app/__init__.py          0      0   100%
   app/actions.py          16      0   100%
   app/api.py               8      0   100%
   app/cache.py            12      0   100%
   app/celerybeat.py       17      1    94%
   app/celerytasks.py      40      0   100%
   app/main.py             13      3    77%
   app/schemas.py          20      0   100%
   app/settings.py          8      0   100%
   ----------------------------------------
   TOTAL                  134      4    97%


   =========================== 525 passed in 10.17s ============================
   ```
5. Test suite contains external services tests that can consume you quota.
   To run test suite excluding external tests
   ```shell script
   poetry run pytest -m "not ext" --cov=app
   ```
6. Setup `COMPOSE_FILE` (e.g. via `.env` file) or run all compose files explicitly
   ```shell script
   docker-compose -f compose-docker.yml -f compose-docker-dev.yml up --build
   ```
7. Happy hacking!

## Built With

* [Python](https://www.python.org)
* [FastAPI](https://fastapi.tiangolo.com)
* [Starlette](https://www.starlette.io)
* [Pydantic](https://pydantic-docs.helpmanual.io)
* [Celery](https://github.com/celery/celery)
* [Redis](https://redis.io)
* [Uvicorn](https://www.uvicorn.org)
* [Gunicorn](https://gunicorn.org)

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

Bart Skowron - [bxsx](https://github.com/bxsx) - bxsx@bartskowron.com

[https://github.com/bxsx/currencies-converter-rest-service-fastapi](https://github.com/bxsx/currencies-converter-rest-service-fastapi)


[swagger]: .github/img/swagger.png
[redoc]: .github/img/redoc.png
