FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y netcat-openbsd
RUN apt-get upgrade -y && apt-get install -y libpq-dev gcc python3-dev musl-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]