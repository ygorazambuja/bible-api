FROM python:3.12

WORKDIR /code

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["uv", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "main.py", "--port", "8000", "--proxy-headers"]