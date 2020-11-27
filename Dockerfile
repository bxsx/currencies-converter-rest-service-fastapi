FROM python:3.8

LABEL maintainer="Bart Skowron <bxsx@bartskowron.com>"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# lock* to make it optional
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev


COPY ./app ./app/
COPY ./start.sh ./
RUN chmod u+x ./start.sh
ENTRYPOINT ./start.sh
