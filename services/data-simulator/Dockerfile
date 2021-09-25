FROM python:3.9.5-alpine

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps build-base && \
    apk add --no-cache bash

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt && \
    apk del .build-deps

ADD gitlab_web_app ./gitlab_web_app

CMD [ "python", "-m", "gitlab_web_app" ]
