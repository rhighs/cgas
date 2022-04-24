FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=0
WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app
CMD [ "python3", "-u" ,"main.py" ]
