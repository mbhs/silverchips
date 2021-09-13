FROM archlinux:latest

WORKDIR /app

RUN pacman --noconfirm -Sy base-devel npm python python-pip postgresql-libs icu
RUN npm install -g sass
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv lock
RUN pipenv --three install --system --deploy --ignore-pipfile

COPY . .
COPY ./silverchips/secure_settings.py.example ./silverchips/secure_settings.py
RUN rm core/migrations/*
RUN touch core/migrations/__init__.py
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata core/fixtures/testing.json
RUN python manage.py compilescss
RUN python manage.py collectstatic

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
