FROM python:3.12

WORKDIR /code

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8000