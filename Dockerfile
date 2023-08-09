FROM python:3.11-slim

LABEL org.opencontainers.image.source=https://github.com/almazkun/django_chat

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile ./Pipfile.lock ./

RUN pip3 install pipenv && pipenv install --system

COPY chat ./chat
COPY settings ./settings
COPY manage.py ./

ENTRYPOINT [ "daphne" ]

CMD [ "settings.asgi:application", "-b", "0.0.0.0", "-p", "8000" ]
