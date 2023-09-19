# pull official base image
FROM python

# set work directory
WORKDIR /app
# set environment variables
# don't create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# don't docker buffering
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat-traditional -y \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN mkdir /app/staticfiles && mkdir /app/media

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
