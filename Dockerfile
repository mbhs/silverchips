FROM ubuntu:20.04

WORKDIR /app
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm python3 python3-pip postgresql-server-dev-12
RUN npm install -g sass
RUN pip3 install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv lock --pre --clear
RUN pipenv --three install --system --deploy --ignore-pipfile

COPY . .
COPY ./silverchips/secure_settings.py.postgres_example ./silverchips/secure_settings.py
RUN rm core/migrations/*
RUN touch core/migrations/__init__.py

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080
CMD ["/app/entrypoint.sh"]
