# DOCKERIZE python flask app and build VueJS App

# pull official base image
FROM python:3.12.3-alpine

# set work directory
WORKDIR /usr/src/app

# COPY poetry files
COPY pyproject.toml poetry.lock ./

# copy project
COPY . .

# Copy seed data
COPY ./data/data.json /usr/src/app/data/data.json

# install dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install \
    && apk del .build-deps

# install curl
RUN apk add --no-cache curl

# set environment variables
ENV FLASK_APP="./communityenergylabsserver/flaskr/__init__.py"

# expose port and map it to 3000
EXPOSE 5000

# run Flask 
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
