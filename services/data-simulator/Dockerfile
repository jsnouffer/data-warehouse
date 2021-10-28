FROM python:3.9.5-alpine

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps build-base && \
    apk add --no-cache mariadb-connector-c-dev libstdc++

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt && \
    apk del .build-deps

ADD data_simulator ./data_simulator
ADD config.yaml .
ADD Products1.txt .

CMD [ "python", "-m", "data_simulator" ]