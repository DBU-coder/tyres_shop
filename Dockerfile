FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq \
    git \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-alpine
# don't create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# don't docker buffering
ENV PYTHONUNBUFFERED 1

ENV APP_DIR /app

WORKDIR $APP_DIR

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN apk add --no-cache bash libpq; \
    adduser django_app -D; \
    chown -R django_app $APP_DIR

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
