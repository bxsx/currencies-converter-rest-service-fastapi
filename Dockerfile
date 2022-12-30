FROM python:3.8

LABEL maintainer="Bart Skowron <bart@bxsx.dev>"

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# lock* to make it optional
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev


COPY ./app ./app/
COPY ./.env ./
COPY ./start.sh ./
RUN chmod u+x ./start.sh
